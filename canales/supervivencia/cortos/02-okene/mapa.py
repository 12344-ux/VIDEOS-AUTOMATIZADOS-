"""
El mapa de Nigeria para «60 horas bajo el mar»: el contorno (Natural Earth 1:10 millones, dominio público), los países
vecinos y el punto aproximado del naufragio frente al delta del Níger, en la pantalla de 1080 × 1920. Escribe
recursos/mapa.json.

  python3 canales/supervivencia/cortos/02-okene/mapa.py
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..', '..', '..', 'geografia', 'kit'))
import geo  # noqa: E402

# El Jascon-4 trabajaba junto a una plataforma de Chevron frente a la costa del delta: el punto es aproximado (las
# fuentes no dan la posición), mar adentro frente a Escravos.
NAUFRAGIO = (4.75, 5.45)


def main():
    P = geo.paises()
    proj = geo.Azimutal(7.0, 7.6, 0.62, 560, 740)
    caja = (-300, -300, 1380, 2220)
    vecinos = ''.join(geo.camino([p[0] for p in pols], proj, 2.0, caja) for n, pols in P.items() if n != 'Nigeria')
    out = dict(nigeria=geo.camino([p[0] for p in P['Nigeria']], proj, 1.2, caja), vecinos=vecinos,
               naufragio=[round(v, 1) for v in proj(*NAUFRAGIO)])
    json.dump(out, open(os.path.join(AQUI, 'recursos', 'mapa.json'), 'w'), separators=(',', ':'))
    print(f"naufragio en {out['naufragio']}; {len(out['nigeria']) // 1000} kB Nigeria, {len(vecinos) // 1000} kB vecinos")


if __name__ == '__main__':
    main()
