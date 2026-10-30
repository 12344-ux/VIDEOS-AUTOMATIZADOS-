"""
Monta las pruebas de marca de BusinessForMen: en la plantilla de cada ruta (plantillas/<ruta>.html, el vídeo, y
plantillas/<ruta>-miniatura.html) pone los tiempos de las palabras de la narración, escribe el proyecto de
HyperFrames (<ruta>/index.html y miniaturas/<ruta>/index.html) y copia en su assets/ la voz, su música, la
imagen, las fuentes y los efectos. Las tres rutas cuentan lo mismo con los mismos tiempos. Las plantillas viven
fuera de los proyectos: HyperFrames tomaría cada HTML de la raíz por una composición más.

  python3 canales/businessformen/marca/montar.py [sastre consejo lacre]
  python3 canales/businessformen/marca/montar.py --miniaturas [rutas]     solo las miniaturas

En las plantillas: {{w:palabra}} es el inicio de la palabra en el vídeo y {{f:palabra}} su fin; con #n, la
aparición n («{{w:estás#2}}»). {{VOZ0}} es la entrada de la voz, {{FINVOZ}} su final y {{DUR}} la duración del
vídeo (la voz y el cierre con el logo). {{e:expresión}} calcula con w("palabra", n), f("palabra", n), VOZ0, FINVOZ
y DUR: «{{e:f("pidiendo") + 0.05}}».
Los recursos salen de canales/businessformen/marca/preparar.sh, en salidas/businessformen/marca/.
"""
import json
import os
import re
import shutil
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
TRABAJO = os.environ.get('TRABAJO', os.path.join(REPO, 'salidas', 'businessformen', 'marca'))
H = os.environ.get('HERRAMIENTAS', os.path.expanduser('~/herramientas-videos'))
SFX_HF = os.path.join(H, 'hyperframes/node_modules/hyperframes/dist/skills/media-use/audio/assets/sfx')
SFX = ['impact-bass-1.mp3', 'impact-bass-2.mp3', 'whoosh-short.mp3', 'whoosh-cinematic.mp3', 'whoosh.mp3',
       'click.mp3', 'click-soft.mp3', 'key-press.mp3', 'chime.mp3', 'riser.mp3']
VOZ0 = 0.6
CIERRE = 4.6   # del final de la voz al final del vídeo: el logo animado
RUTAS = ['sastre', 'consejo', 'lacre']


def limpia(s):
    return re.sub(r'[^\wáéíóúüñ]', '', s.lower())


def copiar(d, ruta):
    """Los recursos del proyecto d (la voz, la música de la ruta, las imágenes, las fuentes y los efectos)."""
    a = os.path.join(d, 'assets')
    for sub in ('audio', 'img', 'fonts', 'sfx'):
        os.makedirs(os.path.join(a, sub), exist_ok=True)
    shutil.copy2(os.path.join(TRABAJO, 'voz', 'prueba.wav'), os.path.join(a, 'audio', 'voz.wav'))
    shutil.copy2(os.path.join(TRABAJO, 'musica', ruta + '.wav'), os.path.join(a, 'audio', 'musica.wav'))
    for f in ('mesa.jpg', 'grano.png', 'desgaste.png'):
        shutil.copy2(os.path.join(TRABAJO, 'img', f), os.path.join(a, 'img', f))
    for f in os.listdir(os.path.join(TRABAJO, 'fuentes')):
        shutil.copy2(os.path.join(TRABAJO, 'fuentes', f), os.path.join(a, 'fonts', f))
    for f in SFX:
        shutil.copy2(os.path.join(SFX_HF, f), os.path.join(a, 'sfx', f))


def main():
    voz = json.load(open(os.path.join(TRABAJO, 'voz', 'prueba.json')))
    palabras = [p for f in voz['frases'] for p in f['palabras']]

    def palabra(texto, n=1, fin=False):
        hechas = [p for p in palabras if limpia(p['texto']) == limpia(texto)]
        if len(hechas) < n:
            raise SystemExit(f'no está «{texto}» (aparición {n})')
        p = hechas[n - 1]
        return VOZ0 + (p['fin'] if fin else p['inicio'])

    finvoz = VOZ0 + voz['duracion']
    dur = round(finvoz + CIERRE, 2)
    nombres = dict(w=lambda t, n=1: palabra(t, n), f=lambda t, n=1: palabra(t, n, True), VOZ0=VOZ0, FINVOZ=finvoz, DUR=dur)

    def tiempo(m):
        tipo, clave = m.group(1), m.group(2)
        texto, _, n = clave.partition('#')
        return f"{palabra(texto, int(n or 1), tipo == 'f'):.3f}"

    solo_miniaturas = '--miniaturas' in sys.argv
    for ruta in [a for a in sys.argv[1:] if not a.startswith('--')] or RUTAS:
        for plantilla, d in ((ruta + '.html', os.path.join(AQUI, ruta)),
                             (ruta + '-miniatura.html', os.path.join(AQUI, 'miniaturas', ruta))):
            if solo_miniaturas and not plantilla.endswith('-miniatura.html'):
                continue
            origen = os.path.join(AQUI, 'plantillas', plantilla)
            if not os.path.exists(origen):
                continue
            s = open(origen).read()
            s = re.sub(r'\{\{e:(.+?)\}\}', lambda m: f'{eval(m.group(1), {}, nombres):.3f}', s)
            s = re.sub(r'\{\{([wf]):([^}]+)\}\}', tiempo, s)
            s = s.replace('{{VOZ0}}', f'{VOZ0:.3f}').replace('{{FINVOZ}}', f'{finvoz:.3f}').replace('{{DUR}}', f'{dur:.2f}')
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, 'index.html'), 'w').write(s)
            for f in ('hyperframes.json', 'meta.json'):
                if not os.path.exists(os.path.join(d, f)):
                    shutil.copy2(os.path.join(AQUI, 'plantillas', f), os.path.join(d, f))
            copiar(d, ruta)
        print(json.dumps({'ruta': ruta, 'voz': [VOZ0, round(finvoz, 3)], 'duracion': dur}))


if __name__ == '__main__':
    main()
