"""
El mapa de «Tres semanas solo en el Amazonas» (Natural Earth 1:10 millones, dominio público), en la pantalla de 1080 × 1920:
Bolivia y sus vecinos y, al norte de La Paz, la selva del río Tuichi. Natural Earth no trae ríos en este archivo: el Tuichi
va en esquema, del alto Tuichi a su desembocadura en el río Beni, junto a Rurrenabaque, con la cascada donde Yossi
Ghinsberg cayó y la orilla donde lo encontraron (posiciones aproximadas). Escribe recursos/mapa.json.

  python3 canales/supervivencia/cortos/16-ghinsberg/mapa.py
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..', '..', '..', 'geografia', 'kit'))
import geo  # noqa: E402

LA_PAZ = (-68.150, -16.500)
RURRENABAQUE = (-67.528, -14.441)
# El río Tuichi, en esquema, de oeste a este hasta el Beni; la cascada y la orilla del rescate, aproximadas.
TUICHI = [(-68.78, -14.66), (-68.55, -14.52), (-68.32, -14.50), (-68.12, -14.56), (-67.95, -14.49), (-67.78, -14.40), (-67.60, -14.37)]
BENI = [(-67.75, -14.95), (-67.62, -14.62), (-67.55, -14.45), (-67.50, -14.25), (-67.40, -13.95)]
CASCADA = (-68.32, -14.50)
ORILLA = (-67.95, -14.49)


def main():
    P = geo.paises()
    p = geo.Azimutal(-66.0, -16.5, 0.55, 540, 860)
    caja = (-2600, -2600, 3600, 4400)
    xy = lambda c: [round(v, 1) for v in p(*c)]
    camino = lambda pts: 'M' + 'L'.join(','.join(str(v) for v in xy(c)) for c in pts)
    datos = dict(
        bolivia=geo.camino([r[0] for r in P['Bolivia']], p, 0.6, caja),
        resto=''.join(geo.camino([r[0] for r in P[n]], p, 1.0, caja) for n in ('Peru', 'Brazil', 'Chile', 'Argentina', 'Paraguay') if n in P),
        la_paz=xy(LA_PAZ), rurrenabaque=xy(RURRENABAQUE), cascada=xy(CASCADA), orilla=xy(ORILLA),
        tuichi=camino(TUICHI), beni=camino(BENI),
        # De Rurrenabaque, río arriba por el Tuichi, hasta la orilla (la búsqueda en barca).
        busqueda=camino([RURRENABAQUE, (-67.60, -14.37), (-67.78, -14.40), ORILLA]))
    json.dump(datos, open(os.path.join(AQUI, 'recursos', 'mapa.json'), 'w'), separators=(',', ':'))
    print(f"La Paz {datos['la_paz']} · Rurrenabaque {datos['rurrenabaque']} · cascada {datos['cascada']} · orilla {datos['orilla']}")


if __name__ == '__main__':
    main()
