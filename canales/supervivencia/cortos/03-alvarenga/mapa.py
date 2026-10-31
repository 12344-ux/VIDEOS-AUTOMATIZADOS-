"""
Los mapas de «438 días a la deriva» (Natural Earth 1:10 millones, dominio público), en la pantalla de 1080 × 1920:
  cerca     la costa de Chiapas y El Salvador, de donde salió
  pacifico  el Pacífico entero, de México a las islas Marshall, con la deriva (un esquema: nadie registró la ruta) y
            16 trayectorias de una simulación, también en esquema (la de la Universidad de Hawái soltó 16 trazadores)
Escribe recursos/mapa.json.

  python3 canales/supervivencia/cortos/03-alvarenga/mapa.py
"""
import json
import math
import os
import random
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..', '..', '..', 'geografia', 'kit'))
import geo  # noqa: E402

CHIAPAS = (-93.3, 15.55)        # la costa de Chiapas (Costa Azul, aproximado)
EBON = (168.7, 4.6)             # el atolón de Ebon, en las islas Marshall
# La deriva, en esquema: hacia el oeste con la corriente norecuatorial y, al final, hacia el suroeste hasta Ebon.
DERIVA = [CHIAPAS, (-96.5, 13.6), (-103, 12.2), (-114, 11.4), (-127, 11.0), (-140, 10.4), (-152, 9.5), (-163, 8.4),
          (-174, 7.1), (176, 6.0), (171.5, 5.2), EBON]


def suave(xy, n=8):
    """Catmull-Rom por los puntos: un camino SVG sin quiebros."""
    pts = [xy[0]] + xy + [xy[-1]]
    out = [xy[0]]
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
        for k in range(1, n + 1):
            t = k / n
            out.append(tuple(0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t +
                                    (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t ** 3) for j in (0, 1)))
    return 'M' + 'L'.join(f'{x:.1f},{y:.1f}' for x, y in out)


def meridianos(proj, caja):
    partes = []
    for lon in range(-180, 180, 20):
        partes.append(geo.linea([(lon, lat) for lat in range(-70, 71, 2)], proj, 2.0))
    for lat in range(-60, 61, 10):
        partes.append(geo.linea([((lo + 180) % 360 - 180, lat) for lo in range(60, 300, 2)], proj, 2.0))
    return ''.join(partes)


def main():
    P = geo.paises()
    caja = (-300, -300, 1380, 2220)
    # Cerca: la costa de la salida.
    c = geo.Azimutal(-91.5, 14.6, 0.55, 600, 760)
    cerca = dict(tierra=''.join(geo.camino([p[0] for p in pols], c, 1.6, caja) for n, pols in P.items() if n != 'El Salvador'),
                 salvador=geo.camino([p[0] for p in P['El Salvador']], c, 1.2, caja),
                 chiapas=[round(v, 1) for v in c(*CHIAPAS)], salvador_c=[round(v, 1) for v in c(-88.9, 13.75)],
                 salida=geo.linea([CHIAPAS, (-94.0, 14.9), (-95.2, 14.1), (-96.5, 13.6)], c, 1.0))
    # El Pacífico: centrado a medio camino, a 0,08 px/km.
    p = geo.Azimutal(-142.0, 11.5, 0.08, 548, 800)
    xy = [p(*q) for q in DERIVA]
    random.seed(16)
    trazas = []
    for i in range(16):
        # Cada trazador se desvía un poco más cuanto más lejos va; unos se quedan cortos y otros se pasan.
        largo = 0.8 + 0.4 * random.random()
        desv = random.uniform(-1, 1)
        q = []
        for k, (lon, lat) in enumerate(DERIVA):
            f = k / (len(DERIVA) - 1)
            q.append((lon, lat + desv * 4.0 * f + random.uniform(-0.6, 0.6) * f))
        # Recorta o alarga a lo largo de la deriva.
        n = max(3, round(len(q) * min(1.0, largo)))
        q = q[:n]
        if largo > 1.0:
            lon, lat = q[-1]
            q.append(((lon - 9 * (largo - 1.0) / 0.2 + 180) % 360 - 180, lat - 1.0))
        trazas.append(suave([p(*r) for r in q], 6))
    # Solo la tierra del hemisferio que mira la proyección: un polígono que rodea el antípoda (África) saldría
    # como un anillo gigante que tapa todo el mapa.
    def cerca_del_centro(anillo):
        return max(geo.distancia((-142.0, 11.5), q) for q in anillo[::5]) < 0.5 * math.pi * geo.R * 1.15
    pacifico = dict(tierra=''.join(geo.camino([r[0] for r in pols if cerca_del_centro(r[0])], p, 2.5, caja) for pols in P.values()),
                    marshall=geo.camino([r[0] for r in P['Marshall Is.']], p, 0.2, caja),
                    rejilla=meridianos(p, caja), deriva=suave(xy), trazas=trazas,
                    chiapas=[round(v, 1) for v in p(*CHIAPAS)], ebon=[round(v, 1) for v in p(*EBON)],
                    km=round(geo.distancia(CHIAPAS, EBON)))
    json.dump(dict(cerca=cerca, pacifico=pacifico), open(os.path.join(AQUI, 'recursos', 'mapa.json'), 'w'), separators=(',', ':'))
    print(f"Chiapas {pacifico['chiapas']} → Ebon {pacifico['ebon']}: {pacifico['km']} km en línea recta; "
          f"cerca: Chiapas {cerca['chiapas']}")


if __name__ == '__main__':
    main()
