"""
El mapa de Perú para «La chica que cayó del cielo»: el contorno (Natural Earth 1:10 millones, dominio público), Lima,
Pucallpa y la ruta del vuelo, en la pantalla de 1080 × 1920. Escribe recursos/mapa.json.

  python3 canales/supervivencia/cortos/01-juliane/mapa.py
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..', '..', '..', 'geografia', 'kit'))
import geo  # noqa: E402

LIMA, PUCALLPA = (-77.04, -12.05), (-74.55, -8.38)


def main():
    P = geo.paises()
    proj = geo.Azimutal(-75.5, -10.2, 0.62, 560, 700)
    caja = (-300, -300, 1380, 2220)
    vecinos = ''.join(geo.camino([p[0] for p in P[n]], proj, 2.0, caja) for n in ('Ecuador', 'Colombia', 'Brazil', 'Bolivia', 'Chile'))
    out = dict(peru=geo.camino([p[0] for p in P['Peru']], proj, 1.2, caja), vecinos=vecinos,
               lima=[round(v, 1) for v in proj(*LIMA)], pucallpa=[round(v, 1) for v in proj(*PUCALLPA)],
               km=round(geo.distancia(LIMA, PUCALLPA)))
    json.dump(out, open(os.path.join(AQUI, 'recursos', 'mapa.json'), 'w'), separators=(',', ':'))
    print(f"Lima {out['lima']}, Pucallpa {out['pucallpa']}, {out['km']} km en línea recta")


if __name__ == '__main__':
    main()
