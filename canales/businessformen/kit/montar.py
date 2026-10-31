"""
Monta un vídeo de BusinessForMen como proyecto de HyperFrames a partir de su montaje (videos/<vídeo>/montaje.py),
sus escenas (videos/<vídeo>/escenas/*.html, una plantilla por escena) y los tiempos de su narración
(salidas/businessformen/<vídeo>/voz/voz.json). Escribe videos/<vídeo>/proyecto/ y copia sus recursos.

  python3 canales/businessformen/kit/montar.py 01-flujo-de-caja
  python3 canales/businessformen/kit/montar.py cortos/01-la-clausula      (un corto: canales/businessformen/cortos/…)
  python3 canales/businessformen/kit/montar.py --canal canales/geografia cortos/01-chile     (otro canal con este kit)

Otro canal: su carpeta trae marca/marca.css (y, si quiere, marca/corto.css) y marca/canal.json (nombre, fondo y estilo de
los subtítulos); sus fuentes van en salidas/<canal>/marca/fuentes y su trabajo en salidas/<canal>/<vídeo>.

En montaje.py hay disponibles:
  formato(ancho, alto, voz0=…, cola=…, desenfoque=False)  el lienzo y la entrada de la voz (por defecto 1920 × 1080,
                                         voz a 0,8 s); desenfoque=True: desenfoque de movimiento de HyperFrames. Va
                                         antes de cualquier w(). Un corto vertical: formato(1080, 1920, voz0=0.1, cola=0.4)
  subtitulos(**estilo)                   subtítulos quemados, en grupos de pocas palabras con la palabra que suena en un
                                         bloque rojo (los cortos: muchos los ven sin sonido)
  sin_subtitulos(desde, hasta)           los quita en un tramo (cuando la escena ya escribe en grande lo que dice la voz)
  w("palabra", n=1, fin=False, mas=0.0)   tiempo en el vídeo de esa palabra (n: la aparición n)
  VOZ0                                   entrada de la voz
  escena(id, plantilla, desde, **p)      una escena: subcomposición escenas/<plantilla>.html; acaba donde empieza
                                         la siguiente (o en DURACION). p son sus parámetros. Con entrada=… la escena
                                         entra sobre la anterior, que sigue debajo mientras dura la transición:
                                         "cortina" (el rojo de la marca la cruza y la descubre), "barrido" (de derecha a
                                         izquierda, con un filo rojo), "subida" (de abajo arriba) o {"tipo": "iris",
                                         "x": 540, "y": 700} (un círculo que se abre desde ese punto)
  sonido(nombre, t, vol=1, dur=None, ini=0, fi=0, fo=0)   efectos: los de la biblioteca de HyperFrames (SFX) o un WAV
                                         propio, <trabajo>/sfx/<nombre>.wav o su carpeta de al lado (BigSoundBank, CC0)
  musica(nombre, desde, hasta, vol=0.3, fi=0.6, fo=1.0, puntos=[(t, v)])   lecho de música (musica/<nombre>.wav)
  DURACION = ...                         duración del vídeo (si no, la última palabra más COLA)
  AQUI                                   la carpeta del vídeo (para leer sus recursos/)

En las plantillas de escena:
  {{ID}}            el id de la escena (también su composición): los selectores van con #{{ID}}
  {{ANCHO}}, {{ALTO}} el lienzo (1920 × 1080, o 1080 × 1920 en un corto)
  {{DUR}}           su duración; {{T0}}, su comienzo en el vídeo
  {{p:clave}}       un parámetro (JSON si no es texto)
  /*MARCA*/         el CSS de la marca (fuentes, colores, clases comunes), dentro de <style>
  /*CORTO*/         el CSS común de los cortos verticales (kit/corto.css): zona segura y tamaños para el móvil
  Una plantilla que no está en escenas/ se busca en la carpeta comun/ de al lado (cortos/comun/: golpe rojo, foto…).
  /*AYUDA*/         las ayudas de JS: w("palabra", n), f("palabra", n) y serie("palabra", k, n) en tiempo local, fmt(),
                    cuenta(), sube(), trocea(), cortina(), alBuscar()…
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
CANAL = os.path.dirname(AQUI)
REPO = os.path.dirname(os.path.dirname(CANAL))
H = os.environ.get('HERRAMIENTAS', os.path.expanduser('~/herramientas-videos'))
SFX_HF = os.path.join(H, 'hyperframes/node_modules/hyperframes/dist/skills/media-use/audio/assets/sfx')
SLUG = 'businessformen'
FUENTES = os.path.join(REPO, 'salidas', SLUG, 'marca', 'fuentes')
# Lo propio de cada canal (por defecto, BusinessForMen): ver configurar().
CONF = dict(nombre='BusinessForMen', prefijo='bfm', fondo='#0a0b0d',
            subtitulos=dict(fuente='intertight-800.woff2', familia='Inter Tight', peso=800, color='#f4f3f0',
                            resalte='176, 18, 47'))
VOZ0 = 0.8
COLA = 2.0
# Transiciones de entrada de una escena sobre la anterior (ayuda.js, entradaEscena) y lo que duran.
ENTRADAS = {'cortina': 0.5, 'barrido': 0.42, 'subida': 0.42, 'iris': 0.5}
SFX = {n: 'hf:' + n + '.mp3' for n in ('chime', 'click', 'click-soft', 'impact-bass-1', 'impact-bass-2', 'key-press', 'pop',
                                         'riser', 'typing', 'whoosh', 'whoosh-cinematic', 'whoosh-short', 'glitch-1')}


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


class Video:
    def __init__(self, vid):
        self.id = vid
        self.dir = os.path.join(CANAL, vid) if '/' in vid else os.path.join(CANAL, 'videos', vid)
        self.trabajo = os.environ.get('TRABAJO', os.path.join(REPO, 'salidas', SLUG, vid))
        self.voz = json.load(open(os.path.join(self.trabajo, 'voz', 'voz.json')))
        self.palabras = [p for f in self.voz['frases'] for p in f['palabras']]
        self.escenas, self.sonidos, self.musicas = [], [], []
        self.ancho, self.alto, self.voz0, self.desenfoque = 1920, 1080, VOZ0, False
        self.dur = r3(self.voz0 + self.voz['duracion'] + COLA)
        self.subs, self.sin_subs = None, []

    def w(self, palabra, n=1, fin=False, mas=0.0):
        busca = [limpia(x) for x in palabra.split()]
        hechas = [i for i in range(len(self.palabras) - len(busca) + 1)
                  if all(limpia(self.palabras[i + j]['texto']) == b for j, b in enumerate(busca))]
        if len(hechas) < n:
            raise SystemExit(f'{self.id}: no está «{palabra}» (aparición {n})')
        i = hechas[n - 1]
        p = self.palabras[i + len(busca) - 1] if fin else self.palabras[i]
        return r3(self.voz0 + (p['fin'] if fin else p['inicio']) + mas)

    def mapa(self):
        """Cada palabra (limpia) con sus apariciones [[inicio, fin], ...] en el tiempo del vídeo."""
        m = {}
        for p in self.palabras:
            m.setdefault(limpia(p['texto']), []).append([r3(self.voz0 + p['inicio']), r3(self.voz0 + p['fin'])])
        return m


def cargar(vid):
    v = Video(vid)

    def escena(id, plantilla, desde, **p):
        entrada = p.pop('entrada', None)
        if isinstance(entrada, str):
            entrada = {'tipo': entrada}
        if entrada:
            entrada.setdefault('d', ENTRADAS[entrada['tipo']])
        v.escenas.append(dict(id=id, plantilla=plantilla, desde=r3(desde), p=p, entrada=entrada))

    def sonido(nombre, t, vol=1.0, dur=None, ini=0, fi=0, fo=0):
        v.sonidos.append(dict(nombre=nombre, t=r3(t), vol=vol, dur=dur, ini=ini, fi=fi, fo=fo))

    def musica(nombre, desde, hasta, vol=0.3, fi=0.6, fo=1.0, puntos=None):
        v.musicas.append(dict(nombre=nombre, desde=r3(desde), hasta=r3(hasta), vol=vol, fi=fi, fo=fo, puntos=puntos or []))

    def formato(ancho, alto, voz0=VOZ0, cola=COLA, desenfoque=False):
        v.ancho, v.alto, v.voz0, v.desenfoque = ancho, alto, voz0, desenfoque
        v.dur = r3(voz0 + v.voz['duracion'] + cola)
        nombres['VOZ0'] = voz0

    def subtitulos(**estilo):
        v.subs = estilo

    def sin_subtitulos(desde, hasta):
        v.sin_subs.append((r3(desde), r3(hasta)))

    nombres = dict(w=v.w, VOZ0=VOZ0, escena=escena, sonido=sonido, musica=musica, AQUI=v.dir, formato=formato,
                   subtitulos=subtitulos, sin_subtitulos=sin_subtitulos)
    ruta = os.path.join(v.dir, 'montaje.py')
    exec(compile(open(ruta).read(), ruta, 'exec'), nombres)
    if 'DURACION' in nombres:
        v.dur = r3(nombres['DURACION'])
    v.escenas.sort(key=lambda e: e['desde'])
    for i, e in enumerate(v.escenas):
        e['hasta'] = v.escenas[i + 1]['desde'] if i + 1 < len(v.escenas) else v.dur
        # Si la siguiente entra con una transición, esta sigue debajo mientras dura.
        sig = v.escenas[i + 1]['entrada'] if i + 1 < len(v.escenas) else None
        e['solape'] = sig['d'] if sig else 0
    return v


def plantilla(v, nombre):
    for ruta in (os.path.join(v.dir, 'escenas', nombre + '.html'), os.path.join(os.path.dirname(v.dir), 'comun', nombre + '.html')):
        if os.path.exists(ruta):
            return open(ruta).read()
    raise SystemExit(f'{v.id}: no está la plantilla «{nombre}» (ni en escenas/ ni en ../comun/)')


def comp_escena(v, e, marca_css, ayuda_js):
    fuente = plantilla(v, e['plantilla'])
    dur = r3(e['hasta'] - e['desde'])

    def parametro(m):
        val = e['p'][m.group(1)]
        return val if isinstance(val, str) else json.dumps(val, ensure_ascii=False)

    s = fuente.replace('/*MARCA*/', marca_css).replace('/*AYUDA*/', ayuda_js)
    s = s.replace('/*CORTO*/', open(propio('corto.css')).read())
    s = s.replace('/*ENTRADA*/null', json.dumps(e.get('entrada')))
    s = s.replace('/*W*/', json.dumps(v.mapa(), ensure_ascii=False, separators=(',', ':')))
    s = s.replace('/*L*/', json.dumps([[limpia(q['texto']), r3(v.voz0 + q['inicio']), r3(v.voz0 + q['fin'])] for q in v.palabras],
                                      ensure_ascii=False, separators=(',', ':')))
    s = re.sub(r'\{\{p:(\w+)\}\}', parametro, s)
    s = s.replace('{{ID}}', e['id']).replace('{{DUR}}', f'{dur:.3f}').replace('{{T0}}', f'{e["desde"]:.3f}')
    s = s.replace('{{ANCHO}}', str(v.ancho)).replace('{{ALTO}}', str(v.alto))
    return s


def grupos_subtitulos(v):
    """Grupos de 1–4 palabras con su tiempo, escritos como se leen (kit/subtitulos.py: nombres y cifras)."""
    sys.path.insert(0, AQUI)
    import subtitulos as st
    ruta = os.path.join(v.dir, 'recursos', 'pantalla.json')
    pantalla = {k: x for k, x in json.load(open(ruta)).items() if not k.startswith('_')} if os.path.exists(ruta) else {}
    grupos = []
    for f in v.voz['frases']:
        toks = st.nombres([dict(p) for p in f['palabras']], pantalla)
        # «cinco por ciento» → «5 %»: se marca antes de pasar las cifras (si no, «ciento» se vuelve «100»).
        k = 0
        while k + 2 < len(toks):
            if limpia(toks[k + 1]['texto']) == 'por' and limpia(toks[k + 2]['texto']) == 'ciento':
                cola = re.search(r'[.,:;?!]*$', toks[k + 2]['texto']).group(0)
                toks[k + 1:k + 3] = [dict(texto='§%' + cola, inicio=toks[k + 1]['inicio'], fin=toks[k + 2]['fin'])]
            k += 1
        toks = st.cifras(toks)
        k = 0
        while k + 1 < len(toks):
            if toks[k + 1]['texto'].startswith('§%'):
                n = st.NUMERO.get(limpia(toks[k]['texto']), toks[k]['texto'])
                toks[k:k + 2] = [dict(texto=f'{n} %' + toks[k + 1]['texto'][2:], inicio=toks[k]['inicio'], fin=toks[k + 1]['fin'])]
            k += 1
        actual = []
        for j, t in enumerate(toks):
            actual.append(t)
            texto = ' '.join(x['texto'] for x in actual)
            fin_frase = re.search(r'[.,:;?!]$', t['texto'])
            lleno = len(actual) >= 3 or len(texto) >= 16
            # No se parte un nombre propio de varias palabras («Estados | Unidos», «Bill | Gates»).
            nombre = j + 1 < len(toks) and t['texto'][:1].isupper() and toks[j + 1]['texto'][:1].isupper()
            # Ni una cantidad de su unidad («75.000 | dólares», «tres | meses»).
            cifra = j + 1 < len(toks) and not t['texto'].endswith('%') and (t['texto'][:1].isdigit() or limpia(t['texto']) in st.NUMERO)
            if fin_frase or (lleno and limpia(t['texto']) not in st.DEBIL and not nombre and not cifra) or len(actual) >= 5:
                grupos.append(actual)
                actual = []
        if actual:
            grupos.append(actual)
    out = []
    for i, g in enumerate(grupos):
        a, b = v.voz0 + g[0]['inicio'] - 0.04, v.voz0 + g[-1]['fin'] + 0.3
        if i + 1 < len(grupos):
            sig = v.voz0 + grupos[i + 1][0]['inicio'] - 0.04
            b = sig if sig - (v.voz0 + g[-1]['fin']) < 0.6 else b
        tapado = sum(max(0, min(b, h) - max(a, d)) for d, h in v.sin_subs)
        if tapado > 0.5 * (b - a):
            continue
        out.append(dict(desde=r3(max(0.05, a)), hasta=r3(min(b, v.dur)),
                        palabras=[[re.sub(r'[.,:;]$', '', x['texto']), r3(v.voz0 + x['inicio']), r3(v.voz0 + x['fin'])] for x in g]))
    return out


def comp_subtitulos(v):
    e = dict(top=1168, tam=64, **(v.subs or {}))
    st = CONF['subtitulos']
    r = st['resalte']
    grupos = grupos_subtitulos(v)
    filas = []
    for i, g in enumerate(grupos):
        palabras = ' '.join(f'<span>{html.escape(p[0])}</span>' for p in g['palabras'])
        filas.append(f'<div class="g" id="sub{i}">{palabras}</div>')
    datos = json.dumps([[g['desde'], g['hasta'], [[p[1], p[2]] for p in g['palabras']]] for g in grupos], separators=(',', ':'))
    return f'''<template>
  <!-- Subtítulos quemados (generados por kit/montar.py): grupos cortos y la palabra que suena en un bloque rojo. -->
  <style>
    @font-face {{ font-family: "{st['familia']}"; src: url("assets/fonts/{st['fuente']}") format("woff2"); font-weight: {st['peso']}; }}
    #subs {{ position: absolute; inset: 0; }}
    #subs .g {{ position: absolute; left: 0; right: 0; top: {e['top']}px; padding: 0 96px; text-align: center; visibility: hidden;
      font: {st['peso']} {e['tam']}px/1.14 "{st['familia']}", sans-serif; letter-spacing: -0.012em; color: {st['color']};
      text-shadow: 0 2px 16px rgba(0, 0, 0, 0.6), 0 0 3px rgba(0, 0, 0, 0.5); }}
    #subs .g span {{ display: inline-block; padding: 0.02em 0.13em 0.07em; }}
  </style>
  <div data-composition-id="subs" data-width="{v.ancho}" data-height="{v.alto}">
    <div id="subs">
      {(chr(10) + '      ').join(filas)}
    </div>
  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
      const G = {datos};
      G.forEach(([a, b, ps], i) => {{
        const g = document.getElementById("sub" + i), sp = g.querySelectorAll("span");
        tl.fromTo(g, {{ autoAlpha: 0, y: 10 }}, {{ autoAlpha: 1, y: 0, duration: 0.12, ease: "power3.out" }}, a);
        ps.forEach(([t0, t1], k) => {{
          const fin = k + 1 < ps.length ? ps[k + 1][0] : b;
          tl.fromTo(sp[k], {{ backgroundColor: "rgba({r}, 0)", textShadow: "0 2px 16px rgba(0, 0, 0, 0.6)", color: "{st['color']}" }},
            {{ backgroundColor: "rgba({r}, 1)", textShadow: "0 0 0 rgba(0, 0, 0, 0)", color: "{st.get('color_resalte', st['color'])}", duration: 0.05 }}, Math.max(a, t0 - 0.03));
          tl.to(sp[k], {{ backgroundColor: "rgba({r}, 0)", textShadow: "0 2px 16px rgba(0, 0, 0, 0.6)", color: "{st['color']}", duration: 0.05 }}, Math.max(t0, fin - 0.05));
        }});
        tl.to(g, {{ opacity: 0, duration: 0.08, ease: "power2.in" }}, b - 0.08);
        tl.set(g, {{ visibility: "hidden" }}, b);
      }});
      tl.set({{}}, {{}}, {v.dur});
      window.__timelines["subs"] = tl;
    }})();
  </script>
</template>
'''


def ruta_sfx(v, nombre):
    """El archivo de un efecto: de la biblioteca de HyperFrames, o un WAV propio del vídeo (o de la carpeta de al lado)."""
    if nombre in SFX:
        return os.path.join(SFX_HF, SFX[nombre].split(':', 1)[1])
    for d in (os.path.join(v.trabajo, 'sfx'), os.path.join(os.path.dirname(v.trabajo), 'sfx')):
        if os.path.exists(os.path.join(d, nombre + '.wav')):
            return os.path.join(d, nombre + '.wav')
    raise SystemExit(f'{v.id}: no está el efecto «{nombre}»')


def audio_html(v, avisos):
    out, pista = [], 20
    voz = os.path.join(v.trabajo, 'voz', 'voz.wav')
    dv = min(duracion_audio(voz), v.dur - v.voz0)
    cadena = {'version': 1, 'nodes': [{'type': 'highpass', 'id': 'v1', 'params': {'frequency': 90}},
                                      {'type': 'peaking', 'id': 'v2', 'params': {'frequency': 3000, 'gain': 2, 'q': 1}},
                                      {'type': 'limiter', 'id': 'v3', 'params': {'limit': -1}}]}
    out.append(f'<audio id="voz" class="clip" src="assets/audio/voz.wav" data-start="{v.voz0}" data-duration="{dv:.3f}" '
               f'data-track-index="10" data-volume="1" data-fx-chain="{html.escape(json.dumps(cadena))}"></audio>')
    for i, m in enumerate(v.musicas):
        largo = r3(m['hasta'] - m['desde'])
        pieza = os.path.join(v.trabajo, 'musica', m['nombre'] + '.wav')
        if duracion_audio(pieza) < largo - 0.05:
            avisos.append(f'música «{m["nombre"]}»: la pieza dura {duracion_audio(pieza):.1f} s y el tramo {largo:.1f} s (haz un lecho)')
        pts = [(0, 0), (m['fi'], m['vol'])] + [(r3(t - m['desde']), x) for t, x in m['puntos']] + \
              [(r3(largo - m['fo']), m['vol']), (largo, 0)]
        pts = sorted(pts, key=lambda q: q[0])
        auto = {'version': 1, 'lanes': [{'target': 'volume', 'points': [{'t': t, 'v': x} for t, x in pts]}]}
        out.append(f'<audio id="musica-{i}" class="clip" src="assets/audio/{m["nombre"]}.wav" data-start="{m["desde"]}" '
                   f'data-duration="{largo}" data-track-index="{11 + (i % 2)}" data-timeline-role="music" '
                   f'data-automation="{html.escape(json.dumps(auto))}"></audio>')
    for i, s in enumerate(v.sonidos):
        ruta = ruta_sfx(v, s['nombre'])
        archivo = os.path.basename(ruta)
        dur = s['dur'] or duracion_audio(ruta) - s['ini']
        dur = min(dur, duracion_audio(ruta) - s['ini'])
        extra = (f' data-media-start="{s["ini"]}"' if s['ini'] else '') + (f' data-fade-in="{s["fi"]}"' if s['fi'] else '') + \
                (f' data-fade-out="{s["fo"]}"' if s['fo'] else '')
        out.append(f'<audio id="sfx-{i}" class="clip" src="assets/sfx/{archivo}" data-start="{s["t"]}" data-duration="{dur:.3f}" '
                   f'data-track-index="{pista + i % 12}" data-volume="{s["vol"]}"{extra}></audio>')
    return out


def escribir(v):
    p = os.path.join(v.dir, 'proyecto')
    if os.path.isdir(os.path.join(p, 'compositions')):
        shutil.rmtree(os.path.join(p, 'compositions'))
    os.makedirs(os.path.join(p, 'compositions'), exist_ok=True)
    marca_css = open(propio('marca.css')).read()
    ayuda_js = open(os.path.join(AQUI, 'ayuda.js')).read()
    avisos, anfitriones = [], []
    for i, e in enumerate(v.escenas):
        open(os.path.join(p, 'compositions', e['id'] + '.html'), 'w').write(comp_escena(v, e, marca_css, ayuda_js))
        # Cada escena, encima de la anterior (las transiciones las solapan) y en pistas alternas del Studio.
        anfitriones.append(f'<div id="h-{e["id"]}" data-composition-id="{e["id"]}" data-composition-src="compositions/{e["id"]}.html" '
                           f'data-start="{e["desde"]}" data-duration="{r3(min(e["hasta"] + e["solape"], v.dur) - e["desde"])}" '
                           f'data-track-index="{1 + 2 * (i % 2)}" data-track-kind="graphics" style="z-index: {1 + i}"></div>')
    if v.subs is not None:
        open(os.path.join(p, 'compositions', 'subs.html'), 'w').write(comp_subtitulos(v))
        anfitriones.append(f'<div id="h-subs" data-composition-id="subs" data-composition-src="compositions/subs.html" '
                           f'data-start="0" data-duration="{v.dur}" data-track-index="2" data-track-kind="captions" style="z-index: 30"></div>')
    frames = round(v.dur * 30)
    A, B = v.ancho, v.alto
    indice = f'''<!doctype html>
<!-- Generado por canales/businessformen/kit/montar.py desde {os.path.relpath(v.dir, REPO)}/montaje.py: no editar a mano. -->
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={A}, height={B}" />
    <title>{CONF['nombre']} · {v.id.replace('/', ' · ')}</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: {A}px; height: {B}px; overflow: hidden; background: {CONF['fondo']}; }}
      #root {{ position: relative; width: {A}px; height: {B}px; overflow: hidden; background: {CONF['fondo']}; }}
      #grano {{ position: absolute; inset: 0; background: url("assets/img/grano.png"); opacity: 0.05; mix-blend-mode: overlay; z-index: 50; pointer-events: none; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{v.dur}" data-width="{A}" data-height="{B}"{' data-motion-blur="on"' if v.desenfoque else ''}>
      {(chr(10) + '      ').join(anfitriones)}
      <div id="grano"></div>
      {(chr(10) + '      ').join(audio_html(v, avisos))}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      // Grano: la textura (512 px, repetida) salta 137 × 251 px en cada cuadro; con steps, igual en cada render.
      tl.fromTo("#grano", {{ backgroundPosition: "0px 0px" }}, {{ backgroundPosition: "{137 * frames}px {251 * frames}px", duration: {v.dur}, ease: "steps({frames})" }}, 0);
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
    open(os.path.join(p, 'index.html'), 'w').write(indice)
    for f in ('hyperframes.json',):
        origen = os.path.join(CANAL, 'marca', 'plantillas', f)
        shutil.copy2(origen if os.path.exists(origen) else os.path.join(os.path.dirname(AQUI), 'marca', 'plantillas', f),
                     os.path.join(p, f))
    with open(os.path.join(p, 'meta.json'), 'w') as fh:
        ident = CONF['prefijo'] + '-' + v.id.replace('/', '-')
        json.dump({'id': ident, 'name': ident}, fh, indent=2)
    # Recursos: voz, músicas, imágenes, fuentes y efectos.
    a = os.path.join(p, 'assets')
    for sub in ('audio', 'img', 'fonts', 'sfx'):
        os.makedirs(os.path.join(a, sub), exist_ok=True)
    shutil.copy2(os.path.join(v.trabajo, 'voz', 'voz.wav'), os.path.join(a, 'audio', 'voz.wav'))
    for m in {m['nombre'] for m in v.musicas}:
        shutil.copy2(os.path.join(v.trabajo, 'musica', m + '.wav'), os.path.join(a, 'audio', m + '.wav'))
    for f in os.listdir(os.path.join(v.trabajo, 'img')):
        if f.endswith('.jpg') or f.endswith('_frente.png'):
            shutil.copy2(os.path.join(v.trabajo, 'img', f), os.path.join(a, 'img', f))
    for f in ('grano.png', 'desgaste.png'):
        origen = os.path.join(REPO, 'salidas', SLUG, 'marca', 'img', f)
        if not os.path.exists(origen):   # las texturas son las mismas para todos los canales
            origen = os.path.join(REPO, 'salidas', 'businessformen', 'marca', 'img', f)
        shutil.copy2(origen, os.path.join(a, 'img', f))
    for f in os.listdir(FUENTES):
        shutil.copy2(os.path.join(FUENTES, f), os.path.join(a, 'fonts', f))
    for s in {s['nombre'] for s in v.sonidos}:
        ruta = ruta_sfx(v, s)
        shutil.copy2(ruta, os.path.join(a, 'sfx', os.path.basename(ruta)))
    return avisos


def propio(nombre):
    """El archivo del canal (marca/<nombre>) si lo tiene; si no, el del kit."""
    ruta = os.path.join(CANAL, 'marca', nombre)
    return ruta if os.path.exists(ruta) else os.path.join(AQUI, nombre)


def configurar(canal):
    """Monta para otro canal: su carpeta (canales/<slug>), su marca y sus salidas."""
    global CANAL, SLUG, FUENTES
    CANAL = os.path.abspath(canal)
    SLUG = os.path.basename(CANAL.rstrip('/'))
    FUENTES = os.path.join(REPO, 'salidas', SLUG, 'marca', 'fuentes')
    conf = os.path.join(CANAL, 'marca', 'canal.json')
    if os.path.exists(conf):
        c = json.load(open(conf))
        CONF.update({k: x for k, x in c.items() if k != 'subtitulos'})
        CONF['subtitulos'] = dict(CONF['subtitulos'], **c.get('subtitulos', {}))


def main():
    args = sys.argv[1:]
    if args and args[0] == '--canal':
        configurar(args[1])
        args = args[2:]
    vid = args[0]
    v = cargar(vid)
    avisos = escribir(v)
    print(json.dumps({'video': vid, 'duracion': v.dur, 'escenas': len(v.escenas), 'sonidos': len(v.sonidos), 'musicas': len(v.musicas)}))
    for a in avisos:
        print('aviso:', a)
    limite = 4.5 if v.alto > v.ancho else 9      # un corto vertical cambia cada 1–3 s
    for e in v.escenas:
        d = e['hasta'] - e['desde']
        if d > limite:
            print(f'nota: la escena {e["id"]} dura {d:.1f} s: ¿pasa algo cada {"1–3" if v.alto > v.ancho else "3–5"} s?')


if __name__ == '__main__':
    main()
