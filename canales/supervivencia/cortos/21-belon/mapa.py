"""
El mapa de «Lo imposible» (Natural Earth 1:10 millones, dominio público), en la pantalla de 1080 × 1920: el norte de
Sumatra, el mar de Andamán y la costa de Tailandia. El terremoto del 26 de diciembre de 2004 frente a Sumatra (epicentro en
3,316° N, 95,854° E, según la Wikipedia en inglés) levantó el tsunami que arrasó Khao Lak, en la provincia de Phang Nga, unos
80 km al norte de Phuket: 3.950 muertos confirmados, y quizá más de 4.500 («Effect of the 2004 Indian Ocean earthquake on
Thailand»). Las ondas van en esquema. Escribe recursos/mapa.json.

  python3 canales/supervivencia/cortos/21-belon/mapa.py
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..', '..', '..', 'geografia', 'kit'))
import geo  # noqa: E402

EPICENTRO = (95.854, 3.316)
KHAO_LAK = (98.25, 8.64)
PHUKET = (98.39, 7.88)


def main():
    P = geo.paises()
    p = geo.Azimutal(97.0, 6.5, 0.6, 540, 900)
    caja = (-300, -200, 1400, 2200)
    xy = lambda c: [round(v, 2) for v in p(*c)]
    anillos = lambda nombres: [r[0] for n in nombres for r in P[n]]
    datos = dict(
        tailandia=geo.camino(anillos(['Thailand']), p, 0.8, caja),
        resto=geo.camino(anillos(['Myanmar', 'Malaysia', 'Indonesia', 'Cambodia']), p, 2.0, caja),
        epicentro=xy(EPICENTRO), khao_lak=xy(KHAO_LAK), phuket=xy(PHUKET),
        et_tailandia=xy((100.6, 13.2)), et_sumatra=xy((98.6, 2.2)), et_mar=xy((95.4, 9.6)),
        km=round(geo.distancia(EPICENTRO, KHAO_LAK)), px_km=0.6)
    json.dump(datos, open(os.path.join(AQUI, 'recursos', 'mapa.json'), 'w'), separators=(',', ':'))
    print(f"epicentro {datos['epicentro']} · Khao Lak {datos['khao_lak']} · Phuket {datos['phuket']} · "
          f"epicentro–Khao Lak {datos['km']} km · tamaños {[len(datos[k]) for k in ('tailandia', 'resto')]}")


if __name__ == '__main__':
    main()
