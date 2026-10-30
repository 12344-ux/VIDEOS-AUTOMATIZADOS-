"""
Monta un capítulo de «El mecanismo de Anticitera» como proyecto de HyperFrames a partir de su
descripción (montaje/capN.py) y de los tiempos de su narración (salidas/anticitera/voz/capN.json).
Es el kit del estilo A sacado de la apertura: las planchas en 2.5D (kit/planchas.html), los rótulos
(etiqueta con línea, nombre, cifra, dato, título, cita), las líneas guía, los gráficos dibujados
(graficos/*.html), el rótulo del capítulo y el sonido. Todo se ancla a la palabra que lo dice.

  python3 videos/anticitera/kit/montar.py cap1            escribe cap1/ y copia sus recursos
  python3 videos/anticitera/kit/montar.py cap1 --borrador  con planchas provisionales si faltan

En montaje/capN.py hay disponibles (ver cap1.py como ejemplo):
  w("palabra"), w("dos palabras", n=2, fin=True, mas=0.1)  tiempo en el capítulo de esa palabra
  DUR, VOZ0                                               duración del capítulo y entrada de la voz
  toma(nombre, desde, entra=..., mov=..., ...)            una plancha; acaba donde empieza la siguiente
  bloque(x, y, [E(...), N(...), C(...), D(...), T(...), Q(...)], sale=t)   rótulos
  guia(x, y, largo, t, sale, angulo=0)                    línea guía con punto
  grafico(nombre, desde, hasta, **parametros)             graficos/<nombre>.html, donde {{p:x}} es un parámetro,
                                                          {{t:x}} un parámetro de tiempo (pasa a local), {{w:palabra}}
                                                          y {{f:palabra}} el inicio y el fin de una palabra
  sonido(nombre, t, vol, dur=None, ini=0, fi=0, fo=0)     efectos (ver SFX)
  MUSICA = dict(subidas=[(t0, t1, v)])                    la música: más presente en un tramo
"""
import html
import json
import os
import re
import shutil
import subprocess
import sys
import wave

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)                       # videos/anticitera
REPO = os.path.dirname(os.path.dirname(RAIZ))
TRABAJO = os.environ.get('TRABAJO', os.path.join(REPO, 'salidas', 'anticitera'))
H = os.environ.get('HERRAMIENTAS', os.path.expanduser('~/herramientas-videos'))
SFX_HF = os.path.join(H, 'hyperframes/node_modules/hyperframes/dist/skills/media-use/audio/assets/sfx')

VOZ0 = 3.4      # la voz entra tras el rótulo del capítulo
COLA = 2.6      # de la última palabra al final del capítulo (el último cuadro ya en negro)
TINTA, ACENTO, GRIS = '#f3ede4', '#e8b66a', '#8a8780'

# Efectos: BigSoundBank (CC0, audio/efectos.py) y la biblioteca de HyperFrames (licencia de Pixabay).
SFX = {
    'tictac': '2138.wav', 'tictac2': '2655.wav', 'tictac3': '2816.wav', 'maquina': '2841.wav',
    'grillos': '0425.wav', 'noche': '1880.wav', 'monedas': '0194.wav', 'fuego': '0987.wav',
    'chimenea': '2857.wav', 'paginas': '2212.wav', 'lapiz': '0221.wav', 'cajon': '1267.wav',
    'interruptor': '3061.wav', 'clic': '0052.wav', 'zumbido': '2118.wav', 'transformador': '0086.wav',
    'pasos': '1515.wav', 'viento': '0155.wav', 'vendaval': '0146.wav', 'manivela': '2470.wav',
    'yunque': '3590.wav', 'mercado': '2728.wav', 'barrido': '1801.wav', 'barrido2': '1800.wav',
    'escaner': '1796.wav', 'olas': '2570.wav', 'parquet': '3060.wav', 'trueno': '3113.wav',
    'lluvia': '0740.wav', 'jarcias': '2444.wav',
    'travesia': 'hf:whoosh-cinematic.mp3', 'golpe': 'hf:impact-bass-1.mp3', 'golpe2': 'hf:impact-bass-2.mp3',
    'whoosh': 'hf:whoosh.mp3', 'tecla': 'hf:key-press.mp3', 'subida': 'hf:riser.mp3',
}
FUENTES = ['cormorant-500.woff2', 'cormorant-500-italic.woff2', 'hanken-500.woff2', 'hanken-600.woff2', 'didot-griego.woff2']


def limpia(s):
    return re.sub(r'[^\wáéíóúüñ]', '', s.lower())


def duracion_audio(ruta):
    if ruta.endswith('.wav'):
        with wave.open(ruta) as w:
            return w.getnframes() / w.getframerate()
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', ruta],
                       capture_output=True, text=True, check=True)
    return float(r.stdout)


def r3(x):
    return round(float(x), 3)


# ---------------------------------------------------------------- descripción del capítulo

class Parte:
    def __init__(self, tipo, texto, t, **k):
        self.tipo, self.texto, self.t, self.k = tipo, texto, t, k


