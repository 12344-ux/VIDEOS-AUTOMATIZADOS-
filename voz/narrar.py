"""
Narración en local con Piper: convierte un texto o un guion en un WAV de 48 kHz
mono y un JSON con el inicio y el fin de cada frase y de cada palabra. Esos tiempos
sirven para los subtítulos, para que el texto en pantalla caiga en la palabra que lo
dice y para saber cuánto tiene que durar cada escena del vídeo.

Se ejecuta con el Python del entorno de Piper:
  PY=$HERRAMIENTAS/piper/bin/python
  $PY voz/narrar.py "Primera frase. Segunda frase." -o narracion.wav
  $PY voz/narrar.py --guion guion.json -o narracion.wav --voz es_MX-claude-high --velocidad 0.85

guion.json es una lista de segmentos: [{"texto": "...", "pausa": 0.8}, ...].
"pausa" es el silencio tras el segmento, en segundos (por defecto 0,6). Dentro de
cada segmento el texto se parte en frases, separadas por 0,3 s.

El JSON de salida (mismo nombre que el WAV, con .json) tiene:
  {"duracion": s, "voz": ..., "frases": [{"segmento": i, "texto": ..., "inicio": s, "fin": s,
   "palabras": [{"texto": ..., "inicio": s, "fin": s}]}]}

Los tiempos de las palabras salen de la alineación de fonemas de Piper (exacta, al
contrario que Whisper, que aquí falló hasta 0,8 s). Necesita el paquete onnx en el
entorno de Piper; sin él se reparten por longitud.
"""
import argparse
import json
import os
import re
import sys
import wave

import numpy as np
from piper import PiperVoice, SynthesisConfig

SR = 48000
HERRAMIENTAS = os.environ.get('HERRAMIENTAS', os.path.expanduser('~/herramientas-videos'))
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


def sintetizar(voz, texto, velocidad):
    """Audio de una frase a 48 kHz y los tiempos de sus palabras, relativos al audio recortado."""
    trozos = list(voz.synthesize(texto, SynthesisConfig(length_scale=velocidad), include_alignments=True))
    x = np.concatenate([t.audio_int16_array for t in trozos]).astype(float) / 32768
    alineadas = palabras_alineadas(trozos, voz.config.sample_rate)
    x = remuestrear(x, voz.config.sample_rate, SR)
    # Fuera los graves por debajo de 80 Hz, que solo emborronan la mezcla.
    espectro = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    x = np.fft.irfft(espectro / np.sqrt(1 + (80 / np.maximum(f, 1e-6)) ** 4), len(x))
    x, inicio = recortar_silencio(x)
    escritas = texto.split()
    if alineadas is None or len(alineadas) != len(escritas):
        # Sin alineación, o espeak juntó o partió palabras: se reparten por longitud.
        total = sum(len(p) for p in escritas)
        alineadas, t = [], 0.0
        for p in escritas:
            d = len(p) / total * len(x) / SR
            alineadas.append((t, t + d))
            t += d
    else:
        alineadas = [(a - inicio / SR, b - inicio / SR) for a, b in alineadas]
    palabras = [{'texto': p, 'inicio': max(a, 0.0), 'fin': b} for p, (a, b) in zip(escritas, alineadas)]
    return x, palabras


def frases(texto):
    partes = re.split(r'(?<=[.!?…])\s+', texto.strip())
    return [p for p in partes if re.search(r'\w', p)]


def ruta_voz(nombre):
    if nombre.endswith('.onnx') and os.path.exists(nombre):
        return nombre
    ruta = os.path.join(HERRAMIENTAS, 'voces', nombre + '.onnx')
    if not os.path.exists(ruta):
        sys.exit(f'No encuentro la voz {nombre} en {os.path.dirname(ruta)}. Ejecuta: ./instalar.sh voz')
    return ruta


def main():
    p = argparse.ArgumentParser(description='Narración en local con Piper.')
    p.add_argument('texto', nargs='?')
    p.add_argument('--guion', help='JSON con una lista de {"texto", "pausa"}')
    p.add_argument('-o', '--salida', default='narracion.wav')
    p.add_argument('--voz', default='es_AR-daniela-high')
    p.add_argument('--velocidad', type=float, default=1.0, help='menos de 1 habla más rápido')
    args = p.parse_args()
    if args.guion:
        segmentos = json.load(open(args.guion))
    elif args.texto:
        segmentos = [{'texto': args.texto}]
    else:
        p.error('falta el texto o --guion')

    try:
        voz = PiperVoice.load(ruta_voz(args.voz), include_alignments=True)
    except Exception:
        voz = PiperVoice.load(ruta_voz(args.voz))
    trozos, tiempos, t = [], [], 0.0
    for i, segmento in enumerate(segmentos):
        lista = frases(segmento['texto'])
        for j, frase in enumerate(lista):
            x, palabras = sintetizar(voz, frase, args.velocidad)
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
    datos = {'duracion': round(len(pista) / SR, 3), 'voz': args.voz, 'velocidad': args.velocidad, 'frases': tiempos}
    with open(os.path.splitext(args.salida)[0] + '.json', 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=1)
    print(json.dumps({'salida': args.salida, 'duracion': datos['duracion'], 'frases': len(tiempos)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
