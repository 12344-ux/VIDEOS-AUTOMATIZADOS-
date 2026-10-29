"""
Narración en local con Piper: convierte un texto o un guion en un WAV de 48 kHz
mono y un JSON con el inicio y el fin de cada frase. Esos tiempos sirven para
los subtítulos y para saber cuánto tiene que durar cada escena del vídeo.

Se ejecuta con el Python del entorno de Piper:
  PY=$HERRAMIENTAS/piper/bin/python
  $PY voz/narrar.py "Primera frase. Segunda frase." -o narracion.wav
  $PY voz/narrar.py --guion guion.json -o narracion.wav --voz es_MX-claude-high --velocidad 0.85

guion.json es una lista de segmentos: [{"texto": "...", "pausa": 0.8}, ...].
"pausa" es el silencio tras el segmento, en segundos (por defecto 0,6). Dentro de
cada segmento el texto se parte en frases, separadas por 0,3 s.

El JSON de salida (mismo nombre que el WAV, con .json) tiene:
  {"duracion": s, "voz": ..., "frases": [{"segmento": i, "texto": ..., "inicio": s, "fin": s}]}
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
    sonoro = np.flatnonzero(np.abs(x) > umbral * np.max(np.abs(x)))
    return x[max(sonoro[0] - 240, 0) : sonoro[-1] + 2400]


def sintetizar(voz, texto, velocidad):
    trozos = voz.synthesize(texto, SynthesisConfig(length_scale=velocidad))
    x = np.concatenate([t.audio_int16_array for t in trozos]).astype(float) / 32768
    x = remuestrear(x, voz.config.sample_rate, SR)
    # Fuera los graves por debajo de 80 Hz, que solo emborronan la mezcla.
    espectro = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    x = np.fft.irfft(espectro / np.sqrt(1 + (80 / np.maximum(f, 1e-6)) ** 4), len(x))
    return recortar_silencio(x)


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

    voz = PiperVoice.load(ruta_voz(args.voz))
    trozos, tiempos, t = [], [], 0.0
    for i, segmento in enumerate(segmentos):
        lista = frases(segmento['texto'])
        for j, frase in enumerate(lista):
            x = sintetizar(voz, frase, args.velocidad)
            trozos.append(x)
            tiempos.append({'segmento': i, 'texto': frase, 'inicio': round(t, 3), 'fin': round(t + len(x) / SR, 3)})
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
