"""
El mapa de «El ovni Tic Tac» (Natural Earth 1:10 millones, dominio público), en la pantalla de 1080 × 1920: la costa de
California y de Baja California y, frente a ella, las posiciones del 14 de noviembre de 2004 según el relato de David
Fravor (declaración ante el Congreso, 2023) y la CBS: la zona del encuentro, a unas 100 millas (161 km) al suroeste de San
Diego; el punto de encuentro de los cazas (CAP), a unas 60 millas (97 km) al este; y el grupo del Nimitz, unas 40 millas al
norte del punto de encuentro. Son posiciones en esquema: las coordenadas exactas no se han publicado.
Escribe recursos/mapa.json.

  python3 canales/incidentes/cortos/02-tictac/mapa.py
"""
import json
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..', '..', '..', 'geografia', 'kit'))
import geo  # noqa: E402

SAN_DIEGO = (-117.161, 32.716)
LOS_ANGELES = (-118.244, 34.052)


def desplaza(c, km_este, km_norte):
    """Un punto a tantos km al este y al norte de otro (vale para distancias de cientos de km)."""
    lat = c[1] + km_norte / 111.2
    return (c[0] + km_este / (111.32 * math.cos(math.radians((c[1] + lat) / 2))), lat)


ENCUENTRO = desplaza(SAN_DIEGO, -161 / math.sqrt(2), -161 / math.sqrt(2))   # 100 millas al suroeste
CAP = desplaza(ENCUENTRO, 97, 0)                                              # 60 millas al este
NIMITZ = desplaza(CAP, 0, 64)                                                  # 40 millas al norte del CAP


def main():
    P = geo.paises()
    p = geo.Azimutal(-117.6, 32.4, 3.0, 540, 860)
    caja = (-3000, -3000, 4000, 4500)
    xy = lambda c: [round(v, 1) for v in p(*c)]
    datos = dict(
        eeuu=geo.camino([r[0] for r in P['United States of America']], p, 1.5, caja),
        mexico=geo.camino([r[0] for r in P['Mexico']], p, 1.5, caja),
        san_diego=xy(SAN_DIEGO), los_angeles=xy(LOS_ANGELES), encuentro=xy(ENCUENTRO), cap=xy(CAP), nimitz=xy(NIMITZ),
        km_salto=round(geo.distancia(ENCUENTRO, CAP)), km_sd=round(geo.distancia(SAN_DIEGO, ENCUENTRO)))
    json.dump(datos, open(os.path.join(AQUI, 'recursos', 'mapa.json'), 'w'), separators=(',', ':'))
    print(f"encuentro {datos['encuentro']} ({datos['km_sd']} km de San Diego) · CAP {datos['cap']} ({datos['km_salto']} km) · "
          f"Nimitz {datos['nimitz']} · San Diego {datos['san_diego']} · Los Ángeles {datos['los_angeles']} · "
          f"EE. UU. {len(datos['eeuu']) // 1000} kB · México {len(datos['mexico']) // 1000} kB")


if __name__ == '__main__':
    main()
