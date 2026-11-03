"""
El mapa de «No es un avión» (Natural Earth 1:10 millones, dominio público), en la pantalla de 1080 × 1920: Australia
entera para situarse y, en la misma proyección, el estrecho de Bass, con la ruta del vuelo de Frederick Valentich del 21 de
octubre de 1978 (Moorabbin, en Melbourne → cabo Otway → isla King, como su plan de vuelo), la zona aproximada del último
contacto (no se conoce su posición exacta) y la isla Flinders, donde apareció en 1983 una pieza de una Cessna 182.
Escribe recursos/mapa.json.

  python3 canales/incidentes/cortos/01-valentich/mapa.py
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..', '..', '..', 'geografia', 'kit'))
import geo  # noqa: E402

MOORABBIN = (145.102, -37.976)    # aeropuerto de Moorabbin (Melbourne), de donde despegó
MELBOURNE = (144.963, -37.814)
OTWAY = (143.511, -38.857)        # cabo Otway: allí dio su posición hacia las 19:00
KING = (143.878, -39.877)         # aeropuerto de la isla King, su destino
FLINDERS = (148.02, -39.98)       # isla Flinders: la pieza de 1983
TASMANIA = (146.6, -41.9)
# La zona del último contacto: sobre el agua, pasado el cabo Otway hacia la isla King (aproximada: no hubo radar).
ZONA = (OTWAY[0] + 0.35 * (KING[0] - OTWAY[0]), OTWAY[1] + 0.35 * (KING[1] - OTWAY[1]))


def main():
    P = geo.paises()
    p = geo.Azimutal(145.75, -39.0, 1.8, 540, 860)
    caja = (-9000, -8000, 2400, 3200)
    xy = lambda c: [round(v, 1) for v in p(*c)]
    aus = P['Australia']
    # Australia continental, Tasmania y las islas, en un solo camino; la isla Flinders aparte para encenderla.
    def cerca(pol, c, km):
        lon = sum(q[0] for q in pol[0]) / len(pol[0]); lat = sum(q[1] for q in pol[0]) / len(pol[0])
        return geo.distancia((lon, lat), c) < km
    flinders = [pol for pol in aus if cerca(pol, FLINDERS, 40)]
    resto = [pol for pol in aus if not cerca(pol, FLINDERS, 40)]
    datos = dict(
        australia=''.join(geo.camino([r[0]], p, 1.6, caja) for r in resto),
        flinders=''.join(geo.camino([r[0]], p, 1.0, caja) for r in flinders),
        moorabbin=xy(MOORABBIN), melbourne=xy(MELBOURNE), otway=xy(OTWAY), king=xy(KING), flinders_c=xy(FLINDERS),
        tasmania=xy(TASMANIA), zona=xy(ZONA), centro_aus=xy((134.0, -26.5)),
        ruta='M' + 'L'.join(','.join(str(v) for v in xy(c)) for c in (MOORABBIN, OTWAY, KING)),
        km_ruta=round(geo.distancia(MOORABBIN, OTWAY) + geo.distancia(OTWAY, KING)),
        km_flinders=round(geo.distancia(ZONA, FLINDERS)))
    json.dump(datos, open(os.path.join(AQUI, 'recursos', 'mapa.json'), 'w'), separators=(',', ':'))
    print(f"ruta {datos['km_ruta']} km · zona→Flinders {datos['km_flinders']} km · islas Flinders: {len(flinders)} · "
          f"Australia {len(datos['australia']) // 1000} kB · moorabbin {datos['moorabbin']} otway {datos['otway']} king "
          f"{datos['king']} flinders {datos['flinders_c']} zona {datos['zona']} centro {datos['centro_aus']}")


if __name__ == '__main__':
    main()