def E(texto, t): return Parte('e', texto, t)                                 # etiqueta con línea
def N(texto, t, tam=132): return Parte('n', texto, t, tam=tam)               # nombre propio, letra a letra
def D(texto, t, tacha=None, tam=None): return Parte('d', texto, t, tacha=tacha, tam=tam)   # dato, de gris a tinta
def T(texto, t, em=None, tam=104): return Parte('t', texto, t, em=em, tam=tam)   # título, palabra a palabra
def Q(texto, t, tam=60): return Parte('q', texto, t, tam=tam)                 # cita o frase destacada
def P(texto, t): return Parte('p', texto, t)                                   # pie: créditos y fuentes, pequeño
def M(texto, t, paso=0.055, tam=72): return Parte('m', texto, t, paso=paso, tam=tam)   # a máquina, letra a letra


def C(texto, t, desde=None, unidad=None, dur=1.3, tam=236):
    """Cifra: con desde, un contador que aterriza en t; si no, cifra a cifra desde t."""
    return Parte('c', texto, t, desde=desde, unidad=unidad, dur=dur, tam=tam)


class Capitulo:
    def __init__(self, cid):
        self.id = cid
        g = json.load(open(os.path.join(RAIZ, 'recursos', 'guion.json')))
        meta = next(c for c in g['capitulos'] if c['id'] == cid)
        self.numero, self.titulo = meta['numero'], meta['titulo']
        self.voz = json.load(open(os.path.join(TRABAJO, 'voz', cid + '.json')))
        self.palabras = [p for f in self.voz['frases'] for p in f['palabras']]
        self.dur = round(VOZ0 + self.voz['duracion'] + COLA, 2)
        self.tomas, self.bloques, self.guias, self.graficos, self.sonidos = [], [], [], [], []
        self.musica = {}
        self.ambiguas = {}

    def w(self, palabra, n=1, fin=False, mas=0.0):
        busca = [limpia(x) for x in palabra.split()]
        hechas = []
        for i in range(len(self.palabras) - len(busca) + 1):
            if all(limpia(self.palabras[i + j]['texto']) == b for j, b in enumerate(busca)):
                hechas.append(i)
        if len(hechas) < n:
            raise SystemExit(f'{self.id}: no está «{palabra}» (aparición {n})')
        if len(hechas) > 1 and n == 1 and palabra not in self.ambiguas:
            self.ambiguas[palabra] = [r3(VOZ0 + self.palabras[i]['inicio']) for i in hechas]
        i = hechas[n - 1]
        p = self.palabras[i + len(busca) - 1] if fin else self.palabras[i]
        return r3(VOZ0 + (p['fin'] if fin else p['inicio']) + mas)

    def ultima(self):
        return r3(VOZ0 + self.palabras[-1]['fin'])


def cargar(cid):
    cap = Capitulo(cid)

    def toma(nombre, desde, entra='corte', mov='empuje', **k):
        cap.tomas.append(dict(nombre=nombre, desde=r3(desde), entra=entra, mov=mov, **k))

    def bloque(x, y, partes, sale, der=False, ancho=None, id=None):
        cap.bloques.append(dict(x=x, y=y, partes=partes, sale=r3(sale), der=der, ancho=ancho, id=id))

    def guia(x, y, largo, t, sale, angulo=0):
        cap.guias.append(dict(x=x, y=y, largo=largo, t=r3(t), sale=r3(sale), angulo=angulo))

    def grafico(nombre, desde, hasta, id=None, z=2, **p):
        cap.graficos.append(dict(nombre=nombre, desde=r3(desde), hasta=r3(hasta), id=id or nombre, z=z, p=p))

    def sonido(nombre, t, vol=1.0, dur=None, ini=0, fi=0, fo=0, fx=None):
        cap.sonidos.append(dict(nombre=nombre, t=r3(t), vol=vol, dur=dur, ini=ini, fi=fi, fo=fo, fx=fx))

    nombres = dict(w=cap.w, DUR=cap.dur, VOZ0=VOZ0, ULTIMA=cap.ultima(), toma=toma, bloque=bloque, guia=guia,
                   grafico=grafico, sonido=sonido, E=E, N=N, C=C, D=D, T=T, Q=Q, M=M, P=P)
    ruta = os.path.join(RAIZ, 'montaje', cid + '.py')
    exec(compile(open(ruta).read(), ruta, 'exec'), nombres)
    cap.musica = nombres.get('MUSICA', {})
    cap.titulo_ancho = nombres.get('TITULO_ANCHO', 1200)   # el rótulo del capítulo pasa a dos líneas si no cabe
    if 'DURACION' in nombres:
        cap.dur = nombres['DURACION']
    return cap


# ---------------------------------------------------------------- planchas y cámara

MOVIMIENTOS = {   # parámetro: (inicio, fin) a lo largo de la toma, con sine.inOut
    'empuje': dict(zoom=(1.04, 1.10), camX=(-0.012, 0.012)),
    'retroceso': dict(zoom=(1.12, 1.05), camX=(0.012, -0.012)),
    'izq': dict(zoom=(1.08, 1.08), panX=(0.016, -0.016), camX=(0.014, -0.014)),
    'der': dict(zoom=(1.08, 1.08), panX=(-0.016, 0.016), camX=(-0.014, 0.014)),
    'sube': dict(zoom=(1.08, 1.09), panY=(0.02, -0.02), camY=(0.008, -0.008)),
    'baja': dict(zoom=(1.08, 1.09), panY=(-0.02, 0.02), camY=(-0.008, 0.008)),
    'quieto': dict(zoom=(1.06, 1.065), camX=(-0.005, 0.005)),
}
CURVAS = {'zoom', 'panX', 'panY', 'camX', 'camY'}
# Planchas que siempre van más cerradas: la placa de bronce (fondo de los dibujos) tiene un borde brillante.
ZOOM_BASE = {'placa': 1.34}


