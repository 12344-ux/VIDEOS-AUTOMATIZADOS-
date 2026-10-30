"""Hojas de auditoría del vídeo entero: un fotograma cada PASO segundos con lo que dice la voz en ese instante,
para revisar si lo que se ve corresponde a lo que se oye. Una hoja por minuto (24 fotogramas).
  python3 videos/anticitera/kit/auditar.py salidas/anticitera/anticitera.mp4 carpeta_salida [paso]"""
import json
import os
import subprocess
import sys
import textwrap

from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
TRABAJO = os.path.join(os.path.dirname(os.path.dirname(RAIZ)), 'salidas', 'anticitera')
PARTES = ['apertura', 'cap1', 'cap2', 'cap3', 'cap4', 'cap5', 'cap6', 'cap7', 'cap8']


def palabras():
    """(inicio, fin, texto) de cada palabra en el tiempo del vídeo entero."""
    t, lista = 0.0, []
    for p in PARTES:
        frames = int(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_packets', '-show_entries',
                                     'stream=nb_read_packets', '-of', 'csv=p=0', os.path.join(TRABAJO, 'renders', p + '.mp4')],
                                    capture_output=True, text=True, check=True).stdout)
        ruta, d = (os.path.join(TRABAJO, 'audio', 'voz_ajustada.json'), 1.2) if p == 'apertura' else \
            (os.path.join(TRABAJO, 'voz', p + '.json'), 3.4)
        for f in json.load(open(ruta))['frases']:
            for w in f['palabras']:
                lista.append((t + d + w['inicio'], t + d + w['fin'], w['texto']))
        t += frames / 30
    return lista, t


def main():
    video, salida = sys.argv[1], sys.argv[2]
    paso = float(sys.argv[3]) if len(sys.argv) > 3 else 2.5
    os.makedirs(salida, exist_ok=True)
    ws, total = palabras()
    fuente = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13) \
        if os.path.exists('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf') else ImageFont.load_default()
    tiempos = [round(i * paso, 2) for i in range(int(total / paso) + 1)]
    for hoja in range(0, len(tiempos), 24):
        grupo = tiempos[hoja:hoja + 24]
        lienzo = Image.new('RGB', (6 * 320, 4 * 250), (18, 18, 18))
        d = ImageDraw.Draw(lienzo)
        for k, t in enumerate(grupo):
            r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', video, '-frames:v', '1', '-vf', 'scale=320:180',
                                '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True, check=True)
            im = Image.open(__import__('io').BytesIO(r.stdout))
            x, y = 320 * (k % 6), 250 * (k // 6)
            lienzo.paste(im, (x, y))
            dicho = ' '.join(w[2] for w in ws if t - paso / 2 <= w[0] < t + paso / 2)
            d.text((x + 4, y + 2), f'{int(t // 60)}:{t % 60:04.1f}', fill=(255, 230, 0), font=fuente)
            for i, linea in enumerate(textwrap.wrap(dicho or '(sin voz)', 44)[:4]):
                d.text((x + 4, y + 183 + i * 16), linea, fill=(230, 230, 230), font=fuente)
        lienzo.save(os.path.join(salida, f'auditoria-{hoja // 24 + 1:02d}.jpg'), quality=80)
    print(f'{(len(tiempos) + 23) // 24} hojas en {salida}')


if __name__ == '__main__':
    main()
