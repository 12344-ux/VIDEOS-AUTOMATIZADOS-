"""
Ajusta una narración a tiempos dados: estira o encoge (sin cambiar el tono, con el atempo de ffmpeg)
cada tramo entre dos palabras ancla para que cada ancla empiece donde se le pide. Sirve para que una
voz regenerada encaje en una composición ya cronometrada con otra toma.

  python3 voz/ajustar.py voz.wav anclas.json -o voz_ajustada.wav

anclas.json: [{"palabra": "tormenta", "t": 2.44}, {"palabra": "conoce", "fin": 29.57}, ...]
  palabra: el texto de la palabra en el JSON de narrar.py (sin signos; «n» elige la aparición, 1 por
  defecto); t: dónde debe empezar, o fin: dónde debe acabar, en segundos desde el inicio del WAV.
Escribe el WAV y su JSON con los tiempos de frases y palabras rehechos. Avisa si algún tramo cambia más
de un 8 %: a partir de ahí se nota.
"""
import argparse
import json
import os
import re
import subprocess
import tempfile
import wave

import numpy as np

SR = 48000
FUNDIDO = int(0.006 * SR)


def limpia(s):
    return re.sub(r'[^\wáéíóúüñ]', '', s.lower())


def leer(ruta):
    with wave.open(ruta) as w:
        return np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(np.float32) / 32768


def atempo(x, factor):
    """Cambia la duración de x por factor (2 = el doble de largo) sin tocar el tono."""
    if abs(factor - 1) < 1e-4 or len(x) < SR // 50:
        n = max(1, int(round(len(x) * factor)))
        return np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x) if len(x) > 1 else np.zeros(n)
    with tempfile.TemporaryDirectory() as d:
        a, b = os.path.join(d, 'a.raw'), os.path.join(d, 'b.raw')
        x.astype('<f4').tofile(a)
        subprocess.run(['ffmpeg', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', a,
                        '-af', f'atempo={1 / factor:.6f}', '-f', 'f32le', b], check=True)
        y = np.fromfile(b, '<f4')
    # atempo redondea a su bloque: se fija la longitud exacta pedida.
    n = int(round(len(x) * factor))
    return y[:n] if len(y) >= n else np.concatenate([y, np.zeros(n - len(y), np.float32)])


def main():
    p = argparse.ArgumentParser(description='Ajusta una narración a tiempos de palabras dados.')
    p.add_argument('voz')
    p.add_argument('anclas')
    p.add_argument('-o', '--salida', required=True)
    args = p.parse_args()

    x = leer(args.voz)
    datos = json.load(open(os.path.splitext(args.voz)[0] + '.json'))
    palabras = [w for f in datos['frases'] for w in f['palabras']]
    # Puntos fijos: (tiempo en la toma, tiempo pedido). Los extremos de la pista se mueven con su vecino.
    fijos = []
    for a in json.load(open(args.anclas)):
        hechas = [w for w in palabras if limpia(w['texto']) == limpia(a['palabra'])]
        w = hechas[a.get('n', 1) - 1]
        fijos.append((w['inicio'], a['t']) if 't' in a else (w['fin'], a['fin']))
    fijos.sort()
    fijos = [(0.0, max(0.0, fijos[0][1] - fijos[0][0]))] + fijos
    fin_toma = len(x) / SR
    fijos.append((fin_toma, fijos[-1][1] + fin_toma - fijos[-1][0]))

    trozos = []
    for (t0, u0), (t1, u1) in zip(fijos, fijos[1:]):
        if t1 <= t0:
            continue
        factor = (u1 - u0) / (t1 - t0)
        if abs(factor - 1) > 0.08:
            print(f'aviso: el tramo {t0:.2f}–{t1:.2f} s cambia un {100 * (factor - 1):+.0f} %')
        y = atempo(x[int(t0 * SR):int(t1 * SR)], factor)
        if trozos and len(y) > FUNDIDO and len(trozos[-1]) > FUNDIDO:
            r = np.linspace(0, 1, FUNDIDO, dtype=np.float32)
            y[:FUNDIDO] = y[:FUNDIDO] * r + trozos[-1][-FUNDIDO:] * (1 - r)
            trozos[-1] = trozos[-1][:-FUNDIDO]
        trozos.append(y.astype(np.float32))
    y = np.concatenate(trozos)
    y *= 0.9 / max(np.max(np.abs(y)), 1e-6)
    with wave.open(args.salida, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((y * 32767).astype('<i2').tobytes())

    def mapa(t):
        return float(np.interp(t, [f[0] for f in fijos], [f[1] for f in fijos]))
    for f in datos['frases']:
        f['inicio'], f['fin'] = round(mapa(f['inicio']), 3), round(mapa(f['fin']), 3)
        for w in f['palabras']:
            w['inicio'], w['fin'] = round(mapa(w['inicio']), 3), round(mapa(w['fin']), 3)
    datos['duracion'] = round(len(y) / SR, 3)
    datos['ajustada'] = [{'toma': round(a, 3), 'pedido': round(b, 3)} for a, b in fijos]
    with open(os.path.splitext(args.salida)[0] + '.json', 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=1)
    print(json.dumps({'salida': args.salida, 'duracion': datos['duracion'], 'anclas': len(fijos) - 2}, ensure_ascii=False))


if __name__ == '__main__':
    main()
