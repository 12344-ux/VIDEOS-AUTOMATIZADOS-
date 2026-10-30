"""
Monta un vídeo de BusinessForMen como proyecto de HyperFrames a partir de su montaje (videos/<vídeo>/montaje.py),
sus escenas (videos/<vídeo>/escenas/*.html, una plantilla por escena) y los tiempos de su narración
(salidas/businessformen/<vídeo>/voz/voz.json). Escribe videos/<vídeo>/proyecto/ y copia sus recursos.

  python3 canales/businessformen/kit/montar.py 01-flujo-de-caja

En montaje.py hay disponibles:
  w("palabra", n=1, fin=False, mas=0.0)   tiempo en el vídeo de esa palabra (n: la aparición n)
  VOZ0                                   entrada de la voz
  escena(id, plantilla, desde, **p)      una escena: subcomposición escenas/<plantilla>.html; acaba donde empieza
                                         la siguiente (o en DURACION). p son sus parámetros
  sonido(nombre, t, vol=1, dur=None, ini=0, fi=0, fo=0)   efectos (ver SFX)
  musica(nombre, desde, hasta, vol=0.3, fi=0.6, fo=1.0, puntos=[(t, v)])   lecho de música (musica/<nombre>.wav)
  DURACION = ...                         duración del vídeo (si no, la última palabra más COLA)
  AQUI                                   la carpeta del vídeo (para leer sus recursos/)

En las plantillas de escena:
  {{ID}}            el id de la escena (también su composición): los selectores van con #{{ID}}
  {{DUR}}           su duración; {{T0}}, su comienzo en el vídeo
  {{p:clave}}       un parámetro (JSON si no es texto)
  /*MARCA*/         el CSS de la marca (fuentes, colores, clases comunes), dentro de <style>
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
FUENTES = os.path.join(REPO, 'salidas', 'businessformen', 'marca', 'fuentes')
VOZ0 = 0.8
COLA = 2.0
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
        self.dir = os.path.join(CANAL, 'videos', vid)
        self.trabajo = os.environ.get('TRABAJO', os.path.join(REPO, 'salidas', 'businessformen', vid))
        self.voz = json.load(open(os.path.join(self.trabajo, 'voz', 'voz.json')))
        self.palabras = [p for f in self.voz['frases'] for p in f['palabras']]
        self.escenas, self.sonidos, self.musicas = [], [], []
        self.dur = r3(VOZ0 + self.voz['duracion'] + COLA)

    def w(self, palabra, n=1, fin=False, mas=0.0):
        busca = [limpia(x) for x in palabra.split()]
        hechas = [i for i in range(len(self.palabras) - len(busca) + 1)
                  if all(limpia(self.palabras[i + j]['texto']) == b for j, b in enumerate(busca))]
        if len(hechas) < n:
            raise SystemExit(f'{self.id}: no está «{palabra}» (aparición {n})')
        i = hechas[n - 1]
        p = self.palabras[i + len(busca) - 1] if fin else self.palabras[i]
        return r3(VOZ0 + (p['fin'] if fin else p['inicio']) + mas)

    def mapa(self):
        """Cada palabra (limpia) con sus apariciones [[inicio, fin], ...] en el tiempo del vídeo."""
        m = {}
        for p in self.palabras:
            m.setdefault(limpia(p['texto']), []).append([r3(VOZ0 + p['inicio']), r3(VOZ0 + p['fin'])])
        return m


def cargar(vid):
    v = Video(vid)

    def escena(id, plantilla, desde, **p):
        v.escenas.append(dict(id=id, plantilla=plantilla, desde=r3(desde), p=p))

    def sonido(nombre, t, vol=1.0, dur=None, ini=0, fi=0, fo=0):
        v.sonidos.append(dict(nombre=nombre, t=r3(t), vol=vol, dur=dur, ini=ini, fi=fi, fo=fo))

    def musica(nombre, desde, hasta, vol=0.3, fi=0.6, fo=1.0, puntos=None):
        v.musicas.append(dict(nombre=nombre, desde=r3(desde), hasta=r3(hasta), vol=vol, fi=fi, fo=fo, puntos=puntos or []))

    nombres = dict(w=v.w, VOZ0=VOZ0, escena=escena, sonido=sonido, musica=musica, AQUI=v.dir)
    ruta = os.path.join(v.dir, 'montaje.py')
    exec(compile(open(ruta).read(), ruta, 'exec'), nombres)
    if 'DURACION' in nombres:
        v.dur = r3(nombres['DURACION'])
    v.escenas.sort(key=lambda e: e['desde'])
    for i, e in enumerate(v.escenas):
        e['hasta'] = v.escenas[i + 1]['desde'] if i + 1 < len(v.escenas) else v.dur
    return v


def comp_escena(v, e, marca_css, ayuda_js):
    fuente = open(os.path.join(v.dir, 'escenas', e['plantilla'] + '.html')).read()
    dur = r3(e['hasta'] - e['desde'])

    def parametro(m):
        val = e['p'][m.group(1)]
        return val if isinstance(val, str) else json.dumps(val, ensure_ascii=False)

    s = fuente.replace('/*MARCA*/', marca_css).replace('/*AYUDA*/', ayuda_js)
    s = s.replace('/*W*/', json.dumps(v.mapa(), ensure_ascii=False, separators=(',', ':')))
    s = s.replace('/*L*/', json.dumps([[limpia(q['texto']), r3(VOZ0 + q['inicio']), r3(VOZ0 + q['fin'])] for q in v.palabras],
                                      ensure_ascii=False, separators=(',', ':')))
    s = re.sub(r'\{\{p:(\w+)\}\}', parametro, s)
    s = s.replace('{{ID}}', e['id']).replace('{{DUR}}', f'{dur:.3f}').replace('{{T0}}', f'{e["desde"]:.3f}')
    return s


def audio_html(v, avisos):
    out, pista = [], 20
    voz = os.path.join(v.trabajo, 'voz', 'voz.wav')
    dv = min(duracion_audio(voz), v.dur - VOZ0)
    cadena = {'version': 1, 'nodes': [{'type': 'highpass', 'id': 'v1', 'params': {'frequency': 90}},
                                      {'type': 'peaking', 'id': 'v2', 'params': {'frequency': 3000, 'gain': 2, 'q': 1}},
                                      {'type': 'limiter', 'id': 'v3', 'params': {'limit': -1}}]}
    out.append(f'<audio id="voz" class="clip" src="assets/audio/voz.wav" data-start="{VOZ0}" data-duration="{dv:.3f}" '
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
        archivo = SFX[s['nombre']].split(':', 1)[1]
        dur = s['dur'] or duracion_audio(os.path.join(SFX_HF, archivo)) - s['ini']
        dur = min(dur, duracion_audio(os.path.join(SFX_HF, archivo)) - s['ini'])
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
    marca_css = open(os.path.join(AQUI, 'marca.css')).read()
    ayuda_js = open(os.path.join(AQUI, 'ayuda.js')).read()
    avisos, anfitriones = [], []
    for e in v.escenas:
        open(os.path.join(p, 'compositions', e['id'] + '.html'), 'w').write(comp_escena(v, e, marca_css, ayuda_js))
        anfitriones.append(f'<div id="h-{e["id"]}" data-composition-id="{e["id"]}" data-composition-src="compositions/{e["id"]}.html" '
                           f'data-start="{e["desde"]}" data-duration="{r3(e["hasta"] - e["desde"])}" data-track-index="1" '
                           f'data-track-kind="graphics" style="z-index: 1"></div>')
    frames = round(v.dur * 30)
    indice = f'''<!doctype html>
<!-- Generado por canales/businessformen/kit/montar.py desde videos/{v.id}/montaje.py: no editar a mano. -->
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>BusinessForMen · {v.id}</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: #0a0b0d; }}
      #root {{ position: relative; width: 1920px; height: 1080px; overflow: hidden; background: #0a0b0d; }}
      #grano {{ position: absolute; inset: 0; background: url("assets/img/grano.png"); opacity: 0.05; mix-blend-mode: overlay; z-index: 50; pointer-events: none; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{v.dur}" data-width="1920" data-height="1080">
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
        shutil.copy2(os.path.join(CANAL, 'marca', 'plantillas', f), os.path.join(p, f))
    with open(os.path.join(p, 'meta.json'), 'w') as fh:
        json.dump({'id': 'bfm-' + v.id, 'name': 'bfm-' + v.id}, fh, indent=2)
    # Recursos: voz, músicas, imágenes, fuentes y efectos.
    a = os.path.join(p, 'assets')
    for sub in ('audio', 'img', 'fonts', 'sfx'):
        os.makedirs(os.path.join(a, sub), exist_ok=True)
    shutil.copy2(os.path.join(v.trabajo, 'voz', 'voz.wav'), os.path.join(a, 'audio', 'voz.wav'))
    for m in {m['nombre'] for m in v.musicas}:
        shutil.copy2(os.path.join(v.trabajo, 'musica', m + '.wav'), os.path.join(a, 'audio', m + '.wav'))
    for f in os.listdir(os.path.join(v.trabajo, 'img')):
        if f.endswith('.jpg'):
            shutil.copy2(os.path.join(v.trabajo, 'img', f), os.path.join(a, 'img', f))
    for f in ('grano.png', 'desgaste.png'):
        shutil.copy2(os.path.join(REPO, 'salidas', 'businessformen', 'marca', 'img', f), os.path.join(a, 'img', f))
    for f in os.listdir(FUENTES):
        shutil.copy2(os.path.join(FUENTES, f), os.path.join(a, 'fonts', f))
    for s in {s['nombre'] for s in v.sonidos}:
        archivo = SFX[s].split(':', 1)[1]
        shutil.copy2(os.path.join(SFX_HF, archivo), os.path.join(a, 'sfx', archivo))
    return avisos


def main():
    vid = sys.argv[1]
    v = cargar(vid)
    avisos = escribir(v)
    print(json.dumps({'video': vid, 'duracion': v.dur, 'escenas': len(v.escenas), 'sonidos': len(v.sonidos), 'musicas': len(v.musicas)}))
    for a in avisos:
        print('aviso:', a)
    for e in v.escenas:
        d = e['hasta'] - e['desde']
        if d > 9:
            print(f'nota: la escena {e["id"]} dura {d:.1f} s: ¿pasa algo cada 3–5 s?')


if __name__ == '__main__':
    main()