def tomas_js(cap):
    tomas = sorted(cap.tomas, key=lambda x: x['desde'])
    salida = []
    for i, tm in enumerate(tomas):
        t0, t1 = tm['desde'], (tomas[i + 1]['desde'] if i + 1 < len(tomas) else cap.dur)
        base = dict(MOVIMIENTOS[tm['mov']]) if isinstance(tm['mov'], str) else dict(tm['mov'])
        for k in ('zoom', 'panX', 'panY', 'camX', 'camY'):
            if k in tm:
                base[k] = tm[k] if isinstance(tm[k], tuple) else (tm[k], tm[k])
        if tm['nombre'] in ZOOM_BASE and 'zoom' in base:
            base['zoom'] = tuple(z * ZOOM_BASE[tm['nombre']] for z in base['zoom'])
        b = tm.get('brillo', 1.0)
        li, lr = tm.get('luzI', 0.15), tm.get('luzR', 0.25)
        claves = {k: [] for k in ('zoom', 'panX', 'panY', 'camX', 'camY', 'desenfoque', 'radial', 'brillo', 'luzI', 'luzR')}
        curva = tm.get('curva', 'sine.inOut')

        def f(k, t):
            a, z = base.get(k, (None, None))
            if a is None:
                return {'zoom': 1.0}.get(k, 0.0)
            p = min(1.0, max(0.0, (t - t0) / max(t1 - t0, 1e-3)))
            q = p * p * (3 - 2 * p)   # aproximación de sine.inOut para empalmar las claves
            return a + (z - a) * q

        for k in base:
            claves[k] = [[t0, base[k][0]], [t1, base[k][1], curva]]
        claves['brillo'] = [[t0, b]]
        claves['luzI'] = [[t0, li]]
        claves['luzR'] = [[t0, lr]]
        dirv = [1, 0]

        # Entrada: cómo llega esta toma (la causa está en la anterior o en lo que dice la voz).
        e = tm['entra']
        if e == 'negro':
            claves['brillo'] = [[t0, 0.0], [t0 + tm.get('fundido', 1.4), b, 'power2.out']]
        elif e in ('barrido', 'barrido-v'):
            k = 'panX' if e == 'barrido' else 'panY'
            dirv = [1, 0] if e == 'barrido' else [0, 1]
            v1 = f(k, t0 + 0.34)
            claves[k] = [[t0, v1 - 0.18], [t0 + 0.34, v1, 'expo.out']] + [c for c in claves[k] if c[0] > t0 + 0.34]
            claves['desenfoque'] = [[t0, 0.08], [t0 + 0.2, 0, 'power2.out']]
        elif e == 'oscuro':
            claves['brillo'] = [[t0, 0.04], [t0 + 0.9, b, 'power2.out']]
        elif e == 'destello':
            claves['luzI'] = [[t0, 3.0], [t0 + 0.6, li, 'power2.out']]
            claves['luzR'] = [[t0, 2.6], [t0 + 0.6, lr, 'power2.out']]
            claves['brillo'] = [[t0, 1.5], [t0 + 0.5, b, 'power2.out']]
        elif e == 'zoom':
            z1 = f('zoom', t0 + 0.55)
            claves['zoom'] = [[t0, z1 * 1.25], [t0 + 0.55, z1, 'power2.out']] + [c for c in claves['zoom'] if c[0] > t0 + 0.55]
            claves['radial'] = [[t0, 0.04], [t0 + 0.4, 0, 'power2.out']]

        # Salida: la prepara la toma siguiente.
        sig = tomas[i + 1]['entra'] if i + 1 < len(tomas) else 'fin'
        if sig == 'corte':        # corte con oscurecido: un 40 % los tres últimos cuadros
            claves['brillo'] += [[t1 - 0.101, b], [t1 - 0.1, b * 0.6]]
        elif sig in ('barrido', 'barrido-v'):
            k = 'panX' if sig == 'barrido' else 'panY'
            dirv = [1, 0] if sig == 'barrido' else [0, 1]
            v0 = f(k, t1 - 0.26)
            claves[k] = [c for c in claves[k] if c[0] < t1 - 0.26] + [[t1 - 0.26, v0], [t1, v0 + 0.22, 'power3.in']]
            claves['desenfoque'] += [[t1 - 0.24, 0], [t1, 0.08, 'power3.in']]
        elif sig == 'oscuro':
            claves['brillo'] += [[t1 - 0.55, b], [t1, 0.04, 'power2.in']]
        elif sig == 'destello':
            claves['luzI'] += [[t1 - 0.32, li], [t1, 3.0, 'power2.in']]
            claves['luzR'] += [[t1 - 0.32, lr], [t1, 2.6, 'power2.in']]
            claves['brillo'] += [[t1 - 0.3, b], [t1, 1.5, 'power2.in']]
        elif sig == 'zoom':
            z0 = f('zoom', t1 - 0.45)
            claves['zoom'] = [c for c in claves['zoom'] if c[0] < t1 - 0.45] + [[t1 - 0.45, z0], [t1, z0 * 2.2, 'power3.in']]
            claves['radial'] += [[t1 - 0.4, 0], [t1, 0.05, 'power3.in']]
        elif sig == 'fin':
            claves['brillo'] += [[t1 - 0.85, b], [t1 - 0.08, 0.0, 'power2.in']]

        js = dict(nombre=tm['nombre'], desde=t0, hasta=r3(t1), luz=list(tm.get('luz', (0.72, 0.3))),
                  luzColor=list(tm.get('luzColor', (1.0, 0.82, 0.56))), dir=dirv,
                  ventana=list(tm.get('ventana', (0.27, 0.5, 0.62))),
                  ventanaI=[[t0, tm.get('ventanaI', 0.4)]])
        if tm.get('capas') is False:
            js['capas'] = False
        if 'centro' in tm:
            js['centro'] = list(tm['centro'])
        if 'sat' in tm:
            js['sat'] = tm['sat']
        for k, v in claves.items():
            v = sorted(v, key=lambda c: c[0])
            if v:
                js[k] = [[r3(c[0]), round(c[1], 4)] + c[2:] for c in v]
        for k, v in tm.get('mas', {}).items():      # claves a mano dentro de la toma (un golpe de zoom, una sacudida)
            js[k] = sorted(js.get(k, []) + [[r3(c[0])] + list(c[1:]) for c in v], key=lambda c: c[0])
        for k, v in tm.get('claves', {}).items():   # claves a mano que sustituyen a las calculadas
            js[k] = v
        salida.append(js)
    return salida


