"""
El mapa de W. T. Grant para la escena «mapa»: el contorno de los 48 estados contiguos (us-atlas, nation-albers-10m,
de dominio público, ya proyectado en Albers) llevado a la pantalla de 1920 × 1080, y mil puntos dentro, uno por
tienda (la cadena llegó a tener más de mil), más densos al este y ordenados desde Lynn (Massachusetts), donde abrió
la primera en 1906: así se encienden de la costa este hacia el oeste. La posición de cada punto es ilustrativa.

  python3 canales/businessformen/videos/01-flujo-de-caja/mapa.py      escribe recursos/mapa.json
"""
import json
import math
import os
import random

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(AQUI))))
ORIGEN = os.path.join(REPO, 'salidas', 'businessformen', 'datos', 'nation-albers-10m.json')
CAJA = (380, 300, 1540, 960)       # dónde cae el mapa en la pantalla (debajo del nombre y su fecha)
LYNN = (912, 148)                   # Lynn (Massachusetts), en coordenadas de la proyección (975 × 610)
N = 1000


def anillos():
    d = json.load(open(ORIGEN))
    (sx, sy), (tx, ty) = d['transform']['scale'], d['transform']['translate']
    arcos = []
    for a in d['arcs']:
        x = y = 0
        pts = []
        for dx, dy in a:
            x += dx; y += dy
            pts.append((x * sx + tx, y * sy + ty))
        arcos.append(pts)

    def arco(i):
        return arcos[i] if i >= 0 else arcos[~i][::-1]

    out = []
    for g in d['objects']['nation']['geometries']:
        polis = g['arcs'] if g['type'] == 'MultiPolygon' else [g['arcs']]
        for poli in polis:
            for anillo in poli:
                pts = []
                for i in anillo:
                    pts.extend(arco(i)[1:] if pts else arco(i))
                out.append(pts)
    return out


def area(p):
    return abs(sum(p[i][0] * p[i - 1][1] - p[i - 1][0] * p[i][1] for i in range(len(p)))) / 2


def dentro(x, y, anillos):
    c = False
    for p in anillos:
        j = len(p) - 1
        for i in range(len(p)):
            (xi, yi), (xj, yj) = p[i], p[j]
            if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
                c = not c
            j = i
    return c


def main():
    todos = anillos()
    # Los 48 contiguos: fuera los recuadros de Alaska y Hawái (abajo a la izquierda) y las islas diminutas.
    contiguos = [p for p in todos if area(p) > 20 and not (min(x for x, _ in p) < 330 and min(y for _, y in p) > 400)]
    xs = [x for p in contiguos for x, _ in p]; ys = [y for p in contiguos for _, y in p]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    k = min((CAJA[2] - CAJA[0]) / (x1 - x0), (CAJA[3] - CAJA[1]) / (y1 - y0))
    ox = CAJA[0] + ((CAJA[2] - CAJA[0]) - (x1 - x0) * k) / 2 - x0 * k
    oy = CAJA[1] + ((CAJA[3] - CAJA[1]) - (y1 - y0) * k) / 2 - y0 * k
    pant = lambda x, y: (round(ox + x * k, 1), round(oy + y * k, 1))
    d = ''.join('M' + 'L'.join(f'{a},{b}' for a, b in (pant(x, y) for x, y in p[::2])) + 'Z' for p in contiguos)
    rnd = random.Random(1906)
    puntos = []
    while len(puntos) < N:
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        peso = 0.18 + 0.82 * ((x - x0) / (x1 - x0)) ** 1.6      # más tiendas al este
        if rnd.random() < peso and dentro(x, y, contiguos):
            orden = math.hypot(x - LYNN[0], y - LYNN[1]) * (0.8 + 0.4 * rnd.random())
            puntos.append((orden, pant(x, y)))
    puntos.sort()
    lynn = pant(*LYNN)
    json.dump({'contorno': d, 'puntos': [p for _, p in puntos], 'lynn': lynn}, open(os.path.join(AQUI, 'recursos', 'mapa.json'), 'w'),
              separators=(',', ':'))
    print(f'{len(contiguos)} anillos, {len(d)} caracteres de contorno, {len(puntos)} puntos; Lynn en {lynn}')


if __name__ == '__main__':
    main()
