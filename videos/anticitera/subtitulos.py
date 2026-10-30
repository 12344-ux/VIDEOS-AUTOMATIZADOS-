"""Subtítulos SRT de la narración, con los tiempos de cada palabra de voz/narrar.py.
Una frase larga se parte en trozos de longitud parecida (mejor tras una coma), sin palabras sueltas.
  python3 videos/anticitera/subtitulos.py salidas/anticitera/audio/voz.json 1.2 > videos/anticitera/apertura/subtitulos.srt
Con varias narraciones (JSON y desfase de cada una), un solo SRT seguido: lo usa unir.sh para el vídeo entero."""
import json
import math
import sys

MAX = 42  # caracteres por subtítulo, más o menos
# El guion escribe algunos nombres como suenan para que la voz los diga bien; los subtítulos, como se escriben.
ESCRITURA = {'Prais': 'Price', 'Máikel': 'Michael', 'Rait': 'Wright', 'Rem': 'Rehm', 'Jaralambos': 'Charalampos',
             'Glásgou': 'Glasgow'}


def escrita(palabra):
    base = palabra.strip('.,:;¿?¡!«»')
    return palabra.replace(base, ESCRITURA[base]) if base in ESCRITURA else palabra


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


def srt(pares):
    """pares: [(ruta del JSON de la narración, segundo del vídeo en que empieza)]."""
    trozos = []
    for ruta, desfase in pares:
        datos = json.load(open(ruta, encoding='utf-8'))
        trozos += [[dict(p, texto=escrita(p['texto']), inicio=p['inicio'] + desfase, fin=p['fin'] + desfase) for p in t]
                   for f in datos['frases'] for t in partir(f['palabras'])]
    salida = []
    for i, t in enumerate(trozos):
        fin = t[-1]['fin'] + 0.12
        if i + 1 < len(trozos):
            fin = min(fin, trozos[i + 1][0]['inicio'] - 0.02)
        salida.append(f"{i + 1}\n{hora(t[0]['inicio'])} --> {hora(fin)}\n{' '.join(p['texto'] for p in t)}\n")
    return '\n'.join(salida)


def main():
    args = sys.argv[1:]
    print(srt([(args[i], float(args[i + 1])) for i in range(0, len(args), 2)]))


if __name__ == '__main__':
    main()