# ---------------------------------------------------------------- rótulos

CSS = f'''
    @font-face {{ font-family: "Cormorant Garamond"; src: url("assets/fonts/cormorant-500.woff2") format("woff2"); font-weight: 500; }}
    @font-face {{ font-family: "Cormorant Garamond"; src: url("assets/fonts/cormorant-500-italic.woff2") format("woff2"); font-weight: 500; font-style: italic; }}
    @font-face {{ font-family: "Hanken Grotesk"; src: url("assets/fonts/hanken-500.woff2") format("woff2"); font-weight: 500; }}
    @font-face {{ font-family: "Hanken Grotesk"; src: url("assets/fonts/hanken-600.woff2") format("woff2"); font-weight: 600; }}
    #root {{ position: absolute; inset: 0; }}
    .blq {{ position: absolute; color: var(--color-ink, {TINTA}); }}
    .blq.der {{ text-align: right; }}
    .blq > * + * {{ margin-top: 22px; }}
    .e {{ display: flex; align-items: center; gap: 22px; font: 600 36px/1 "Hanken Grotesk", sans-serif;
      letter-spacing: 0.24em; color: var(--color-accent, {ACENTO}); text-shadow: 0 2px 14px rgba(0, 0, 0, 0.6); }}
    .der .e {{ justify-content: flex-end; }}
    .e i {{ display: block; width: 72px; height: 2px; background: var(--color-accent, {ACENTO}); transform-origin: left center; }}
    .e span, .n span, .c span {{ display: inline-block; }}
    .n {{ margin-left: -6px; font: 500 132px/1 "Cormorant Garamond", serif; letter-spacing: 0.005em; text-shadow: 0 4px 30px rgba(0, 0, 0, 0.4); }}
    .c {{ margin-left: -10px; display: flex; align-items: baseline; gap: 18px; font-family: "Cormorant Garamond", serif;
      font-weight: 500; line-height: 0.9; font-variant-numeric: lining-nums tabular-nums; text-shadow: 0 6px 40px rgba(0, 0, 0, 0.45); }}
    .der .c {{ justify-content: flex-end; margin-left: 0; }}
    .c em {{ font-style: italic; font-size: 0.51em; }}
    .d {{ font: 500 46px/1.25 "Hanken Grotesk", sans-serif; text-shadow: 0 2px 18px rgba(0, 0, 0, 0.7); font-variant-numeric: lining-nums; }}
    .d b {{ position: relative; font-weight: 500; }}
    .d b u {{ position: absolute; left: -6px; right: -6px; top: 52%; height: 3px; background: var(--color-accent, {ACENTO}); transform-origin: left center; }}
    .t {{ font-family: "Cormorant Garamond", serif; font-weight: 500; line-height: 1.04; letter-spacing: -0.005em; text-shadow: 0 4px 34px rgba(0, 0, 0, 0.5); }}
    .t span {{ display: inline-block; margin-right: 0.22em; }}
    .t em {{ font-style: italic; color: var(--color-accent, {ACENTO}); }}
    .q {{ font-family: "Cormorant Garamond", serif; font-style: italic; font-weight: 500; line-height: 1.15; text-shadow: 0 4px 30px rgba(0, 0, 0, 0.5); }}
    .q span {{ display: inline-block; margin-right: 0.24em; }}
    .pie {{ font: 500 30px/1.35 "Hanken Grotesk", sans-serif; letter-spacing: 0.02em; text-shadow: 0 2px 14px rgba(0, 0, 0, 0.6); }}
    .blq > .pie + .pie {{ margin-top: 6px; }}
    .m {{ font-family: "Cormorant Garamond", serif; font-weight: 500; line-height: 1.1; text-shadow: 0 4px 30px rgba(0, 0, 0, 0.5); }}
    .m span {{ display: inline-block; }}
    .gu {{ position: absolute; height: 2px; background: var(--color-accent, {ACENTO}); transform-origin: left center; }}
    .gu::after {{ content: ""; position: absolute; right: -5px; top: -4px; width: 10px; height: 10px; border-radius: 50%; background: var(--color-accent, {ACENTO}); }}
'''


