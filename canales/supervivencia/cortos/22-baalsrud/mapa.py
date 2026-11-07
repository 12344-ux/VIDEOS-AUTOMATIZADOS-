"""
El mapa de «El duodécimo hombre» (Natural Earth 1:10 millones, dominio público), en la pantalla de 1080 × 1920: el mar del
Norte y la costa de Noruega hasta Troms, con Suecia y Finlandia. Operación Martin (Wikipedia en inglés y en español): en
marzo de 1943 el pesquero Brattholm llevó a doce noruegos de las Shetland a Toftefjord (isla de Rebbenesøya, al norte de
Tromsø); el 29 de marzo lo atacó un barco alemán. Jan Baalsrud huyó por los fiordos de Lyngen y Manndalen y unos sami lo
llevaron en trineo, por Finlandia (Kilpisjärvi), hasta Suecia, a unos dos meses del ataque. Las rutas van en esquema.
Escribe recursos/mapa.json.

  python3 canales/supervivencia/cortos/22-baalsrud/mapa.py
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..', '..', '..', 'geografia', 'kit'))
import geo  # noqa: E402

SHETLAND = (-1.28, 60.15)          # Lerwick
TOFTEFJORD = (18.55, 70.08)        # Rebbenesøya
TROMSO = (18.96, 69.65)
LYNGEN = (20.15, 69.45)            # Furuflaten, en el fiordo de Lyngen
MANNDALEN = (20.55, 69.50)
KILPISJARVI = (20.80, 69.05)       # Finlandia, junto a la frontera sueca
BODEN = (21.69, 65.83)
# El viaje del pesquero, en esquema: de las Shetland por la costa noruega hasta Toftefjord.
MISION = [SHETLAND, (3.0, 62.5), (8.5, 65.6), (13.0, 68.3), (16.8, 69.8), TOFTEFJORD]
# La huida, en esquema: de Toftefjord al fiordo de Lyngen, Manndalen y el altiplano, y en trineo hasta la frontera.
HUIDA = [TOFTEFJORD, (19.2, 69.95), (19.7, 69.62), LYNGEN, (20.35, 69.42), MANNDALEN, (20.75, 69.3), KILPISJARVI]


def main():
    P = geo.paises()
    p = geo.Azimutal(14.0, 66.0, 0.42, 540, 900)
    caja = (-300, -300, 1400, 2200)
    xy = lambda c: [round(v, 2) for v in p(*c)]
    camino = lambda pts: 'M' + 'L'.join(','.join(str(v) for v in xy(c)) for c in pts)
    anillos = lambda nombres: [r[0] for n in nombres for r in P[n]]
    datos = dict(
        noruega=geo.camino(anillos(['Norway']), p, 0.5, caja),
        suecia=geo.camino(anillos(['Sweden']), p, 0.8, caja),
        resto=geo.camino(anillos(['Finland', 'United Kingdom', 'Denmark', 'Faeroe Is.']), p, 1.5, caja),
        shetland=xy(SHETLAND), toftefjord=xy(TOFTEFJORD), tromso=xy(TROMSO), lyngen=xy(LYNGEN), manndalen=xy(MANNDALEN),
        kilpisjarvi=xy(KILPISJARVI), boden=xy(BODEN), mision=camino(MISION), huida=camino(HUIDA),
        et_noruega=xy((12.5, 65.2)), et_suecia=xy((17.0, 64.4)), et_finlandia=xy((25.5, 66.8)),
        et_noruega_n=xy((18.3, 69.25)), et_suecia_n=xy((19.9, 68.45)), et_finlandia_n=xy((22.6, 69.15)),
        km_mision=round(sum(geo.distancia(a, b) for a, b in zip(MISION, MISION[1:]))),
        km_huida=round(sum(geo.distancia(a, b) for a, b in zip(HUIDA, HUIDA[1:]))))
    json.dump(datos, open(os.path.join(AQUI, 'recursos', 'mapa.json'), 'w'), separators=(',', ':'))
    print(f"Shetland {datos['shetland']} · Toftefjord {datos['toftefjord']} · Lyngen {datos['lyngen']} · "
          f"Kilpisjärvi {datos['kilpisjarvi']} · misión {datos['km_mision']} km · huida {datos['km_huida']} km en esquema · "
          f"tamaños {[len(datos[k]) for k in ('noruega', 'suecia', 'resto')]}")


if __name__ == '__main__':
    main()
