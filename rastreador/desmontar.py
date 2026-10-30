"""
Desmonta un vídeo corto para estudiar su formato: planos y cortes, transcripción con tiempos, ritmo de la voz, el gancho
de los 3 primeros segundos y una hoja con un fotograma de cada plano. De ahí sale la ficha del formato, y de la ficha un
guion nuestro: se copia la mecánica, nunca el guion, la voz ni las imágenes.

Trabaja sobre un archivo. Desde esta máquina YouTube pide «Sign in to confirm you're not a bot» y da 403 al bajar el
vídeo, y TikTok rechaza la petición: el vídeo lo guarda el usuario desde la app y lo sube a la sesión. (Con una URL lo
intenta con yt-dlp, por si un día deja.)

  python3 rastreador/desmontar.py video.mp4                 # → salidas/rastreador/desmontajes/<nombre>/
  python3 rastreador/desmontar.py video.mp4 --umbral 0.25   # más sensible a los cortes (por defecto 0,3)

Salida: ficha.json, ficha.md y hoja.jpg. La transcripción es la de whisper (small, español) de HyperFrames: la primera
vez baja el modelo (488 MB).
"""
import argparse
import json
import os
import re
import statistics
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = os.environ.get('HERRAMIENTAS', os.path.expanduser('~/herramientas-videos'))
SALIDAS = os.path.join(REPO, 'salidas', 'rastreador', 'desmontajes')
GANCHO = 3.0


def sondear(video):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration:stream=codec_type,width,height,r_frame_rate',
                        '-of', 'json', video], capture_output=True, text=True, check=True)
    d = json.loads(r.stdout)
    v = next(s for s in d['streams'] if s['codec_type'] == 'video')
    num, den = (int(x) for x in v['r_frame_rate'].split('/'))
    return float(d['format']['duration']), v['width'], v['height'], num / den, any(s['codec_type'] == 'audio' for s in d['streams'])


def cortes(video, umbral):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', video, '-filter:v', f"select='gt(scene,{umbral})',showinfo",
                        '-f', 'null', '-'], capture_output=True, text=True)
    return [float(t) for t in re.findall(r'pts_time:([0-9.]+)', r.stderr)]


def transcribir(video, carpeta):
    destino = os.path.join(carpeta, 'transcript.json')
    if not os.path.exists(destino):
        r = subprocess.run([os.path.join(REPO, 'video', 'hf.sh'), 'transcribe', os.path.abspath(video), '--model', 'small',
                            '--language', 'es', '--json', '-d', carpeta], capture_output=True, text=True)
        if r.returncode or not os.path.exists(destino):
            print('Transcripción: no se pudo (' + r.stderr.strip().splitlines()[-1][:200] + ')' if r.stderr.strip() else
                  'Transcripción: no se pudo', file=sys.stderr)
            return []
    return json.load(open(destino))


