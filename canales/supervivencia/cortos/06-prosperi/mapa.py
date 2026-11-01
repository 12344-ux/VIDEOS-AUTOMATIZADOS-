"""
El mapa de «9 días en el Sahara» (Natural Earth 1:10 millones, dominio público), en la pantalla de 1080 × 1920: el sur
de Marruecos y el oeste de Argelia, la salida de la carrera (Foum Zguid) y Tinduf, en Argelia, adonde lo llevaron. Su
camino es un esquema: nadie lo registró; las fuentes dicen que acabó a 291 km de la carrera (Foum Zguid–Tinduf, 295 km en
línea recta). Escribe recursos/mapa.json.

  python3 canales/supervivencia/cortos/06-prosperi/mapa.py
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..', '..', '..', 'geografia', 'kit'))
import geo  # noqa: E402

CARRERA = (-6.87, 30.08)        # Foum Zguid, salida de la Maratón de las Arenas de 1994 (la etapa 4, por la zona: aproximado)
TINDUF = (-8.147, 27.674)       # Tinduf, Argelia: el hospital adonde lo llevaron
# Su camino, en esquema: hacia el sur y el suroeste, hacia las montañas que creía en la ruta, hasta Argelia.
CAMINO = [CARRERA, (-6.95, 29.75), (-7.25, 29.35), (-7.5, 28.95), (-7.75, 28.5), (-7.95, 28.1), (-8.05, 27.85)]


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


def main():
    P = geo.paises()
    caja = (-300, -300, 1380, 2220)
    # Centrado entre la carrera y Tinduf, a 2 px/km: los 295 km ocupan unos 590 px.
    p = geo.Azimutal(-7.5, 28.9, 2.0, 540, 700)
    vecinos = [n for n in ('W. Sahara', 'Mauritania', 'Mali', 'Spain', 'Tunisia', 'Libya', 'Portugal') if n in P]
    datos = dict(
        marruecos=geo.camino([r[0] for r in P['Morocco']], p, 1.2, caja),
        argelia=geo.camino([r[0] for r in P['Algeria']], p, 1.2, caja),
        vecinos=''.join(geo.camino([r[0] for r in P[n]], p, 1.2, caja) for n in vecinos),
        frontera=''.join(geo.linea(l, p, 1.0) for l in geo.fronteras('Morocco', 'Algeria')),
        camino=suave([p(*q) for q in CAMINO]),
        carrera=[round(v, 1) for v in p(*CARRERA)], tinduf=[round(v, 1) for v in p(*TINDUF)],
        km=round(geo.distancia(CARRERA, TINDUF)))
    json.dump(datos, open(os.path.join(AQUI, 'recursos', 'mapa.json'), 'w'), separators=(',', ':'))
    print(f"carrera {datos['carrera']} → Tinduf {datos['tinduf']}: {datos['km']} km en línea recta")


if __name__ == '__main__':
    main()
