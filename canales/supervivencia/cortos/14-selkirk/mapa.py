"""
El mapa de «El verdadero Robinson Crusoe» (Natural Earth 1:10 millones, dominio público), en la pantalla de 1080 × 1920:
la costa del Pacífico de Sudamérica, de Panamá a Chile, en una sola proyección para que la cámara pueda ir de la isla de
Selkirk (Más a Tierra, hoy Isla Robinson Crusoe) a la isla de Malpelo (Colombia), cerca de donde se hundió el Cinque Ports.
Escribe recursos/mapa.json.

  python3 canales/supervivencia/cortos/14-selkirk/mapa.py
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..', '..', '..', 'geografia', 'kit'))
import geo  # noqa: E402

ISLA = (-78.83, -33.64)          # Más a Tierra (Juan Fernández), hoy Isla Robinson Crusoe
VALPARAISO = (-71.62, -33.05)
MALPELO = (-81.61, 4.0)          # isla de Malpelo (Colombia)
# El rumbo del barco hacia el norte, mar adentro (esquema: no se conoce su derrota exacta).
RUMBO = [ISLA, (-79.6, -29.5), (-81.2, -23.0), (-82.6, -15.5), (-83.4, -8.0), (-83.0, -1.5), MALPELO]


def main():
    P = geo.paises()
    caja = (-400, -400, 1480, 2320)
    # Toda la costa, de Panamá a Chile central, a 0,3 px/km (unos 1.350 px de alto); la cámara de la escena acerca.
    p = geo.Azimutal(-76.5, -14.8, 0.3, 560, 960)
    resto = [n for n in ('Ecuador', 'Peru', 'Bolivia', 'Argentina', 'Brazil', 'Panama', 'Venezuela', 'Paraguay', 'Costa Rica')
             if n in P]
    xy = lambda c: [round(v, 1) for v in p(*c)]
    datos = dict(
        chile=geo.camino([r[0] for r in P['Chile']], p, 1.0, caja),
        colombia=geo.camino([r[0] for r in P['Colombia']], p, 1.0, caja),
        resto=''.join(geo.camino([r[0] for r in P[n]], p, 1.0, caja) for n in resto),
        isla=xy(ISLA), valparaiso=xy(VALPARAISO), malpelo=xy(MALPELO),
        rumbo='M' + 'L'.join(','.join(str(v) for v in xy(c)) for c in RUMBO),
        km=round(geo.distancia(ISLA, VALPARAISO)), km_rumbo=round(sum(geo.distancia(a, b) for a, b in zip(RUMBO, RUMBO[1:]))))
    json.dump(datos, open(os.path.join(AQUI, 'recursos', 'mapa.json'), 'w'), separators=(',', ':'))
    print(f"isla {datos['isla']} · Valparaíso {datos['valparaiso']} ({datos['km']} km) · Malpelo {datos['malpelo']} "
          f"· rumbo {datos['km_rumbo']} km")


if __name__ == '__main__':
    main()
