"""
Lecho de música para un tramo largo: repite una pieza corta (MusicGen da 30 s) con fundidos cruzados
de potencia constante hasta la duración pedida, con entrada y salida suaves, y la deja a un volumen
estándar (loudnorm de ffmpeg). Se le quita el último segundo y medio a la pieza, que MusicGen suele
cortar en seco.

  python3 audio/lecho.py pieza.wav 62.4 -o lecho.wav [--cruce 3] [--lufs -16]
"""
import argparse
import os
import subprocess
import tempfile
import wave

import numpy as np


def leer(ruta):
    with wave.open(ruta) as w:
        sr, ch = w.getframerate(), w.getnchannels()
        x = np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(np.float32) / 32768
    return x.reshape(-1, ch), sr


def main():
    p = argparse.ArgumentParser(description='Lecho de música a una duración dada.')
    p.add_argument('pieza')
    p.add_argument('duracion', type=float)
    p.add_argument('-o', '--salida', required=True)
    p.add_argument('--cruce', type=float, default=3.0, help='segundos de fundido cruzado entre repeticiones')
    p.add_argument('--recorte', type=float, default=1.5, help='segundos que se quitan del final de la pieza')
    p.add_argument('--entrada', type=float, default=1.0)
    p.add_argument('--salida-fundido', type=float, default=2.0, dest='fin')
    p.add_argument('--lufs', type=float, default=-16.0)
    a = p.parse_args()

    x, sr = leer(a.pieza)
    x = x[:len(x) - int(a.recorte * sr)]
    n, c = int(a.duracion * sr), int(a.cruce * sr)
    t = np.linspace(0, np.pi / 2, c)[:, None]
    sube, baja = np.sin(t), np.cos(t)
    y = x.copy()
    while len(y) < n:
        y = np.concatenate([y[:-c], y[-c:] * baja + x[:c] * sube, x[c:]])
    y = y[:n]
    e, f = int(a.entrada * sr), int(a.fin * sr)
    y[:e] *= np.linspace(0, 1, e)[:, None]
    y[-f:] *= np.linspace(1, 0, f)[:, None] ** 2
    with tempfile.TemporaryDirectory() as d:
        crudo = os.path.join(d, 'crudo.wav')
        with wave.open(crudo, 'wb') as w:
            w.setnchannels(y.shape[1])
            w.setsampwidth(2)
            w.setframerate(sr)
            w.writeframes((np.clip(y, -1, 1) * 32767).astype('<i2').tobytes())
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', crudo, '-af', f'loudnorm=I={a.lufs}:TP=-2:LRA=11',
                        '-ar', str(sr), a.salida], check=True)
    print(f'{a.salida}  {a.duracion:.1f} s desde {len(x) / sr:.1f} s de pieza')


if __name__ == '__main__':
    main()
