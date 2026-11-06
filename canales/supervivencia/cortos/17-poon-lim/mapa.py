"""
El mapa de «133 días solo en una balsa» (Natural Earth 1:10 millones, dominio público), en la pantalla de 1080 × 1920: el
Atlántico ecuatorial entre el nordeste de Brasil y el oeste de África. El Benlomond iba de Ciudad del Cabo a Paramaribo y
el U-172 lo hundió el 23 de noviembre de 1942 en 00°30′ N, 38°45′ O (uboat.net y Wikipedia), a unos 400 km al norte de la
costa de Brasil. Poon Lim derivó hacia el oeste y el 5 de abril de 1943 lo encontraron unos pescadores a unos 16 km de la
costa de Pará, al este de Salinas; lo llevaron a Belém. La ruta del barco y la deriva van en esquema (la deriva real fue
más larga que la línea recta: unos 1.210 km según la Wikipedia en inglés). Escribe recursos/mapa.json.

  python3 canales/supervivencia/cortos/17-poon-lim/mapa.py
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..', '..', '..', 'geografia', 'kit'))
import geo  # noqa: E402

HUNDIMIENTO = (-38.75, 0.50)
RESCATE = (-47.00, -0.45)          # unos 16 km frente a la costa de Pará, al este de Salinas (aproximado)
BELEM = (-48.49, -1.456)
FORTALEZA = (-38.54, -3.72)
# La ruta del Benlomond, en esquema: del sur (venía de Ciudad del Cabo) hacia Paramaribo.
RUTA = [(-14.0, -24.0), (-22.0, -16.0), (-30.0, -7.6), HUNDIMIENTO]
SIGUE = [HUNDIMIENTO, (-46.0, 3.4), (-55.2, 5.85)]
# La deriva hacia el oeste, en esquema, hasta el punto del rescate.
DERIVA = [HUNDIMIENTO, (-40.2, 0.62), (-41.8, 0.38), (-43.3, 0.12), (-44.6, -0.02), (-45.9, -0.30), RESCATE]


def main():
    P = geo.paises()
    p = geo.Azimutal(-30.0, -2.0, 0.2, 540, 860)
    caja = (-300, -200, 1400, 2100)
    xy = lambda c: [round(v, 1) for v in p(*c)]
    camino = lambda pts: 'M' + 'L'.join(','.join(str(v) for v in xy(c)) for c in pts)
    resto = ''.join(geo.camino([r[0] for r in P[n]], p, 1.5, caja) for n in P if n != "Brazil")
    datos = dict(
        brasil=geo.camino([r[0] for r in P['Brazil']], p, 0.4, caja), resto=resto,
        hundimiento=xy(HUNDIMIENTO), rescate=xy(RESCATE), belem=xy(BELEM), fortaleza=xy(FORTALEZA),
        ruta=camino(RUTA), sigue=camino(SIGUE), deriva=camino(DERIVA),
        et_brasil=xy((-47.5, -7.0)), et_africa=xy((-10.5, 10.5)), et_oceano=xy((-18.0, -5.0)),
        km_recta=round(geo.distancia(HUNDIMIENTO, RESCATE)),
        km_costa=round(min(geo.distancia(HUNDIMIENTO, c) for pol in P['Brazil'] for c in pol[0])))
    json.dump(datos, open(os.path.join(AQUI, 'recursos', 'mapa.json'), 'w'), separators=(',', ':'))
    print(f"hundimiento {datos['hundimiento']} · rescate {datos['rescate']} · Belém {datos['belem']} · "
          f"en línea recta {datos['km_recta']} km · a la costa de Brasil {datos['km_costa']} km")


if __name__ == '__main__':
    main()
