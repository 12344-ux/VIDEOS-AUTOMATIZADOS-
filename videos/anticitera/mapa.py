"""
Costa del Mediterráneo oriental para graficos/mapa.html, sacada de Natural Earth (tierra a 1:50 millones,
dominio público) en el TopoJSON de world-atlas (jsDelivr). Escribe graficos/datos/costa.txt: un camino SVG
en la proyección del mapa (equirectangular con la escala horizontal de la latitud 38°), en el que el cuadro
de 1920 × 1080 va de 9° a 31° de longitud este.

  python3 -I videos/anticitera/mapa.py salidas/anticitera/datos/land-50m.json videos/anticitera/graficos/datos/costa.txt
"""
import json
import math
import sys

LON0, LAT0, K = 20.0, 37.9, 1920 / 22.0 / math.cos(math.radians(38))   # px por grado de latitud
CX, CY = 960, 540


def proyecta(lon, lat):
    return CX + (lon - LON0) * K * math.cos(math.radians(38)), CY - (lat - LAT0) * K


def main():
    d = json.load(open(sys.argv[1]))
    sx, sy = d['transform']['scale']
    tx, ty = d['transform']['translate']
    arcos = []
    for arco in d['arcs']:   # coordenadas cuantizadas y en diferencias
        x = y = 0
        pts = []
        for dx, dy in arco:
            x, y = x + dx, y + dy
            pts.append((x * sx + tx, y * sy + ty))
        arcos.append(pts)

    def anillo(indices):
        pts = []
        for i in indices:
            a = arcos[i] if i >= 0 else arcos[~i][::-1]
            pts.extend(a if not pts else a[1:])
        return pts

    geos = d['objects']['land']['geometries']
    poligonos = []
    for g in geos:
        if g['type'] == 'Polygon':
            poligonos.append(g['arcs'])
        elif g['type'] == 'MultiPolygon':
            poligonos.extend(g['arcs'])
    caminos, puntos = [], 0
    for pol in poligonos:
        for r in pol:
            pts = anillo(r)
            lons, lats = [p[0] for p in pts], [p[1] for p in pts]
            if max(lons) < 2 or min(lons) > 38 or max(lats) < 28 or min(lats) > 47:
                continue
            xy = [proyecta(*p) for p in pts]
            simp = [xy[0]]
            for p in xy[1:]:
                if math.dist(p, simp[-1]) >= 1.6:
                    simp.append(p)
            if len(simp) < 4:
                continue
            xs, ys = [p[0] for p in simp], [p[1] for p in simp]
            if (max(xs) - min(xs)) * (max(ys) - min(ys)) < 12:   # islotes de menos de unos 3 × 4 px
                continue
            caminos.append('M' + 'L'.join(f'{x:.0f},{y:.0f}' for x, y in simp) + 'Z')
            puntos += len(simp)
    open(sys.argv[2], 'w').write(''.join(caminos))
    print(f'{len(caminos)} costas, {puntos} puntos, {sum(map(len, caminos)) // 1024} KB')


if __name__ == '__main__':
    main()
