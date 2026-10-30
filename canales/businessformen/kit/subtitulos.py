"""
Subtítulos (SRT) de un vídeo de BusinessForMen a partir de los tiempos de su narración (voz.json, palabra a palabra).
En pantalla se escribe como se lee, no como se pronuncia: los nombres que la voz dice a la española vuelven a su
grafía (videos/<vídeo>/recursos/pantalla.json: «Dóbliu Ti Grant» → «W. T. Grant») y las cantidades van en cifras
(«ciento veinte millones» → «120 millones», «dos mil dieciocho» → «2018»); los números del uno al diez se quedan
en letra («cuatro de cada diez», «Dos: prevé…»). Cada subtítulo, de una o dos líneas de 42 caracteres como mucho.

  python3 canales/businessformen/kit/subtitulos.py 01-flujo-de-caja     escribe salidas/businessformen/<vídeo>/subtitulos.srt
"""
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
VOZ0 = 0.8          # la entrada de la voz en el vídeo (la misma que en montar.py)
LINEA = 42
MAX_DUR = 8.0
# Palabras que no cierran una línea ni un subtítulo («…lo que gana a / casi…» se lee mal).
DEBIL = set('a al de del el la los las un una y o en con por para que se lo le sus su tu tus mi no es muy'.split())

UNIDADES = dict(un=1, uno=1, una=1, dos=2, tres=3, cuatro=4, cinco=5, seis=6, siete=7, ocho=8, nueve=9, diez=10,
                once=11, doce=12, trece=13, catorce=14, quince=15, dieciséis=16, diecisiete=17, dieciocho=18,
                diecinueve=19, veinte=20, veintiuno=21, veintiún=21, veintidós=22, veintitrés=23, veinticuatro=24,
                veinticinco=25, veintiséis=26, veintisiete=27, veintiocho=28, veintinueve=29)
DECENAS = dict(treinta=30, cuarenta=40, cincuenta=50, sesenta=60, setenta=70, ochenta=80, noventa=90)
CENTENAS = dict(cien=100, ciento=100, doscientos=200, trescientos=300, cuatrocientos=400, quinientos=500,
                seiscientos=600, setecientos=700, ochocientos=800, novecientos=900)
CENTENAS.update({k[:-2] + 'as': v for k, v in CENTENAS.items() if k.endswith('os')})
NUMERO = {**UNIDADES, **DECENAS, **CENTENAS, 'mil': 1000}
CANTIDAD = {'millones', 'euros', 'dólares', 'libras', 'tiendas', 'días', 'semanas'}


def limpia(s):
    return re.sub(r'[^\wáéíóúüñ]', '', s.lower())


def valor(palabras):
    total = actual = 0
    for p in palabras:
        if p == 'mil':
            total += (actual or 1) * 1000
            actual = 0
        else:
            actual += NUMERO[p]
    return total + actual


def cifras(tokens):
    """Junta las cantidades dichas en letra en una sola palabra con su cifra."""
    out, i = [], 0
    while i < len(tokens):
        j = i
        while j < len(tokens) and limpia(tokens[j]['texto']) in NUMERO:
            ultimo = tokens[j]['texto']
            j += 1
            if re.search(r'[.,:;?!]$', ultimo):
                break
            # «y» solo une decenas y unidades: «setenta y tres», no «sesenta y seis y mil…».
            if (j + 1 < len(tokens) and limpia(tokens[j]['texto']) == 'y' and limpia(tokens[j - 1]['texto']) in DECENAS
                    and limpia(tokens[j + 1]['texto']) in UNIDADES and UNIDADES[limpia(tokens[j + 1]['texto'])] < 10):
                j += 1
        if j == i:
            out.append(tokens[i]); i += 1
            continue
        grupo = tokens[i:j]
        nums = [limpia(t['texto']) for t in grupo if limpia(t['texto']) != 'y']
        v = valor(nums)
        if v <= 10 and 'mil' not in nums:
            out.extend(grupo); i = j
            continue
        sigue = limpia(tokens[j]['texto']) if j < len(tokens) else ''
        txt = str(v) if 1000 <= v <= 2100 and sigue not in CANTIDAD else f'{v:,}'.replace(',', '.')
        cola = re.search(r'[.,:;?!]*$', grupo[-1]['texto']).group(0)
        cabeza = '¿' if grupo[0]['texto'].startswith('¿') else ''
        out.append(dict(texto=cabeza + txt + cola, inicio=grupo[0]['inicio'], fin=grupo[-1]['fin']))
        i = j
    return out


