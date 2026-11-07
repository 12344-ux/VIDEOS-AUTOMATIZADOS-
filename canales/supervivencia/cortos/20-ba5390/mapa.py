"""
El mapa de «Fuera del avión» (Natural Earth 1:10 millones, dominio público), en la pantalla de 1080 × 1920: Inglaterra, el
canal de la Mancha, Francia y España en una sola proyección. Vuelo 5390 de British Airways, 10 de junio de 1990
(Wikipedia en inglés y en español, «British Airways Flight 5390»): despegó del aeropuerto de Birmingham a las 08:20 hacia
Málaga; a las 08:33, a unos 5.300 m sobre Didcot (Oxfordshire), se soltó el parabrisas del capitán; aterrizó en Southampton
a las 08:55. La ruta prevista y el desvío van en esquema. Escribe recursos/mapa.json.

  python3 canales/supervivencia/cortos/20-ba5390/mapa.py
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..', '..', '..', 'geografia', 'kit'))
import geo  # noqa: E402

BIRMINGHAM = (-1.748, 52.454)      # el aeropuerto
DIDCOT = (-1.243, 51.608)
SOUTHAMPTON = (-1.357, 50.950)     # el aeropuerto
MALAGA = (-4.499, 36.675)          # el aeropuerto
# Lo que voló, en esquema: al sur hasta Didcot; después, el descenso y el desvío a Southampton.
VUELO = [BIRMINGHAM, (-1.60, 52.20), (-1.40, 51.90), DIDCOT]
DESVIO = [DIDCOT, (-1.30, 51.45), (-1.42, 51.22), (-1.40, 51.06), SOUTHAMPTON]
# La ruta prevista hasta Málaga (en esquema): por el canal de la Mancha, la Bretaña y el golfo de Vizcaya.
RUTA = [BIRMINGHAM, (-1.65, 51.60), (-1.80, 50.40), (-2.60, 48.80), (-3.40, 46.00), (-3.90, 43.20), (-4.20, 40.20), MALAGA]


def main():
    P = geo.paises()
    p = geo.Azimutal(-2.5, 45.0, 0.5, 540, 960)
    caja = (-600, -300, 1700, 2300)
    xy = lambda c: [round(v, 2) for v in p(*c)]
    camino = lambda pts: 'M' + 'L'.join(','.join(str(v) for v in xy(c)) for c in pts)
    anillos = lambda nombres: [r[0] for n in nombres for r in P[n]]
    datos = dict(
        uk=geo.camino(anillos(['United Kingdom', 'Isle of Man', 'Jersey', 'Guernsey']), p, 0.25, caja),
        francia=geo.camino(anillos(['France']), p, 0.6, caja),
        espana=geo.camino(anillos(['Spain', 'Gibraltar', 'Andorra']), p, 0.6, caja),
        resto=geo.camino(anillos(['Ireland', 'Portugal', 'Belgium', 'Netherlands', 'Morocco']), p, 1.5, caja),
        birmingham=xy(BIRMINGHAM), didcot=xy(DIDCOT), southampton=xy(SOUTHAMPTON), malaga=xy(MALAGA),
        ruta=camino(RUTA), vuelo=camino(VUELO), desvio=camino(DESVIO),
        et_inglaterra=xy((-1.2, 52.9)), et_francia=xy((2.4, 47.0)), et_espana=xy((-3.6, 39.9)),
        km_ruta=round(sum(geo.distancia(a, b) for a, b in zip(RUTA, RUTA[1:]))),
        km_didcot=round(geo.distancia(BIRMINGHAM, DIDCOT)), km_desvio=round(geo.distancia(DIDCOT, SOUTHAMPTON)))
    json.dump(datos, open(os.path.join(AQUI, 'recursos', 'mapa.json'), 'w'), separators=(',', ':'))
    print(f"Birmingham {datos['birmingham']} · Didcot {datos['didcot']} · Southampton {datos['southampton']} · Málaga {datos['malaga']} · "
          f"ruta prevista {datos['km_ruta']} km · Birmingham–Didcot {datos['km_didcot']} km · Didcot–Southampton {datos['km_desvio']} km "
          f"en línea recta · tamaños {[len(datos[k]) for k in ('uk', 'francia', 'espana', 'resto')]}")


if __name__ == '__main__':
    main()
