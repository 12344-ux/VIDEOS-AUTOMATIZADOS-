"""
El mapa de «72 días en los Andes» (Natural Earth 1:10 millones, dominio público), en la pantalla de 1080 × 1920: Uruguay,
Argentina y Chile en una sola proyección, para que la cámara vaya del vuelo (Montevideo → Mendoza → la cordillera) al
lugar del accidente (el Glaciar de las Lágrimas, en Argentina, junto a la frontera) y a la caminata de Nando Parrado y
Roberto Canessa hasta el valle chileno donde encontraron al arriero Sergio Catalán. La caminata va en esquema: unos 60 km
en diez días (subieron hacia el oeste y bajaron por el valle del río Azufre). Escribe recursos/mapa.json.

  python3 canales/supervivencia/cortos/15-andes/mapa.py
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..', '..', '..', 'geografia', 'kit'))
import geo  # noqa: E402

MONTEVIDEO = (-56.165, -34.905)
MENDOZA = (-68.845, -32.890)
SANTIAGO = (-70.650, -33.450)
GLACIAR = (-70.286, -34.765)       # Glaciar de las Lágrimas (Malargüe, Mendoza), a unos 3.600 m
ENCUENTRO = (-70.600, -34.830)     # el valle del río Azufre (Chile), donde los vio el arriero: aproximado
# La caminata, en esquema: hacia el oeste, por la cumbre, y abajo por el valle hasta el río.
CAMINO = [GLACIAR, (-70.33, -34.79), (-70.38, -34.80), (-70.44, -34.83), (-70.51, -34.84), ENCUENTRO]
# La ruta del vuelo, en esquema: de Montevideo a Mendoza (donde hizo noche) y de allí al sur y al oeste, a la cordillera.
VUELO = [MONTEVIDEO, MENDOZA, (-69.6, -34.0), GLACIAR]


def main():
    P = geo.paises()
    p = geo.Azimutal(-64.5, -34.0, 0.62, 540, 860)
    caja = (-2600, -2600, 3600, 4400)
    xy = lambda c: [round(v, 1) for v in p(*c)]
    camino = lambda pts: 'M' + 'L'.join(','.join(str(v) for v in xy(c)) for c in pts)
    datos = dict(
        argentina=geo.camino([r[0] for r in P['Argentina']], p, 0.6, caja),
        chile=geo.camino([r[0] for r in P['Chile']], p, 0.6, caja),
        uruguay=geo.camino([r[0] for r in P['Uruguay']], p, 0.6, caja),
        resto=''.join(geo.camino([r[0] for r in P[n]], p, 1.0, caja) for n in ('Brazil', 'Paraguay', 'Bolivia') if n in P),
        montevideo=xy(MONTEVIDEO), mendoza=xy(MENDOZA), santiago=xy(SANTIAGO), glaciar=xy(GLACIAR), encuentro=xy(ENCUENTRO),
        vuelo=camino(VUELO), caminata=camino(CAMINO),
        km_caminata=round(sum(geo.distancia(a, b) for a, b in zip(CAMINO, CAMINO[1:]))),
        km_vuelo=round(sum(geo.distancia(a, b) for a, b in zip(VUELO, VUELO[1:]))))
    json.dump(datos, open(os.path.join(AQUI, 'recursos', 'mapa.json'), 'w'), separators=(',', ':'))
    print(f"glaciar {datos['glaciar']} · encuentro {datos['encuentro']} · caminata en esquema {datos['km_caminata']} km · "
          f"Montevideo {datos['montevideo']} · Mendoza {datos['mendoza']} · Santiago {datos['santiago']}")


if __name__ == '__main__':
    main()
