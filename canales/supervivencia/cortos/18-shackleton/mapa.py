"""
El mapa de «Atrapados en el hielo» (Natural Earth 1:10 millones, dominio público), en la pantalla de 1080 × 1920: el mar de
Weddell, la península Antártica, la isla Elefante, Georgia del Sur, las Malvinas y la punta de Sudamérica en una sola
proyección. Posiciones de la Wikipedia en inglés («Imperial Trans-Antarctic Expedition»): el Endurance quedó parado en el
hielo en 76°34′ S, 31°30′ O (enero de 1915), lo abandonaron en 69°05′ S, 51°30′ O (27 de octubre de 1915) y su pecio
apareció en 2022 a 3.008 m de profundidad, unos 7 km al sur de la posición de Worsley (68°39′ S, 52°26′ O). Los botes
llegaron a la isla Elefante (Punta Wild, 61°06′ S, 54°52′ O) el 15 de abril de 1916; el James Caird, a la bahía Rey Haakon
(Georgia del Sur) el 10 de mayo; y la travesía a pie acabó en Stromness. El Yelcho salió de Punta Arenas el 25 de agosto y
llegó a la isla el 30. La deriva y las rutas van en esquema. Escribe recursos/mapa.json.

  python3 canales/supervivencia/cortos/18-shackleton/mapa.py
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..', '..', '..', 'geografia', 'kit'))
import geo  # noqa: E402

ATRAPADO = (-31.50, -76.57)
ABANDONO = (-51.50, -69.08)
HUNDIDO = (-52.33, -68.74)         # el pecio (Endurance22, 2022)
ELEFANTE = (-54.87, -61.10)        # Punta Wild
HAAKON = (-37.30, -54.17)          # bahía Rey Haakon, Georgia del Sur
STROMNESS = (-36.71, -54.16)
PUNTA_ARENAS = (-70.91, -53.16)
# La deriva del barco y del campamento, en esquema: del punto donde quedó parado, al sur y al oeste en el invierno, y al
# norte hasta abandonarlo; después, el hielo hacia el norte y los botes hasta la isla Elefante.
DERIVA = [ATRAPADO, (-33.5, -76.95), (-38.0, -75.8), (-42.2, -74.3), (-46.0, -72.6), (-49.0, -70.9), ABANDONO, HUNDIDO,
          (-52.8, -67.0), (-53.0, -65.0), (-52.6, -63.0), (-53.6, -62.0), ELEFANTE]
CAIRD = [ELEFANTE, (-48.5, -59.4), (-43.0, -57.2), (-39.5, -55.4), HAAKON]
YELCHO = [PUNTA_ARENAS, (-68.0, -55.6), (-63.0, -58.0), (-58.5, -59.9), ELEFANTE]
GRYTVIKEN = (-36.51, -54.28)
STANLEY = (-57.85, -51.69)
# El plan: cruzar a pie de la bahía Vahsel al estrecho de McMurdo por el polo (en esquema, en línea recta).
VAHSEL = (-35.0, -77.8)
POLO = (0.0, -90.0)
MCMURDO = (166.0, -77.6)
# La entrada en el mar de Weddell (5 de diciembre de 1914 – enero de 1915), en esquema.
ENTRADA = [GRYTVIKEN, (-27.0, -59.5), (-20.0, -66.0), (-21.5, -72.0), (-26.5, -75.4), ATRAPADO]
# Los tres intentos que paró el hielo (en esquema): el Southern Sky desde Georgia del Sur (lo paró a unos 110 km), el
# Instituto de Pesca N.º 1 (de Uruguay) desde las Malvinas y el Emma desde Punta Arenas.
INTENTOS = [[(-36.6, -54.0), (-44.0, -57.6), (-51.6, -60.2)],
            [STANLEY, (-56.6, -55.6), (-55.6, -59.4)],
            [PUNTA_ARENAS, (-67.5, -56.0), (-62.5, -58.6), (-58.4, -60.1)]]
# La travesía de Georgia del Sur, en esquema: de la bahía Rey Haakon a Stromness por el interior.
TRAVESIA = [HAAKON, (-37.12, -54.22), (-36.95, -54.24), (-36.83, -54.19), STROMNESS]


def main():
    P = geo.paises()
    p = geo.Azimutal(-53.0, -64.0, 0.40, 560, 900)
    caja = (-400, -300, 1500, 2300)
    xy = lambda c: [round(v, 1) for v in p(*c)]
    camino = lambda pts: 'M' + 'L'.join(','.join(str(v) for v in xy(c)) for c in pts)
    datos = dict(
        antartida=geo.camino([r[0] for r in P['Antarctica']], p, 0.8, caja),
        georgia=geo.camino([r[0] for r in P['S. Geo. and the Is.']], p, 0.3, caja),
        chile=geo.camino([r[0] for r in P['Chile']], p, 1.0, caja),
        resto=''.join(geo.camino([r[0] for r in P[n]], p, 1.2, caja) for n in ('Argentina', 'Falkland Is.')),
        atrapado=xy(ATRAPADO), abandono=xy(ABANDONO), hundido=xy(HUNDIDO), elefante=xy(ELEFANTE), haakon=xy(HAAKON),
        stromness=xy(STROMNESS), punta_arenas=xy(PUNTA_ARENAS),
        deriva=camino(DERIVA), caird=camino(CAIRD), yelcho=camino(YELCHO), ruta_entrada=camino(ENTRADA), travesia=camino(TRAVESIA),
        plan=camino([VAHSEL, POLO, MCMURDO]), intentos=[camino(c) for c in INTENTOS], fin_intentos=[xy(c[-1]) for c in INTENTOS],
        grytviken=xy(GRYTVIKEN), stanley=xy(STANLEY), vahsel=xy(VAHSEL), polo=xy(POLO), mcmurdo=xy(MCMURDO),
        et_weddell=xy((-40.0, -72.0)), et_antartida=xy((-30.0, -82.5)),
        km_caird=round(geo.distancia(ELEFANTE, HAAKON)), km_yelcho=round(geo.distancia(PUNTA_ARENAS, ELEFANTE)))
    json.dump(datos, open(os.path.join(AQUI, 'recursos', 'mapa.json'), 'w'), separators=(',', ':'))
    print(f"atrapado {datos['atrapado']} · hundido {datos['hundido']} · Elefante {datos['elefante']} · Haakon {datos['haakon']} · "
          f"Punta Arenas {datos['punta_arenas']} · Elefante–Georgia {datos['km_caird']} km en línea recta · "
          f"Punta Arenas–Elefante {datos['km_yelcho']} km · tamaños {[len(datos[k]) for k in ('antartida', 'georgia', 'resto')]}")


if __name__ == '__main__':
    main()