def letras(texto):
    return ''.join('<br>' if ch == '\n' else '<span>&nbsp;</span>' if ch == ' ' else f'<span>{html.escape(ch)}</span>' for ch in texto)


def palabras_html(texto, em=None):
    em = set((em or '').split())
    return ''.join(f'<em><span>{html.escape(p)}</span></em>' if p in em else f'<span>{html.escape(p)}</span>'
                   for p in texto.split())


def comp_textos(cid, tm, bloques, guias, avisos):
    """Una composición de texto por toma: sus bloques y líneas guía, con tiempos locales."""
    t0 = tm['desde']
    L = lambda t: f'{t - t0:.3f}'
    marcado, js = [], []
    for bi, b in enumerate(bloques):
        bid = b['id'] or f'{cid}-{tm["tid"]}-b{bi}'   # único en el capítulo: todas las tomas comparten documento
        lado = f'right: {b["x"]}px' if b['der'] else f'left: {b["x"]}px'
        ancho = f'; width: {b["ancho"]}px' if b['ancho'] else ''
        partes = []
        for pi, p in enumerate(b['partes']):
            pid = f'{bid}-{pi}'
            leer = 0.5 + 0.3 * max(1, len(p.texto.split()))
            if b['sale'] - p.t < leer - 0.05:
                avisos.append(f'{cid}: «{p.texto}» se lee {b["sale"] - p.t:.1f} s (pide {leer:.1f} s)')
            if p.tipo == 'e':
                partes.append(f'<div id="{pid}" class="e" data-layout-ignore><i></i>{letras(p.texto)}</div>')
                js.append(f'tl.fromTo("#{pid} i", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.5, ease: "expo.out" }}, {L(p.t - 0.06)});')
                st = 0.03 if len(p.texto) <= 18 else 0.018
                js.append(f'tl.fromTo("#{pid} span", {{ opacity: 0, filter: "blur(4px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power2.out", stagger: {st} }}, {L(p.t)});')
            elif p.tipo == 'n':
                partes.append(f'<div id="{pid}" class="n" style="font-size: {p.k["tam"]}px" data-layout-ignore>{letras(p.texto)}</div>')
                js.append(f'tl.fromTo("#{pid} span", {{ opacity: 0, filter: "blur(5px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.24, ease: "power2.out", stagger: 0.06 }}, {L(p.t)});')
            elif p.tipo == 'c':
                k = p.k
                unidad = f'<em>{html.escape(k["unidad"])}</em>' if k['unidad'] else ''
                if k['desde'] is not None:
                    partes.append(f'<div id="{pid}" class="c" style="font-size: {k["tam"]}px"><span id="{pid}-n">{k["desde"]}</span>{unidad}</div>')
                    a = p.t - k['dur']
                    js.append(f'tl.fromTo("#{pid}", {{ opacity: 0, filter: "blur(10px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.22, ease: "power3.out" }}, {L(a)});')
                    js.append(f'(function () {{ const n = document.getElementById("{pid}-n"), o = {{ v: {k["desde"]} }};'
                              f' tl.fromTo(o, {{ v: {k["desde"]} }}, {{ v: {p.texto}, duration: {k["dur"]}, ease: "power2.out",'
                              f' onUpdate: () => {{ n.textContent = String(Math.round(o.v)); }} }}, {L(a)}); }})();')
                else:
                    partes.append(f'<div id="{pid}" class="c" style="font-size: {k["tam"]}px" data-layout-ignore>{letras(p.texto)}{unidad}</div>')
                    js.append(f'tl.fromTo("#{pid} > *", {{ opacity: 0, filter: "blur(12px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.22, ease: "power3.out", stagger: 0.11 }}, {L(p.t)});')
            elif p.tipo == 'd':
                texto = html.escape(p.texto)
                if p.k.get('tacha') is not None:
                    texto = f'<b>{texto}<u></u></b>'
                tam = f' style="font-size: {p.k["tam"]}px"' if p.k.get('tam') else ''
                partes.append(f'<div id="{pid}" class="d"{tam}>{texto}</div>')
                js.append(f'tl.fromTo("#{pid}", {{ opacity: 0, color: "{GRIS}" }}, {{ opacity: 1, duration: 0.2, ease: "power1.out" }}, {L(p.t)});')
                js.append(f'tl.to("#{pid}", {{ color: "{TINTA}", duration: 0.5, ease: "power2.out" }}, {L(p.t + 0.2)});')
                if p.k.get('tacha') is not None:
                    tc = p.k['tacha']
                    js.append(f'tl.fromTo("#{pid} u", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.35, ease: "power3.out" }}, {L(tc)});')
                    js.append(f'tl.to("#{pid} b", {{ opacity: 0.55, duration: 0.3, ease: "power2.out" }}, {L(tc + 0.2)});')
            elif p.tipo == 'p':
                partes.append(f'<div id="{pid}" class="pie">{html.escape(p.texto)}</div>')
                js.append(f'tl.fromTo("#{pid}", {{ opacity: 0 }}, {{ opacity: 0.78, duration: 0.5, ease: "power1.out" }}, {L(p.t)});')
            elif p.tipo == 'm':
                partes.append(f'<div id="{pid}" class="m" style="font-size: {p.k["tam"]}px" data-layout-ignore>{letras(p.texto)}</div>')
                js.append(f'gsap.utils.toArray("#{pid} span").forEach((s, i) => {{ tl.set(s, {{ opacity: 0 }}, 0); tl.set(s, {{ opacity: 1 }}, {L(p.t)} + i * {p.k["paso"]}); }});')
            elif p.tipo in ('t', 'q'):
                cls = p.tipo
                partes.append(f'<div id="{pid}" class="{cls}" style="font-size: {p.k["tam"]}px">{palabras_html(p.texto, p.k.get("em"))}</div>')
                if cls == 't':
                    js.append(f'gsap.utils.toArray("#{pid} span").forEach((s, i) => tl.fromTo(s, {{ opacity: 0, filter: "blur(6px)" }},'
                              f' {{ opacity: 1, filter: "blur(0px)", duration: 0.13, ease: "power2.out" }}, {L(p.t)} + i * 0.067));')
                else:
                    js.append(f'tl.fromTo("#{pid} span", {{ opacity: 0 }}, {{ opacity: 0.28, duration: 0.25, ease: "power1.out" }}, {L(p.t - 0.25)});')
                    js.append(f'gsap.utils.toArray("#{pid} span").forEach((s, i) => tl.to(s, {{ opacity: 1, duration: 0.16, ease: "power2.out" }}, {L(p.t)} + i * 0.09));')
        marcado.append(f'    <div id="{bid}" class="blq{" der" if b["der"] else ""}" style="{lado}; top: {b["y"]}px{ancho}">\n      '
                       + '\n      '.join(partes) + '\n    </div>')
        js.append(f'tl.to("#{bid} > *", {{ opacity: 0, filter: "blur(8px)", duration: 0.18, ease: "power2.in", stagger: 0.04 }}, {L(b["sale"])});')
    for gi, g in enumerate(guias):
        gid = f'{cid}-{tm["tid"]}-g{gi}'
        marcado.append(f'    <i id="{gid}" class="gu" style="left: {g["x"]}px; top: {g["y"]}px; width: {g["largo"]}px; transform: rotate({g["angulo"]}deg)"></i>')
        js.append(f'tl.fromTo("#{gid}", {{ scaleX: 0, rotation: {g["angulo"]} }}, {{ scaleX: 1, rotation: {g["angulo"]}, duration: 0.45, ease: "expo.out" }}, {L(g["t"])});')
        js.append(f'tl.to("#{gid}", {{ opacity: 0, duration: 0.16, ease: "power2.in" }}, {L(g["sale"])});')
    ident = tm['tid']
    return f'''<template>
  <style>{CSS}  </style>
  <div id="root" data-composition-id="{ident}" data-width="1920" data-height="1080">
{chr(10).join(marcado)}
  </div>
  <script>
    (function () {{
      // Generado por kit/montar.py desde montaje/{cid}.py: tiempos locales (la toma empieza en {t0:.2f} s).
      const tl = gsap.timeline({{ paused: true }});
      {(chr(10) + '      ').join(js)}
      window.__timelines["{ident}"] = tl;
    }})();
  </script>
</template>
'''


