"""
Geografía para los mapas del canal: fronteras de Natural Earth (dominio público) en el TopoJSON de world-atlas
(jsDelivr), medidas sobre la esfera y caminos SVG en la proyección de cada plano.

  python3 canales/geografia/kit/geo.py medir Chile          # largo norte-sur, ancho por latitud, el punto más estrecho

Las medidas salen del contorno a 1:10 millones: valen para un vídeo («unos 90 km»), no para un catastro.
"""
import json
import math
import os
import sys
import urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DATOS = os.path.join(REPO, 'salidas', 'geografia', 'datos')
R = 6371.0088  # radio medio de la Tierra, km


def archivo(nombre='countries-10m'):
    ruta = os.path.join(DATOS, nombre + '.json')
    if not os.path.exists(ruta):
        os.makedirs(DATOS, exist_ok=True)
        urllib.request.urlretrieve(f'https://cdn.jsdelivr.net/npm/world-atlas@2/{nombre}.json', ruta)
    return ruta


def paises(nombre='countries-10m'):
    """{nombre: [polígono, ...]}; cada polígono, una lista de anillos [(lon, lat), ...] (el primero, el exterior)."""
    d = json.load(open(archivo(nombre)))
    (sx, sy), (tx, ty) = d['transform']['scale'], d['transform']['translate']
    arcos = []
    for a in d['arcs']:
        x = y = 0
        pts = []
        for dx, dy in a:
            x, y = x + dx, y + dy
            pts.append((x * sx + tx, y * sy + ty))
        arcos.append(pts)

    def anillo(ids):
        pts = []
        for i in ids:
            a = arcos[i] if i >= 0 else arcos[~i][::-1]
            pts.extend(a if not pts else a[1:])
        return pts

    out = {}
    for g in d['objects']['countries']['geometries']:
        pols = [g['arcs']] if g['type'] == 'Polygon' else g['arcs'] if g['type'] == 'MultiPolygon' else []
        out[g['properties']['name']] = [[anillo(r) for r in p] for p in pols]
    return out


def fronteras(a, b, nombre='countries-10m'):
    """La frontera común de dos países: las líneas (arcos del TopoJSON) que comparten, como listas de (lon, lat)."""
    d = json.load(open(archivo(nombre)))
    (sx, sy), (tx, ty) = d['transform']['scale'], d['transform']['translate']
    usados = {}
    for g in d['objects']['countries']['geometries']:
        if g['properties']['name'] not in (a, b):
            continue
        pols = [g['arcs']] if g['type'] == 'Polygon' else g['arcs']
        usados[g['properties']['name']] = {i if i >= 0 else ~i for p in pols for r in p for i in r}
    comunes = usados[a] & usados[b]
    lineas = []
    for i in sorted(comunes):
        x = y = 0
        pts = []
        for dx, dy in d['arcs'][i]:
            x, y = x + dx, y + dy
            pts.append((x * sx + tx, y * sy + ty))
        lineas.append(pts)
    return lineas


def recorta(anillo_, lat, norte=True):
    """El anillo cortado por un paralelo: lo que queda al norte (o al sur) de lat (Sutherland–Hodgman)."""
    dentro = (lambda p: p[1] >= lat) if norte else (lambda p: p[1] <= lat)
    out = []
    for p, q in zip(anillo_, anillo_[1:] + anillo_[:1]):
        if dentro(q):
            if not dentro(p):
                out.append((p[0] + (lat - p[1]) * (q[0] - p[0]) / (q[1] - p[1]), lat))
            out.append(q)
        elif dentro(p):
            out.append((p[0] + (lat - p[1]) * (q[0] - p[0]) / (q[1] - p[1]), lat))
    return out


def linea(pts, proj, minimo=1.2):
    """Camino SVG abierto (una frontera, un río)."""
    xy = [proj(*p) for p in pts]
    simp = [xy[0]]
    for p in xy[1:]:
        if math.dist(p, simp[-1]) >= minimo:
            simp.append(p)
    return 'M' + 'L'.join(f'{x:.1f},{y:.1f}' for x, y in simp)


