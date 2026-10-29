"""
Pista de máquina de escribir hecha con teclas reales: corta cada pulsación de una grabación
(por ejemplo, la «Typewriter #8» de BigSoundBank, CC0) y coloca una en el instante de cada
letra que aparece en pantalla. Los espacios suenan más flojos. Cada tecla sale de un golpe
distinto de la grabación, así no se repite el mismo sonido.

  python3 audio/efectos.py bajar 2841 -o maquina.wav
  python3 audio/tecleo.py maquina.wav -o tecleo.wav --duracion 10 \
      --texto "CABO NORTE" --desde 0.8 --paso 0.053 \
      --texto "LIBRO DE GUARDIA · 1891–2026" --desde 7.45 --paso 0.05

Cada --texto lleva su --desde (segundo de la primera letra) y su --paso (segundos entre letras),
los mismos que usa la animación.
"""
import argparse
import wave

import numpy as np


def leer(ruta):
    with wave.open(ruta) as w:
        sr, canales = w.getframerate(), w.getnchannels()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype='<i2').reshape(-1, canales).astype(float) / 32768
    if canales == 1:
        x = np.repeat(x, 2, axis=1)
    return x[:, :2], sr


def pulsaciones(x, sr, salto_db=14, separacion=0.12, largo=0.14):
    """Recorta cada golpe de tecla: subidas bruscas de energía separadas al menos 0,12 s."""
    m = x.mean(1)
    paso = int(sr * 0.005)
    energia = np.array([np.sqrt(np.mean(m[i:i + paso] ** 2)) for i in range(0, len(m) - paso, paso)])
    db = 20 * np.log10(energia + 1e-9)
    inicios = []
    for i in range(4, len(db)):
        if db[i] - db[i - 4] > salto_db and db[i] > -38 and (not inicios or (i - inicios[-1]) * 0.005 > separacion):
            inicios.append(i)
    n = int(largo * sr)
    caida = np.ones(n)
    caida[-int(0.03 * sr):] = np.linspace(1, 0, int(0.03 * sr))
    golpes = []
    for i in inicios:
        a = max(i * paso - int(0.004 * sr), 0)
        if a + n < len(x):
            g = x[a:a + n] * caida[:, None]
            golpes.append(g / max(np.max(np.abs(g)), 1e-6) * 0.8)
    return golpes


def main():
    p = argparse.ArgumentParser(description='Pista de tecleo con teclas reales.')
    p.add_argument('grabacion', help='WAV con una máquina de escribir')
    p.add_argument('-o', '--salida', default='tecleo.wav')
    p.add_argument('--duracion', type=float, required=True)
    p.add_argument('--texto', action='append', required=True)
    p.add_argument('--desde', action='append', type=float, required=True)
    p.add_argument('--paso', action='append', type=float, required=True)
    args = p.parse_args()
    if not len(args.texto) == len(args.desde) == len(args.paso):
        p.error('cada --texto necesita su --desde y su --paso')

    x, sr = leer(args.grabacion)
    golpes = pulsaciones(x, sr)
    if not golpes:
        p.error('no encuentro pulsaciones en la grabación')
    pista = np.zeros((int(args.duracion * sr), 2))
    k = 0
    for texto, desde, paso in zip(args.texto, args.desde, args.paso):
        for i, letra in enumerate(texto):
            g = golpes[k % len(golpes)]
            k += 1
            a = int((desde + i * paso) * sr)
            n = min(len(g), len(pista) - a)
            if n > 0:
                pista[a:a + n] += g[:n] * (0.45 if letra == ' ' else 0.85)
    pista = np.clip(pista, -1, 1)
    with wave.open(args.salida, 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((pista * 32767).astype('<i2').tobytes())
    print(f'{args.salida}: {k} teclas de {len(golpes)} golpes distintos')


if __name__ == '__main__':
    main()
