"""
El mapa de «40 días en la selva» (Natural Earth 1:10 millones, dominio público), en la pantalla de 1080 × 1920: Colombia
entera con sus vecinos, Bogotá para orientarse, y la ruta de la avioneta de Araracuara a San José del Guaviare con el
punto donde cayó (la posición del accidente, de Wikipedia: 00°54′18,5″ N, 72°24′44,1″ O). Escribe recursos/mapa.json.

  python3 canales/supervivencia/cortos/09-ninos-selva/mapa.py
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..', '..', '..', 'geografia', 'kit'))
import geo  # noqa: E402

BOGOTA = (-74.072, 4.711)
ARARACUARA = (-72.398, -0.601)      # el aeródromo de Araracuara (Caquetá)
SAN_JOSE = (-72.645, 2.572)         # San José del Guaviare
ACCIDENTE = (-72.4123, 0.9051)      # Solano (Caquetá)


def main():
    P = geo.paises()
    caja = (-300, -300, 1380, 2220)
    # Colombia entera a 0,8 px/km: unos 1.070 × 1.490 px; el centro, un poco al sur para dejar sitio arriba a los rótulos.
    p = geo.Azimutal(-73.1, 4.0, 0.8, 540, 980)
    vecinos = [n for n in ('Venezuela', 'Brazil', 'Peru', 'Ecuador', 'Panama') if n in P]
    datos = dict(
        colombia=geo.camino([r[0] for r in P['Colombia']], p, 1.0, caja),
        vecinos=''.join(geo.camino([r[0] for r in P[n]], p, 1.0, caja) for n in vecinos),
        bogota=[round(v, 1) for v in p(*BOGOTA)], araracuara=[round(v, 1) for v in p(*ARARACUARA)],
        sanjose=[round(v, 1) for v in p(*SAN_JOSE)], accidente=[round(v, 1) for v in p(*ACCIDENTE)],
        km=round(geo.distancia(ARARACUARA, SAN_JOSE)), km_accidente=round(geo.distancia(ARARACUARA, ACCIDENTE)))
    json.dump(datos, open(os.path.join(AQUI, 'recursos', 'mapa.json'), 'w'), separators=(',', ':'))
    print(f"Araracuara {datos['araracuara']} → San José {datos['sanjose']}: {datos['km']} km; el accidente, a {datos['km_accidente']} km "
          f"de Araracuara, en {datos['accidente']}; Bogotá en {datos['bogota']}")


if __name__ == '__main__':
    main()