def distancia(a, b):
    """Gran círculo entre (lon, lat) y (lon, lat), en km."""
    l1, f1, l2, f2 = map(math.radians, (*a, *b))
    h = math.sin((f2 - f1) / 2) ** 2 + math.cos(f1) * math.cos(f2) * math.sin((l2 - l1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def area_km2(anillo_):
    """Área aproximada de un anillo (proyección equivalente local)."""
    lat0 = sum(p[1] for p in anillo_) / len(anillo_)
    k = math.cos(math.radians(lat0))
    xy = [(p[0] * 111.32 * k, p[1] * 110.57) for p in anillo_]
    return abs(sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(xy, xy[1:] + xy[:1]))) / 2


def principal(poligonos):
    """El polígono más grande (el territorio continental)."""
    return max(poligonos, key=lambda p: area_km2(p[0]))


def cortes(anillo_, lat):
    """Longitudes donde el paralelo lat corta el anillo."""
    xs = []
    for (x1, y1), (x2, y2) in zip(anillo_, anillo_[1:] + anillo_[:1]):
        if (y1 <= lat < y2) or (y2 <= lat < y1):
            xs.append(x1 + (lat - y1) * (x2 - x1) / (y2 - y1))
    return sorted(xs)


def ancho(poligono, lat):
    """Ancho este-oeste del polígono en esa latitud (km): la suma de los tramos dentro."""
    xs = cortes(poligono[0], lat)
    dentro = sum(b - a for a, b in zip(xs[::2], xs[1::2]))
    return dentro * 111.32 * math.cos(math.radians(lat))


def extremos(poligonos):
    pts = [p for pol in poligonos for p in pol[0]]
    return max(pts, key=lambda p: p[1]), min(pts, key=lambda p: p[1])


class Azimutal:
    """Proyección azimutal equidistante local: distancias reales desde el centro; km → píxeles con la escala dada."""

    def __init__(self, lon0, lat0, px_km, cx, cy, giro=0.0):
        self.l0, self.f0 = math.radians(lon0), math.radians(lat0)
        self.k, self.cx, self.cy, self.g = px_km, cx, cy, math.radians(giro)

    def km(self, lon, lat):
        l, f = math.radians(lon), math.radians(lat)
        c = math.acos(max(-1, min(1, math.sin(self.f0) * math.sin(f) + math.cos(self.f0) * math.cos(f) * math.cos(l - self.l0))))
        kk = R * c / math.sin(c) if c > 1e-9 else R
        x = kk * math.cos(f) * math.sin(l - self.l0)
        y = kk * (math.cos(self.f0) * math.sin(f) - math.sin(self.f0) * math.cos(f) * math.cos(l - self.l0))
        return x, y

    def __call__(self, lon, lat):
        x, y = self.km(lon, lat)
        x, y = x * math.cos(self.g) - y * math.sin(self.g), x * math.sin(self.g) + y * math.cos(self.g)
        return self.cx + x * self.k, self.cy - y * self.k


def camino(anillos, proj, minimo=1.2, caja=None):
    """Camino SVG de unos anillos; quita puntos a menos de `minimo` px y los anillos fuera de la caja (x0, y0, x1, y1)."""
    partes = []
    for r in anillos:
        xy = [proj(*p) for p in r]
        if caja:
            xs, ys = [p[0] for p in xy], [p[1] for p in xy]
            if max(xs) < caja[0] or min(xs) > caja[2] or max(ys) < caja[1] or min(ys) > caja[3]:
                continue
        simp = [xy[0]]
        for p in xy[1:]:
            if math.dist(p, simp[-1]) >= minimo:
                simp.append(p)
        if len(simp) >= 3:
            partes.append('M' + 'L'.join(f'{x:.1f},{y:.1f}' for x, y in simp) + 'Z')
    return ''.join(partes)


def medir(nombre):
    pols = paises()[nombre]
    p = principal(pols)
    norte, sur = extremos(pols)
    norte_c, sur_c = extremos([p])
    lats = [x / 20 for x in range(round(sur_c[1] * 20) + 1, round(norte_c[1] * 20))]
    anchos = [(lat, ancho(p, lat)) for lat in lats]
    validos = [(lat, a) for lat, a in anchos if a > 0]
    estrecho = min(validos, key=lambda t: t[1])
    ancho_max = max(validos, key=lambda t: t[1])
    print(f'{nombre}: {len(pols)} polígonos; el continental, {area_km2(p[0]):,.0f} km² (aprox.)')
    print(f'  norte {norte[1]:.2f}°, {norte[0]:.2f}°; sur (con islas) {sur[1]:.2f}°, {sur[0]:.2f}°: {distancia(norte, sur):,.0f} km')
    print(f'  continental: norte {norte_c[1]:.2f}°, sur {sur_c[1]:.2f}°: {distancia(norte_c, sur_c):,.0f} km')
    print(f'  ancho medio (continental, cada 0,05°): {sum(a for _, a in validos) / len(validos):.0f} km; '
          f'el más estrecho {estrecho[1]:.0f} km a {estrecho[0]:.2f}°; el más ancho {ancho_max[1]:.0f} km a {ancho_max[0]:.2f}°')
    return dict(norte=norte, sur=sur, largo=distancia(norte, sur), estrecho=estrecho, ancho_max=ancho_max)


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == 'medir':
        medir(' '.join(sys.argv[2:]))
