"""
Hoja comparativa de las tres rutas de marca de BusinessForMen: para cada una, su paleta, sus tipografías, dos
fotogramas del vídeo (la MAAN y el logo) y la miniatura. Saca los fotogramas de los renders.

  python3 canales/businessformen/marca/hoja.py salidas/businessformen/marca/hoja-marca.jpg
"""
import io
import os
import subprocess
import sys
import textwrap

from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
TRABAJO = os.path.join(REPO, 'salidas', 'businessformen', 'marca')
INTER = '/usr/share/fonts/opentype/inter/Inter-{}.otf'

RUTAS = [
    ('sastre', '1 · Sastre', 'La elegancia clásica de la sastrería: lenta, fina, segura.',
     [('#0E0C0C', 'negro cálido'), ('#EFE8DD', 'marfil'), ('#8E1B2C', 'rojo burdeos'), ('#8C8379', 'gris')],
     'Bodoni Moda · Jost'),
    ('consejo', '2 · Consejo', 'La sala de juntas moderna: rápida, precisa, cortes secos.',
     [('#0A0B0D', 'grafito'), ('#F4F3F0', 'blanco'), ('#B0122F', 'rojo carmesí'), ('#8A8D93', 'gris')],
     'Inter Tight · IBM Plex Mono'),
    ('lacre', '3 · Lacre', 'Editorial y contundente: palabras grandes, sello que se estampa.',
     [('#0B0A0A', 'negro'), ('#F1EBE1', 'papel'), ('#B3261E', 'rojo lacre'), ('#8E877D', 'gris')],
     'Archivo Narrow · Instrument Serif'),
]
TIEMPOS = (3.9, 9.9, 17.4)   # el titular, la MAAN y el logo


def cuadro(video, t, ancho):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', video, '-frames:v', '1', '-f', 'image2pipe',
                        '-vcodec', 'png', '-'], capture_output=True, check=True)
    im = Image.open(io.BytesIO(r.stdout)).convert('RGB')
    return im.resize((ancho, ancho * 9 // 16), Image.LANCZOS)


def main():
    salida = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TRABAJO, 'hoja-marca.jpg')
    W, FILA, M = 2480, 440, 40
    hoja = Image.new('RGB', (W, 120 + FILA * len(RUTAS)), (22, 22, 24))
    d = ImageDraw.Draw(hoja)
    f = lambda peso, tam: ImageFont.truetype(INTER.format(peso), tam)
    d.text((M, 36), 'BusinessForMen · pruebas de marca', font=f('SemiBold', 44), fill=(240, 238, 234))
    d.text((W - M, 50), 'el mismo texto y los mismos tiempos en las tres', font=f('Regular', 26), fill=(150, 150, 150), anchor='ra')
    ancho_img = 440
    for i, (ruta, nombre, lema, paleta, tipos) in enumerate(RUTAS):
        y = 120 + i * FILA
        d.line([(M, y), (W - M, y)], fill=(48, 48, 52), width=2)
        d.text((M, y + 30), nombre, font=f('Bold', 50), fill=(240, 238, 234))
        for k, renglon in enumerate(textwrap.wrap(lema, 40)):
            d.text((M, y + 98 + k * 30), renglon, font=f('Regular', 24), fill=(170, 170, 170))
        for k, (hexa, etiqueta) in enumerate(paleta):
            x0 = M + k * 132
            d.rectangle([x0, y + 176, x0 + 112, y + 288], fill=hexa, outline=(70, 70, 74))
            d.text((x0, y + 300), hexa, font=f('Medium', 20), fill=(220, 220, 220))
            d.text((x0, y + 326), etiqueta, font=f('Regular', 18), fill=(140, 140, 140))
        d.text((M, y + 372), tipos, font=f('Medium', 24), fill=(200, 200, 200))
        video = os.path.join(TRABAJO, 'renders', ruta + '.mp4')
        x = 620
        for t in TIEMPOS:
            hoja.paste(cuadro(video, t, ancho_img), (x, y + 60))
            x += ancho_img + 24
        mini = Image.open(os.path.join(TRABAJO, 'miniaturas', ruta + '.jpg')).convert('RGB').resize((ancho_img, ancho_img * 9 // 16), Image.LANCZOS)
        hoja.paste(mini, (x, y + 60))
        for k, texto in enumerate(('titular', 'la MAAN', 'logo', 'miniatura')):
            d.text((620 + k * (ancho_img + 24), y + 60 + ancho_img * 9 // 16 + 14), texto, font=f('Regular', 20), fill=(140, 140, 140))
    hoja.save(salida, quality=90)
    print(salida)


if __name__ == '__main__':
    main()