# ---------------------------------------------------------------- gráficos dibujados

def comp_grafico(cap, g):
    fuente = open(os.path.join(RAIZ, 'graficos', g['nombre'] + '.html')).read()
    t0 = g['desde']

    def sustituye(m):
        tipo, clave = m.group(1), m.group(2)
        if tipo == 't':                              # un tiempo del capítulo, pasado a local
            return f'{g["p"][clave] - t0:.3f}'
        if tipo == 'p':
            v = g['p'][clave]
            return json.dumps(v) if not isinstance(v, str) else v
        palabra, _, n = clave.partition('#')
        t = cap.w(palabra, n=int(n or 1), fin=(tipo == 'f'))
        return f'{t - t0:.3f}'
    fuente = fuente.replace('/*AYUDA*/', open(os.path.join(AQUI, 'ayuda.js')).read())
    fuente = re.sub(r'/\*DATOS:(\w+)\*/', lambda m: open(os.path.join(RAIZ, 'graficos', 'datos', m.group(1) + '.txt')).read(), fuente)
    fuente = fuente.replace('/*FUENTES*/', '\n'.join(l for l in CSS.splitlines() if '@font-face' in l))
    s = re.sub(r'\{\{(w|f|p|t):([^}]+)\}\}', sustituye, fuente)
    return s.replace('{{id}}', g['id']).replace('{{dur}}', f'{g["hasta"] - t0:.3f}').replace('{{desde}}', f'{t0:.3f}')


# ---------------------------------------------------------------- índice y sonido

def automatizacion(puntos):
    return html.escape(json.dumps({'version': 1, 'lanes': [{'target': 'volume', 'points':
                       [{'t': r3(t), 'v': round(v, 3)} for t, v in puntos]}]}), quote=True)


def musica_puntos(cap):
    """La música bajo la voz: más presente con el rótulo, en los silencios largos y al final."""
    d, ult = cap.dur, cap.ultima()
    bajo = cap.musica.get('bajo', 0.2)
    p = [(0, 0), (1.2, 0.34), (VOZ0 - 0.4, 0.34), (VOZ0 + 0.1, bajo)]
    for (a, b, v) in sorted(cap.musica.get('subidas', [])):
        p += [(a - 0.4, bajo), (a, v), (b, v), (b + 0.5, bajo)]
    p += [(ult, bajo), (ult + 0.7, 0.36), (d - 1.3, 0.36), (d - 0.05, 0)]
    return sorted(p)


