"""
Música de fondo sintetizada con numpy, de la duración que haga falta y sin
derechos de autor: acordes de pad, bajo, arpegios suaves y, si se pide, batería.

Uso:
  python3 audio/musica.py --duracion 90 -o musica.wav
  python3 audio/musica.py --duracion 30 --estilo ritmo --bpm 110 -o musica.wav

Estilos: «suave» (pad, bajo y arpegio; para narración) y «ritmo» (añade bombo,
charles y palmas). La progresión es La menor, Fa, Do, Sol, un compás cada acorde.
"""
import argparse
import wave

import numpy as np

SR = 48000
NOTAS = {  # Hz
    'F2': 87.31, 'G2': 98.0, 'A2': 110.0, 'C3': 130.81,
    'F3': 174.61, 'G3': 196.0, 'A3': 220.0, 'B3': 246.94, 'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'G4': 392.0,
    'A4': 440.0, 'B4': 493.88, 'C5': 523.25, 'D5': 587.33, 'E5': 659.26, 'F5': 698.46, 'G5': 783.99,
}
PROGRESION = [  # acorde del pad, raíz del bajo, notas del arpegio
    (('A3', 'C4', 'E4'), 'A2', ('A4', 'C5', 'E5')),
    (('F3', 'A3', 'C4'), 'F2', ('F5', 'A4', 'C5')),
    (('C4', 'E4', 'G4'), 'C3', ('C5', 'E5', 'G5')),
    (('G3', 'B3', 'D4'), 'G2', ('G5', 'B4', 'D5')),
]


def tiempo(dur):
    return np.arange(int(SR * dur)) / SR


def filtrar(x, bajo=None, alto=None, orden=2):
    """Filtro en frecuencia con caída tipo Butterworth: bajo = paso bajo, alto = paso alto."""
    espectro = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    ganancia = np.ones_like(f)
    if bajo:
        ganancia /= np.sqrt(1 + (f / bajo) ** (2 * orden))
    if alto:
        ganancia /= np.sqrt(1 + (alto / np.maximum(f, 1e-6)) ** (2 * orden))
    return np.fft.irfft(espectro * ganancia, len(x))


def pad(frecuencias, dur):
    """Tres dientes de sierra algo desafinados por nota, limitados en banda y suavizados."""
    t = tiempo(dur)
    onda = np.zeros_like(t)
    for f in frecuencias:
        for desafine in (-0.18, 0, 0.21):
            fd = f * 2 ** (desafine / 12)
            for k in range(1, int(5000 / fd) + 1):
                onda += np.sin(2 * np.pi * fd * k * t + k * desafine) / k
    onda = filtrar(onda, bajo=1200)
    borde = np.minimum(np.minimum(t / 0.12, (dur - t) / 0.12), 1)
    return onda * borde / (len(frecuencias) * 3)


def nota_bajo(f, dur):
    t = tiempo(dur)
    onda = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)
    return np.tanh(onda * np.minimum(t / 0.01, 1) * np.exp(-t * 2.5) * 1.3)


def pulsacion(f, dur=0.8):
    t = tiempo(dur)
    s = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t) * np.exp(-t * 12)
    return s * np.exp(-t * 5) * np.minimum(t / 0.004, 1)


def bombo():
    t = tiempo(0.45)
    f = 46 + 100 * np.exp(-t * 30)
    return np.tanh(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 8) * 1.5)


def charles(rng):
    t = tiempo(0.06)
    return filtrar(rng.standard_normal(len(t)), alto=7500) * np.exp(-t * 80)


def palmada(rng):
    t = tiempo(0.25)
    golpes = sum(np.exp(-np.maximum(t - d, 0) * 160) * (t >= d) for d in (0, 0.011, 0.023))
    return filtrar(rng.standard_normal(len(t)), bajo=3200, alto=900) * (golpes + np.exp(-t * 16) * 0.6) * 0.8


def poner(pista, senal, inicio, vol=1.0, pan=0.0):
    i = int(inicio * SR)
    if i >= pista.shape[1]:
        return
    s = senal[: pista.shape[1] - i] * vol
    angulo = (pan + 1) * np.pi / 4
    pista[0, i : i + len(s)] += s * np.cos(angulo) * np.sqrt(2)
    pista[1, i : i + len(s)] += s * np.sin(angulo) * np.sqrt(2)


def componer(duracion, bpm=90, estilo='suave', semilla=1):
    rng = np.random.default_rng(semilla)
    pulso = 60 / bpm
    compas = 4 * pulso
    pista = np.zeros((2, int(SR * duracion)))
    # Cada acorde se sintetiza una vez y se reutiliza en todos sus compases.
    pads = [pad([NOTAS[n] for n in acorde], compas + 0.12) for acorde, _, _ in PROGRESION]
    golpe_bombo = bombo()
    n_compases = int(np.ceil(duracion / compas))
    for c in range(n_compases):
        t0 = c * compas
        acorde, raiz, arpegio = PROGRESION[c % len(PROGRESION)]
        poner(pista, pads[c % len(PROGRESION)], t0, 0.55)
        for b in (0, 2):
            poner(pista, nota_bajo(NOTAS[raiz], pulso * 2), t0 + b * pulso, 0.35)
        # Arpegio disperso: algunas corcheas, nunca todas, para que no canse.
        for k in range(8):
            if rng.random() < 0.45:
                nota = arpegio[rng.integers(len(arpegio))]
                poner(pista, pulsacion(NOTAS[nota]), t0 + k * pulso / 2, 0.1, pan=rng.uniform(-0.6, 0.6))
        if estilo == 'ritmo':
            for b in range(4):
                poner(pista, golpe_bombo, t0 + b * pulso, 0.6)
                poner(pista, charles(rng), t0 + (b + 0.5) * pulso, 0.15, pan=0.3)
                if b in (1, 3):
                    poner(pista, palmada(rng), t0 + b * pulso, 0.3, pan=-0.1)
    t = np.arange(pista.shape[1]) / SR
    pista *= np.minimum(np.minimum(t / 1.5, (duracion - t) / 3.0), 1)
    return pista * 0.8 / np.max(np.abs(pista))


def guardar(ruta, pista):
    with wave.open(ruta, 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((pista.T * 32767).astype('<i2').tobytes())


def main():
    p = argparse.ArgumentParser(description='Música de fondo sintetizada, sin derechos.')
    p.add_argument('--duracion', type=float, required=True, help='en segundos')
    p.add_argument('-o', '--salida', default='musica.wav')
    p.add_argument('--bpm', type=float, default=90)
    p.add_argument('--estilo', choices=['suave', 'ritmo'], default='suave')
    p.add_argument('--semilla', type=int, default=1)
    args = p.parse_args()
    guardar(args.salida, componer(args.duracion, args.bpm, args.estilo, args.semilla))
    print(args.salida)


if __name__ == '__main__':
    main()
