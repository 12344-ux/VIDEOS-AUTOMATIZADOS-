"""
Cuánta energía de una pieza de música cae bajo 150 Hz. Un móvil no reproduce esa banda: una pieza con la mayor parte
de su energía ahí suena vacía (BusinessForMen: «pulse» y las cuerdas punteadas de MusicGen salieron con el 71–99 %).
También el nivel de cada tramo de 5 s: algunas piezas se apagan antes de acabar (a los 15 o a los 25 s).

  python3 audio/graves.py pieza_1.wav pieza_2.wav ...
"""
import sys
import wave

import numpy as np

for ruta in sys.argv[1:]:
    with wave.open(ruta) as w:
        sr, ch = w.getframerate(), w.getnchannels()
        x = np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(np.float64).reshape(-1, ch).mean(axis=1)
    e = np.abs(np.fft.rfft(x)) ** 2
    f = np.fft.rfftfreq(len(x), 1 / sr)
    total = e[f > 20].sum()
    tramos = ' '.join(f'{20 * np.log10(np.sqrt(np.mean(x[i:i + 5 * sr] ** 2)) / 32768 + 1e-9):.0f}'
                      for i in range(0, len(x) - sr, 5 * sr))
    print(f'{ruta}: {100 * e[(f > 20) & (f < 150)].sum() / total:.0f} % bajo 150 Hz, '
          f'{100 * e[f > 6000].sum() / total:.0f} % sobre 6 kHz, {len(x) / sr:.1f} s; dB cada 5 s: {tramos}')