VOZ_FX = html.escape(json.dumps({'version': 1, 'nodes': [
    {'type': 'highpass', 'id': 'v1', 'label': 'Quitar graves', 'params': {'frequency': 90}},
    {'type': 'peaking', 'id': 'v2', 'label': 'Claridad', 'params': {'frequency': 3000, 'gain': 2, 'q': 1}},
    {'type': 'limiter', 'id': 'v3', 'params': {'limit': -1}}]}), quote=True)
AGUA_FX = html.escape(json.dumps({'version': 1, 'nodes': [
    {'type': 'lowpass', 'id': 'm1', 'label': 'Bajo el agua', 'params': {'frequency': 420}}]}), quote=True)


def indice(cap, tomas, sonidos):
    hosts = [f'''      <div id="planchas" data-composition-id="planchas" data-composition-src="compositions/planchas.html"
        data-start="0" data-duration="{cap.dur}" data-track-index="1" data-track-kind="graphics" style="z-index: 1"></div>''']
    for g in cap.graficos:
        hosts.append(f'''      <div id="{g["id"]}" data-composition-id="{g["id"]}" data-composition-src="compositions/{g["id"]}.html"
        data-start="{g["desde"]}" data-duration="{r3(g["hasta"] - g["desde"])}" data-track-index="2" data-track-kind="graphics" style="z-index: {g["z"]}"></div>''')
    for tm in tomas:
        hosts.append(f'''      <div id="{tm["tid"]}" data-composition-id="{tm["tid"]}" data-composition-src="compositions/{tm["tid"]}.html"
        data-start="{tm["desde"]}" data-duration="{r3(tm["hasta"] - tm["desde"])}" data-track-index="4" data-track-kind="graphics" style="z-index: 5"></div>''')
    voz = cap.voz['duracion']
    audios = [f'''      <audio id="voz" class="clip" src="assets/audio/voz.wav" data-start="{VOZ0}" data-duration="{voz}" data-track-index="10"
        data-volume="1" data-fx-chain="{VOZ_FX}"></audio>''',
              f'''      <audio id="musica" class="clip" src="assets/audio/musica.wav" data-start="0" data-duration="{cap.dur}" data-track-index="11"
        data-timeline-role="music" data-automation="{automatizacion(musica_puntos(cap))}"></audio>''']
    for i, s in enumerate(sonidos):
        extra = ''
        if s['ini']:
            extra += f' data-media-start="{s["ini"]}"'
        if s['fi']:
            extra += f' data-fade-in="{s["fi"]}"'
        if s['fo']:
            extra += f' data-fade-out="{s["fo"]}"'
        if s['fx'] == 'agua':
            extra += f' data-fx-chain="{AGUA_FX}"'
        audios.append(f'''      <audio id="s{i}-{s["nombre"]}" class="clip" src="assets/sfx/{s["archivo"]}" data-start="{s["t"]}" data-duration="{s["dur"]}"
        data-track-index="{12 + i}" data-volume="{s["vol"]}"{extra}></audio>''')
    return f'''<!doctype html>
<html lang="es" data-composition-variables='[
  {{"id":"color-ground","type":"color","label":"Fondo","default":"#0d1114"}},
  {{"id":"color-ink","type":"color","label":"Texto","default":"{TINTA}"}},
  {{"id":"color-accent","type":"color","label":"Acento","default":"{ACENTO}"}}
]'>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>El mecanismo de Anticitera · {cap.numero}. {html.escape(cap.titulo)}</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      :root {{ --color-ground: #0d1114; --color-ink: {TINTA}; --color-accent: {ACENTO}; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: var(--color-ground); }}
      #root {{ position: relative; width: 1920px; height: 1080px; overflow: hidden; }}
      #fondo {{ position: absolute; inset: 0; background: var(--color-ground); }}
    </style>
  </head>
  <body>
    <!-- Generado por videos/anticitera/kit/montar.py desde montaje/{cap.id}.py: editar allí y volver a montar. -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{cap.dur}" data-width="1920" data-height="1080">
      <div id="fondo"></div>
{chr(10).join(hosts)}
{chr(10).join(audios)}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
'''


# ---------------------------------------------------------------- recursos

def provisional(destino, tipo):
    """Plancha provisional (para montar antes de que FLUX acabe): gris oscuro, profundidad plana."""
    from PIL import Image
    if tipo == 'frente':
        Image.new('RGBA', (1920, 1080), (0, 0, 0, 0)).save(destino)
    elif tipo == 'prof':
        Image.new('RGB', (1920, 1080), (90, 90, 0)).save(destino)
    else:
        Image.new('RGB', (1920, 1080), (38, 42, 44)).save(destino, quality=90)


