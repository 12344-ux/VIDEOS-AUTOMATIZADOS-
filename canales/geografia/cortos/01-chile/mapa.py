"""
Los mapas de «¿Por qué Chile es tan largo?» en la pantalla de 1080 × 1920: caminos SVG de Natural Earth (1:10 millones,
dominio público) en proyecciones azimutales equidistantes locales, todas a la escala que pide cada plano. Escribe
recursos/mapa.json.

  python3 canales/geografia/cortos/01-chile/mapa.py

Planos:
  sa      Sudamérica a 0,25 px/km: Chile entero (4.274 km), a la izquierda, de y 180 a 1250; la pregunta, a su derecha
  eu      Europa a la misma escala, con el contorno de Chile encima: su punta norte en Oslo (tamaño real)
  centro  el centro de Chile a 1,6 px/km: la franja entre el Pacífico y los Andes, y el punto más estrecho (31,6° S)
  norte   el norte a 0,6 px/km: lo que era de Perú y de Bolivia hasta 1879 (Chile llegaba al paralelo 24° S)
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..', '..', 'kit'))
import geo  # noqa: E402

CAJA = (-200, -200, 1280, 2120)
LOA = -21.45      # el río Loa: hasta 1879, al norte era Perú (Tarapacá) y al sur la costa de Bolivia (aprox.)
LIMITE = -24.0    # la frontera de Chile y Bolivia antes de la guerra (tratados de 1866 y 1874)


def caminos(paises, nombres, proj, minimo=1.2):
    return {n: geo.camino([a for p in paises[n] for a in p[:1]], proj, minimo, CAJA) for n in nombres}


def tierra(paises, proj, fuera=(), minimo=2.5):
    return ''.join(geo.camino([p[0] for p in pols], proj, minimo, CAJA) for n, pols in paises.items() if n not in fuera)


def main():
    P = geo.paises()
    chile = P['Chile']
    norte, sur = geo.extremos(chile)
    vecinos = ['Argentina', 'Bolivia', 'Peru', 'Brazil', 'Paraguay', 'Uruguay']
    out = {}

    # Sudamérica: el centro del contorno de Chile, a un tercio de la anchura; la punta norte, en y 180.
    k = 0.25
    sa = geo.Azimutal(-64.0, -36.7, k, 290, 0)
    dy = 180 - sa(*norte)[1]
    sa = geo.Azimutal(-64.0, -36.7, k, 290, dy)
    estrecho = [(lon, -31.6) for lon in geo.cortes(geo.principal(chile)[0], -31.6)[:2]]
    out['sa'] = dict(tierra=tierra(P, sa, ['Chile'] + vecinos), **caminos(P, ['Chile'] + vecinos, sa),
                     norte=sa(*norte), sur=sa(*sur), estrecho=[sa(*p) for p in estrecho],
                     bolivia=sa(-64.7, -16.7), largo=round(geo.distancia(norte, sur)))

    # Europa a la misma escala; Chile, en la proyección de Sudamérica y desplazado hasta que su punta norte cae en Oslo.
    eu = geo.Azimutal(12.0, 41.0, k, 520, 0)
    oslo = (10.75, 59.91)
    dy = 230 - eu(*oslo)[1]
    eu = geo.Azimutal(12.0, 41.0, k, 520, dy)
    ox, oy = eu(*oslo)
    nx, ny = sa(*norte)
    desplazado = lambda lon, lat: (sa(lon, lat)[0] - nx + ox, sa(lon, lat)[1] - ny + oy)  # noqa: E731
    sur_eu = desplazado(*sur)
    out['eu'] = dict(tierra=tierra(P, eu), chile=geo.camino([p[0] for p in chile], desplazado, 1.2, CAJA),
                     oslo=(ox, oy), sur=sur_eu, desde=geo.camino([p[0] for p in chile], sa, 1.2, CAJA))

    # El centro: la franja, los Andes (la frontera con Argentina) y el punto más estrecho.
    c = geo.Azimutal(-70.6, -32.0, 1.6, 560, 820)
    out['centro'] = dict(tierra=tierra(P, c, ['Chile', 'Argentina']), **caminos(P, ['Chile', 'Argentina'], c),
                         frontera=''.join(geo.linea(l, c) for l in geo.fronteras('Chile', 'Argentina')),
                         estrecho=[c(*p) for p in estrecho], escala=1.6)

    # El norte: Chile llegaba al 24° S; lo de arriba era de Bolivia (la costa) y de Perú (Tarapacá y Arica).
    n = geo.Azimutal(-69.0, -22.0, 0.6, 560, 760)
    principal = geo.principal(chile)[0]
    antes = geo.recorta(principal, LIMITE, norte=False)
    ganado = geo.recorta(principal, LIMITE, norte=True)
    ex_bolivia = geo.recorta(ganado, LOA, norte=False)
    ex_peru = geo.recorta(ganado, LOA, norte=True)
    out['norte'] = dict(tierra=tierra(P, n, ['Chile', 'Bolivia', 'Peru', 'Argentina']), **caminos(P, ['Bolivia', 'Peru', 'Argentina'], n),
                        antes=geo.camino([antes], n, 1.2, CAJA), ganado=geo.camino([ganado], n, 1.2, CAJA),
                        ex_bolivia=geo.camino([ex_bolivia], n, 1.2, CAJA), ex_peru=geo.camino([ex_peru], n, 1.2, CAJA),
                        y24=n(-70.6, LIMITE)[1], ytope=n(*norte)[1], km=round(geo.distancia((-70.4, LIMITE), (-70.4, norte[1]))),
                        x_costa=n(-70.6, LIMITE)[0], x_frontera=n(-67.6, LIMITE)[0])

    def redondea(x):
        if isinstance(x, float):
            return round(x, 1)
        if isinstance(x, (list, tuple)):
            return [redondea(y) for y in x]
        if isinstance(x, dict):
            return {a: redondea(b) for a, b in x.items()}
        return x

    ruta = os.path.join(AQUI, 'recursos', 'mapa.json')
    json.dump(redondea(out), open(ruta, 'w'), ensure_ascii=False, separators=(',', ':'))
    print(f'{ruta}: {os.path.getsize(ruta) // 1024} KB; largo {out["sa"]["largo"]} km; Chile en sa de y {out["sa"]["norte"][1]:.0f} '
          f'a {out["sa"]["sur"][1]:.0f}; en eu, de Oslo ({oy:.0f}) a {sur_eu[1]:.0f}; del 24° S a la punta norte, {out["norte"]["km"]} km')


if __name__ == '__main__':
    main()