def nombres(tokens, pantalla):
    """Devuelve los nombres a su grafía: «Dóbliu Ti Grant» → «W. T. Grant»."""
    for dicho, escrito in sorted(pantalla.items(), key=lambda kv: -len(kv[0].split())):
        busca = dicho.split()
        i = 0
        while i <= len(tokens) - len(busca):
            if all(re.sub(r'[.,:;?!]+$', '', tokens[i + k]['texto']) == b for k, b in enumerate(busca)):
                cola = re.search(r'[.,:;?!]*$', tokens[i + len(busca) - 1]['texto']).group(0)
                tokens[i:i + len(busca)] = [dict(texto=escrito + cola, inicio=tokens[i]['inicio'], fin=tokens[i + len(busca) - 1]['fin'])]
            i += 1
    return tokens


def trozos(tokens):
    """Parte una frase en subtítulos de dos líneas como mucho, mejor tras una coma o dos puntos."""
    out, actual = [], []
    for t in tokens:
        prueba = ' '.join(x['texto'] for x in actual + [t])
        if actual and (len(prueba) > 2 * LINEA - 4 or t['fin'] - actual[0]['inicio'] > MAX_DUR):
            corte = max((k for k in range(1, len(actual)) if re.search(r'[,:;]$', actual[k - 1]['texto'])
                         and len(' '.join(x['texto'] for x in actual[:k])) >= 24), default=None)
            if not corte:
                corte = max((k for k in range(1, len(actual) + 1) if limpia(actual[k - 1]['texto']) not in DEBIL), default=len(actual))
            out.append(actual[:corte]); actual = actual[corte:]
        actual.append(t)
    if actual:
        out.append(actual)
    return out


def lineas(texto):
    if len(texto) <= LINEA:
        return texto
    def nota(e):
        izq = texto[:e].split()[-1]
        castigo = 100 if limpia(izq) in DEBIL or re.search(r'\d$', izq) else 0
        return abs(e - len(texto) / 2) + castigo - (12 if re.search(r'[,:;]$', izq) else 0) + (200 if max(e, len(texto) - e - 1) > LINEA else 0)
    k = min((m.start() for m in re.finditer(' ', texto)), key=nota)
    return texto[:k] + '\n' + texto[k + 1:]


def hora(t):
    ms = int(round(t * 1000))
    return f'{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}'


def main():
    video = sys.argv[1]
    trabajo = os.path.join(REPO, 'salidas', 'businessformen', video)
    voz = json.load(open(os.path.join(trabajo, 'voz', 'voz.json')))
    ruta = os.path.join(REPO, 'canales', 'businessformen', 'videos', video, 'recursos', 'pantalla.json')
    pantalla = {k: v for k, v in json.load(open(ruta)).items() if not k.startswith('_')} if os.path.exists(ruta) else {}
    subs = []
    for f in voz['frases']:
        tokens = cifras(nombres([dict(p) for p in f['palabras']], pantalla))
        for tr in trozos(tokens):
            subs.append([tr[0]['inicio'] + VOZ0, tr[-1]['fin'] + VOZ0, ' '.join(x['texto'] for x in tr)])
    for k, s in enumerate(subs):
        siguiente = subs[k + 1][0] if k + 1 < len(subs) else s[1] + 2
        s[1] = min(max(s[1] + 0.25, s[0] + 1.0), siguiente - 0.05)
    salida = os.path.join(trabajo, 'subtitulos.srt')
    with open(salida, 'w') as o:
        for k, (a, b, t) in enumerate(subs, 1):
            o.write(f'{k}\n{hora(a)} --> {hora(b)}\n{lineas(t)}\n\n')
    print(json.dumps({'srt': salida, 'subtitulos': len(subs)}))


if __name__ == '__main__':
    main()