def copiar_recursos(cap, borrador):
    d = os.path.join(RAIZ, cap.id, 'assets')
    for sub in ('img', 'audio', 'sfx', 'fonts'):
        os.makedirs(os.path.join(d, sub), exist_ok=True)
    P = os.path.join(TRABAJO, 'planchas')
    faltan = []
    for tm in cap.tomas:
        n = tm['nombre']
        archivos = [('.jpg', 'img'), ('_prof.png', 'prof')] if tm.get('capas') is False else \
            [('_fondo.jpg', 'img'), ('_frente.png', 'frente'), ('_prof.png', 'prof')]
        for suf, tipo in archivos:
            src, dst = os.path.join(P, n + suf), os.path.join(d, 'img', n + suf)
            if os.path.exists(src):
                if not os.path.exists(dst) or os.path.getmtime(src) > os.path.getmtime(dst):
                    shutil.copy2(src, dst)
            elif borrador:
                if not os.path.exists(dst):
                    provisional(dst, tipo)
                faltan.append(n + suf)
            else:
                raise SystemExit(f'{cap.id}: falta la plancha {src}')
    shutil.copy2(os.path.join(TRABAJO, 'voz', cap.id + '.wav'), os.path.join(d, 'audio', 'voz.wav'))
    m = os.path.join(TRABAJO, 'musica', cap.id + '.wav')
    if os.path.exists(m):
        shutil.copy2(m, os.path.join(d, 'audio', 'musica.wav'))
    elif borrador:
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', f'anullsrc=r=32000:cl=stereo', '-t', str(cap.dur),
                        os.path.join(d, 'audio', 'musica.wav')], check=True)
        faltan.append('música')
    else:
        raise SystemExit(f'{cap.id}: falta la música {m}')
    for f in FUENTES:
        shutil.copy2(os.path.join(TRABAJO, 'fuentes', f), os.path.join(d, 'fonts', f))
    for f in cap.p_fuentes if hasattr(cap, 'p_fuentes') else []:
        shutil.copy2(os.path.join(TRABAJO, 'fuentes', f), os.path.join(d, 'fonts', f))
    for g in cap.graficos:   # imágenes propias de un gráfico (la radiografía de una plancha, por ejemplo)
        for f in g['p'].get('archivos', []):
            shutil.copy2(os.path.join(P, f), os.path.join(d, 'img', f))
    for s in cap.sonidos:
        nombre = SFX[s['nombre']]
        src = os.path.join(SFX_HF, nombre[3:]) if nombre.startswith('hf:') else os.path.join(TRABAJO, 'sfx', nombre)
        s['archivo'] = s['nombre'] + os.path.splitext(src)[1]
        shutil.copy2(src, os.path.join(d, 'sfx', s['archivo']))
        if s['dur'] is None:
            s['dur'] = r3(min(duracion_audio(src) - s['ini'], cap.dur - s['t']))
        s['dur'] = r3(min(s['dur'], cap.dur - s['t'], duracion_audio(src) - s['ini']))
    return faltan


def montar(cid, borrador=False):
    cap = cargar(cid)
    destino = os.path.join(RAIZ, cid)
    comp = os.path.join(destino, 'compositions')
    os.makedirs(comp, exist_ok=True)
    for f in os.listdir(comp):
        if f.endswith('.html'):
            os.remove(os.path.join(comp, f))
    # El rótulo del capítulo, sobre la primera toma.
    cap.bloques.insert(0, dict(x=150, y=380, partes=[E(f'CAPÍTULO {cap.numero}', 0.4), T(cap.titulo, 0.72, tam=118)],
                               sale=r3(VOZ0 - 0.35), der=False, ancho=cap.titulo_ancho, id=f'{cid}-titulo'))
    faltan = copiar_recursos(cap, borrador)
    tomas = sorted(cap.tomas, key=lambda x: x['desde'])
    js = tomas_js(cap)
    for i, tm in enumerate(tomas):
        tm['tid'] = f't{i + 1}'
        tm['hasta'] = tomas[i + 1]['desde'] if i + 1 < len(tomas) else cap.dur
    avisos = []
    for tm in tomas:
        dentro = lambda t: tm['desde'] <= t < tm['hasta']
        bl = [b for b in cap.bloques if dentro(min(p.t for p in b['partes']))]
        gu = [g for g in cap.guias if dentro(g['t'])]
        for b in bl:
            if b['sale'] > tm['hasta'] - 0.15:
                avisos.append(f'{cid}: el bloque «{b["partes"][0].texto}» sale en {b["sale"]} s, tras el fin de su toma ({tm["hasta"]:.2f} s)')
        open(os.path.join(comp, tm['tid'] + '.html'), 'w').write(comp_textos(cid, tm, bl, gu, avisos))
    motor = open(os.path.join(AQUI, 'planchas.html')).read()
    open(os.path.join(comp, 'planchas.html'), 'w').write(
        motor.replace('/*TOMAS*/', json.dumps(js, ensure_ascii=False, separators=(',', ':'))))
    for g in cap.graficos:
        open(os.path.join(comp, g['id'] + '.html'), 'w').write(comp_grafico(cap, g))
    open(os.path.join(destino, 'index.html'), 'w').write(indice(cap, tomas, cap.sonidos))
    open(os.path.join(destino, 'hyperframes.json'), 'w').write(open(os.path.join(RAIZ, 'apertura', 'hyperframes.json')).read())
    json.dump({'id': f'anticitera-{cid}', 'name': f'anticitera-{cid}'}, open(os.path.join(destino, 'meta.json'), 'w'), indent=2)
    print(json.dumps({'capitulo': cid, 'duracion': cap.dur, 'tomas': len(tomas), 'graficos': len(cap.graficos),
                      'sonidos': len(cap.sonidos), 'provisionales': len(faltan)}, ensure_ascii=False))
    for a in avisos:
        print('aviso:', a)
    for palabra, ts in cap.ambiguas.items():
        print(f'nota: «{palabra}» sale {len(ts)} veces ({", ".join(f"{t:.1f}" for t in ts)} s); se usa la primera')


if __name__ == '__main__':
    montar(sys.argv[1], borrador='--borrador' in sys.argv)