def hoja(video, planos, carpeta, ancho_celda=270):
    """Un fotograma del centro de cada plano (hasta 24), con su tiempo."""
    planos = planos if len(planos) <= 24 else [planos[round(i * (len(planos) - 1) / 23)] for i in range(24)]
    fotos = []
    for i, (ini, fin) in enumerate(planos):
        t = (ini + fin) / 2
        ruta = os.path.join(carpeta, f'_f{i:02d}.jpg')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', video, '-frames:v', '1', '-q:v', '3', ruta],
                       check=True)
        fotos.append((ini, fin, Image.open(ruta).convert('RGB')))
    w0, h0 = fotos[0][2].size
    alto_celda = round(ancho_celda * h0 / w0)
    cols = min(6, len(fotos))
    filas = (len(fotos) + cols - 1) // cols
    hoja = Image.new('RGB', (cols * ancho_celda, filas * (alto_celda + 34)), (16, 16, 16))
    d = ImageDraw.Draw(hoja)
    fuente = subprocess.run(['fc-match', '-f', '%{file}', 'Inter:weight=600'], capture_output=True, text=True).stdout
    try:
        letra = ImageFont.truetype(fuente, 20)
    except OSError:
        letra = ImageFont.load_default(20)
    for i, (ini, fin, foto) in enumerate(fotos):
        x, y = (i % cols) * ancho_celda, (i // cols) * (alto_celda + 34)
        hoja.paste(foto.resize((ancho_celda, alto_celda)), (x, y))
        d.text((x + 8, y + alto_celda + 6), f'{ini:.1f}–{fin:.1f} s', fill=(235, 235, 235), font=letra)
        os.remove(os.path.join(carpeta, f'_f{i:02d}.jpg'))
    ruta = os.path.join(carpeta, 'hoja.jpg')
    hoja.save(ruta, quality=88)
    return ruta


def bajar(url, carpeta):
    py = os.path.join(H, 'rastreador', 'bin', 'python')
    r = subprocess.run([py, '-m', 'yt_dlp', '-q', '--no-warnings', '-f', 'b[ext=mp4]/bv*+ba/b', '--merge-output-format', 'mp4',
                        '-o', os.path.join(carpeta, 'video.%(ext)s'), url], capture_output=True, text=True)
    ruta = os.path.join(carpeta, 'video.mp4')
    if r.returncode or not os.path.exists(ruta):
        sys.exit('No se pudo bajar (' + (r.stderr.strip().splitlines() or ['?'])[-1][:160] + '). Guarda el vídeo desde la '
                 'app y súbelo a la sesión.')
    return ruta


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('video', help='archivo de vídeo (o URL, que casi siempre bloquean)')
    p.add_argument('-o', '--salida', help='carpeta (por defecto salidas/rastreador/desmontajes/<nombre>)')
    p.add_argument('--umbral', type=float, default=0.3, help='sensibilidad a los cortes, de 0 a 1')
    a = p.parse_args()

    es_url = re.match(r'https?://', a.video)
    nombre = re.sub(r'[^\w-]+', '-', os.path.splitext(os.path.basename(a.video.rstrip('/')))[0]).strip('-')[:60]
    carpeta = a.salida or os.path.join(SALIDAS, nombre)
    os.makedirs(carpeta, exist_ok=True)
    video = bajar(a.video, carpeta) if es_url else a.video

    dur, ancho, alto, fps, con_audio = sondear(video)
    cs = [t for t in cortes(video, a.umbral) if 0.2 < t < dur - 0.2]
    bordes = [0.0] + cs + [dur]
    planos = list(zip(bordes[:-1], bordes[1:]))
    largos = [b - a_ for a_, b in planos]
    palabras = transcribir(video, carpeta) if con_audio else []
    habla = [w for w in palabras if w.get('text', '').strip()]
    gancho = ' '.join(w['text'] for w in habla if w['start'] < GANCHO)
    voz = (habla[-1]['end'] - habla[0]['start']) if habla else 0

    ficha = dict(video=os.path.basename(video), duracion=round(dur, 2), formato=f'{ancho}×{alto}', fps=round(fps, 2),
                 planos=len(planos), plano_medio=round(statistics.mean(largos), 2),
                 plano_mediano=round(statistics.median(largos), 2), cortes_por_minuto=round(60 * len(cs) / dur, 1),
                 primer_corte=round(cs[0], 2) if cs else None, cortes=[round(c, 2) for c in cs],
                 palabras=len(habla), palabras_por_segundo=round(len(habla) / voz, 2) if voz else None,
                 primera_palabra=round(habla[0]['start'], 2) if habla else None, gancho_3s=gancho,
                 transcripcion=' '.join(w['text'] for w in habla))
    ficha['hoja'] = hoja(video, planos, carpeta)
    json.dump(dict(ficha, palabras_con_tiempos=habla), open(os.path.join(carpeta, 'ficha.json'), 'w'),
              ensure_ascii=False, indent=1)

    lineas = [f'# Desmontaje de {ficha["video"]}', '',
              f'- **Duración:** {dur:.1f} s, {ancho} × {alto}, {fps:.0f} fps',
              f'- **Planos:** {len(planos)}; plano medio {ficha["plano_medio"]} s (mediano {ficha["plano_mediano"]} s); '
              f'{ficha["cortes_por_minuto"]} cortes por minuto; primer corte a los {ficha["primer_corte"]} s',
              f'- **Voz:** {len(habla)} palabras, {ficha["palabras_por_segundo"]} por segundo; la primera, a los '
              f'{ficha["primera_palabra"]} s',
              f'- **Gancho (0–{GANCHO:.0f} s):** «{gancho}»', '', '## Planos', '',
              '| # | Desde | Hasta | Dura | Lo que se dice |', '| --- | --- | --- | --- | --- |']
    for i, (ini, fin) in enumerate(planos, 1):
        dicho = ' '.join(w['text'] for w in habla if ini <= (w['start'] + w['end']) / 2 < fin)
        lineas.append(f'| {i} | {ini:.2f} | {fin:.2f} | {fin - ini:.2f} | {dicho or "—"} |')
    lineas += ['', f'Hoja de fotogramas: `{ficha["hoja"]}`']
    open(os.path.join(carpeta, 'ficha.md'), 'w').write('\n'.join(lineas) + '\n')
    print('\n'.join(lineas))


if __name__ == '__main__':
    main()
