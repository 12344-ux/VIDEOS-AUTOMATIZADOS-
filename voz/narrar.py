"""
Narración en local: convierte un texto o un guion en un WAV de 48 kHz mono y un JSON con el
inicio y el fin de cada frase y de cada palabra. Esos tiempos sirven para los subtítulos, para
que el texto en pantalla caiga en la palabra que lo dice y para saber cuánto dura cada escena.

Voces: «supertonic-M1» (Supertonic-3, masculina, la principal del proyecto; también M2–M5 y
F1–F5) o una de Piper por su nombre, como «es_AR-daniela-high» (femenina, acento argentino).

Se ejecuta con el Python del entorno de Piper:
  PY=$HERRAMIENTAS/piper/bin/python
  $PY voz/narrar.py "Primera frase. Segunda frase." -o narracion.wav
  $PY voz/narrar.py --guion guion.json -o narracion.wav --voz es_AR-daniela-high --velocidad 1.08

guion.json es una lista de segmentos: [{"texto": "...", "pausa": 0.8}, ...].
"pausa" es el silencio tras el segmento, en segundos (por defecto 0,6). Dentro de
cada segmento el texto se parte en frases, separadas por 0,3 s.

El JSON de salida (mismo nombre que el WAV, con .json) tiene:
  {"duracion": s, "voz": ..., "frases": [{"segmento": i, "texto": ..., "inicio": s, "fin": s,
   "palabras": [{"texto": ..., "inicio": s, "fin": s}]}]}

--velocidad es la duración relativa: 1,1 habla un 10 % más despacio, 0,9 más rápido.

Tiempos de las palabras: con Piper salen de su alineación de fonemas (exacta; necesita el
paquete onnx en su entorno). Con Supertonic, de voz/alinear.py, la alineación forzada sobre la
pista final (17 ms de error medio). Si falta algo, se reparten por longitud y lo avisa.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import wave

import numpy as np
from piper import PiperVoice, SynthesisConfig

SR = 48000
HERRAMIENTAS = os.environ.get('HERRAMIENTAS', os.path.expanduser('~/herramientas-videos'))
AQUI = os.path.dirname(os.path.abspath(__file__))
PY_SUPERTONIC = os.path.join(HERRAMIENTAS, 'supertonic', 'bin', 'python')
PY_ALINEADOR = os.path.join(HERRAMIENTAS, 'fastsdcpu', 'env', 'bin', 'python')
PAUSA_FRASE = 0.3
PAUSA_SEGMENTO = 0.6


def remuestrear(x, origen, destino):
    """Cambio de frecuencia por FFT: limpio para subir de 22 kHz a 48 kHz."""
    n = round(len(x) * destino / origen)
    espectro = np.fft.rfft(x)
    salida = np.zeros(n // 2 + 1, dtype=complex)
    m = min(len(espectro), len(salida))
    salida[:m] = espectro[:m]
    return np.fft.irfft(salida, n) * n / len(x)


def recortar_silencio(x, umbral=0.02):
    """Devuelve el audio sin el silencio de los bordes y la muestra donde empieza el recorte."""
    sonoro = np.flatnonzero(np.abs(x) > umbral * np.max(np.abs(x)))
    inicio = max(sonoro[0] - 240, 0)
    return x[inicio : sonoro[-1] + 2400], inicio


def palabras_alineadas(trozos, sr):
    """Inicio y fin, en segundos, de cada palabra según la alineación de fonemas de Piper.

    Los fonemas de una palabra van entre espacios; la puntuación, el inicio y el final
    de frase no cuentan como palabra. Devuelve None si la voz no da alineaciones."""
    palabras, desplazamiento = [], 0
    for trozo in trozos:
        if not trozo.phoneme_alignments:
            return None
        muestra, inicio, fin = desplazamiento, None, None
        for alineacion in trozo.phoneme_alignments:
            fonema = alineacion.phoneme
            if fonema == ' ':
                if inicio is not None:
                    palabras.append((inicio / sr, fin / sr))
                inicio = None
            elif re.match(r'[\w\u0250-\u02ff\u0300-\u036f]', fonema):
                inicio = muestra if inicio is None else inicio
                fin = muestra + alineacion.num_samples
            muestra += alineacion.num_samples
        if inicio is not None:
            palabras.append((inicio / sr, fin / sr))
        desplazamiento += len(trozo.audio_int16_array)
    return palabras


def limpiar(x, sr):
    """A 48 kHz, sin graves por debajo de 80 Hz (solo emborronan la mezcla) y sin silencio en los bordes."""
    x = remuestrear(x, sr, SR)
    espectro = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    x = np.fft.irfft(espectro / np.sqrt(1 + (80 / np.maximum(f, 1e-6)) ** 4), len(x))
    return recortar_silencio(x)


def por_longitud(texto, duracion):
    """Tiempos aproximados: reparte la frase entre sus palabras según su número de letras."""
    escritas = texto.split()
    total = sum(len(p) for p in escritas)
    palabras, t = [], 0.0
    for p in escritas:
        d = len(p) / total * duracion
        palabras.append({'texto': p, 'inicio': t, 'fin': t + d})
        t += d
    return palabras


def sintetizar_piper(voz, texto, velocidad):
    """Audio de una frase a 48 kHz y los tiempos de sus palabras, relativos al audio recortado."""
    trozos = list(voz.synthesize(texto, SynthesisConfig(length_scale=velocidad), include_alignments=True))
    x = np.concatenate([t.audio_int16_array for t in trozos]).astype(float) / 32768
    alineadas = palabras_alineadas(trozos, voz.config.sample_rate)
    x, inicio = limpiar(x, voz.config.sample_rate)
    escritas = texto.split()
    if alineadas is None or len(alineadas) != len(escritas):
        # Sin alineación, o espeak juntó o partió palabras.
        return x, por_longitud(texto, len(x) / SR)
    return x, [{'texto': p, 'inicio': max(a - inicio / SR, 0.0), 'fin': b - inicio / SR}
               for p, (a, b) in zip(escritas, alineadas)]


def leer_wav(ruta):
    with wave.open(ruta) as w:
        sr, canales = w.getframerate(), w.getnchannels()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype='<i2').reshape(-1, canales).mean(1)
    return x.astype(float) / 32768, sr


def sintetizar_supertonic(nombre, lista, velocidad):
    """Audio de cada frase a 48 kHz con Supertonic-3 (en su propio entorno). Sin tiempos de palabras."""
    if not os.path.exists(PY_SUPERTONIC):
        sys.exit('Falta Supertonic. Ejecuta: ./instalar.sh voz')
    with tempfile.TemporaryDirectory() as carpeta:
        pedido = {'voz': nombre, 'velocidad': velocidad, 'pasos': 12, 'carpeta': carpeta, 'frases': lista}
        entorno = dict(os.environ, SUPERTONIC_CACHE_DIR=os.path.join(HERRAMIENTAS, 'supertonic-3'),
                       HF_HUB_DISABLE_TELEMETRY='1')
        r = subprocess.run([PY_SUPERTONIC, os.path.join(AQUI, 'supertonic_frases.py')], input=json.dumps(pedido),
                           capture_output=True, text=True, env=entorno)
        if r.returncode != 0:
            sys.exit(f'Supertonic falló:\n{r.stderr[-2000:]}')
        return [limpiar(*leer_wav(ruta))[0] for ruta in json.loads(r.stdout.strip().splitlines()[-1])]


def alinear_pista(ruta_wav, tiempos):
    """Pone los tiempos de cada palabra con voz/alinear.py (alineación forzada sobre la pista final)."""
    texto = ' '.join(f['texto'] for f in tiempos)
    with tempfile.NamedTemporaryFile(suffix='.json') as tmp:
        entorno = dict(os.environ, HF_HUB_OFFLINE='1', TRANSFORMERS_VERBOSITY='error', TQDM_DISABLE='1')
        r = subprocess.run([PY_ALINEADOR, os.path.join(AQUI, 'alinear.py'), ruta_wav, texto, '-o', tmp.name],
                           capture_output=True, text=True, env=entorno) if os.path.exists(PY_ALINEADOR) else None
        if r is None or r.returncode != 0:
            print('Aviso: sin alineador (./instalar.sh imagen edicion); tiempos de palabras aproximados.', file=sys.stderr)
            return False
        palabras = json.load(open(tmp.name))
    k = 0
    for frase in tiempos:
        n = len(frase['texto'].split())
        frase['palabras'] = palabras[k:k + n]
        k += n
    return True


def frases(texto):
    partes = re.split(r'(?<=[.!?…])\s+', texto.strip())
    return [p for p in partes if re.search(r'\w', p)]


def ruta_voz(nombre):
    """Archivo .onnx de una voz de Piper."""
    if nombre.endswith('.onnx') and os.path.exists(nombre):
        return nombre
    ruta = os.path.join(HERRAMIENTAS, 'voces', nombre + '.onnx')
    if not os.path.exists(ruta):
        sys.exit(f'No encuentro la voz {nombre} en {os.path.dirname(ruta)}. Ejecuta: ./instalar.sh voz')
    return ruta


def main():
    p = argparse.ArgumentParser(description='Narración en local (Supertonic-3 o Piper).')
    p.add_argument('texto', nargs='?')
    p.add_argument('--guion', help='JSON con una lista de {"texto", "pausa"}')
    p.add_argument('-o', '--salida', default='narracion.wav')
    p.add_argument('--voz', default='supertonic-M1', help='supertonic-M1…M5/F1…F5 o una voz de Piper')
    p.add_argument('--velocidad', type=float, default=1.0, help='duración relativa: menos de 1 habla más rápido')
    args = p.parse_args()
    if args.guion:
        segmentos = json.load(open(args.guion))
    elif args.texto:
        segmentos = [{'texto': args.texto}]
    else:
        p.error('falta el texto o --guion')

    todas = [(i, j, frase) for i, s in enumerate(segmentos) for j, frase in enumerate(frases(s['texto']))]
    supertonic = args.voz.startswith('supertonic-')
    if supertonic:
        audios = sintetizar_supertonic(args.voz.split('-', 1)[1], [f for _, _, f in todas], args.velocidad)
        sintetizadas = iter((x, por_longitud(f, len(x) / SR)) for x, (_, _, f) in zip(audios, todas))
    else:
        try:
            voz = PiperVoice.load(ruta_voz(args.voz), include_alignments=True)
        except Exception:
            voz = PiperVoice.load(ruta_voz(args.voz))
        sintetizadas = (sintetizar_piper(voz, f, args.velocidad) for _, _, f in todas)
    trozos, tiempos, t = [], [], 0.0
    for i, segmento in enumerate(segmentos):
        lista = frases(segmento['texto'])
        for j, frase in enumerate(lista):
            x, palabras = next(sintetizadas)
            trozos.append(x)
            palabras = [{'texto': p['texto'], 'inicio': round(t + p['inicio'], 3), 'fin': round(t + p['fin'], 3)} for p in palabras]
            tiempos.append({'segmento': i, 'texto': frase, 'inicio': round(t, 3), 'fin': round(t + len(x) / SR, 3),
                            'palabras': palabras})
            t += len(x) / SR
            pausa = PAUSA_FRASE if j < len(lista) - 1 else segmento.get('pausa', PAUSA_SEGMENTO)
            trozos.append(np.zeros(int(pausa * SR)))
            t += pausa

    pista = np.concatenate(trozos)
    pista *= 0.9 / np.max(np.abs(pista))
    with wave.open(args.salida, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((pista * 32767).astype('<i2').tobytes())
    if supertonic:
        alinear_pista(args.salida, tiempos)
    datos = {'duracion': round(len(pista) / SR, 3), 'voz': args.voz, 'velocidad': args.velocidad, 'frases': tiempos}
    with open(os.path.splitext(args.salida)[0] + '.json', 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=1)
    print(json.dumps({'salida': args.salida, 'duracion': datos['duracion'], 'frases': len(tiempos)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
