"""Subtítulos SRT de la narración, con los tiempos de cada palabra de voz/narrar.py.
Una frase larga se parte en trozos de longitud parecida (mejor tras una coma), sin palabras sueltas.
  python3 videos/anticitera/subtitulos.py salidas/anticitera/audio/voz.json 1.2 > videos/anticitera/apertura/subtitulos.srt"""
import json
import math
import sys

MAX = 42  # caracteres por subtítulo, más o menos


def partir(palabras):
    texto = lambda ps: ' '.join(p['texto'] for p in ps)
    if len(texto(palabras)) <= MAX:
        return [palabras]
    n = math.ceil(len(texto(palabras)) / MAX)
    mejor, coste_mejor = None, None
    for i in range(1, len(palabras)):
        a, b = palabras[:i], palabras[i:]
        coste = abs(len(texto(a)) - len(texto(b)) * (n - 1) / max(n - 1, 1) * (1 if n == 2 else 0.5))
        if palabras[i - 1]['texto'].endswith(','):
            coste -= 12
        if coste_mejor is None or coste < coste_mejor:
            mejor, coste_mejor = i, coste
    return partir(palabras[:mejor]) + partir(palabras[mejor:])


def hora(s):
    ms = round(s * 1000)
    return f'{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}'


def main():
    datos, desfase = json.load(open(sys.argv[1], encoding='utf-8')), float(sys.argv[2])
    trozos = [t for f in datos['frases'] for t in partir(f['palabras'])]
    for i, t in enumerate(trozos):
        fin = t[-1]['fin'] + desfase + 0.12
        if i + 1 < len(trozos):
            fin = min(fin, trozos[i + 1][0]['inicio'] + desfase - 0.02)
        print(f"{i + 1}\n{hora(t[0]['inicio'] + desfase)} --> {hora(fin)}\n{' '.join(p['texto'] for p in t)}\n")


if __name__ == '__main__':
    main()
