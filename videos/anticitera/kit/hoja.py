"""Hoja de contacto de planchas (para revisarlas): python3 kit/hoja.py salida.jpg nombre1 nombre2 ...
Cada plancha a 640 × 360 con una retícula de 10 × 10 (cada línea, un 10 % del cuadro) para situar cosas."""
import os
import sys

from PIL import Image, ImageDraw

P = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'salidas', 'anticitera', 'planchas')
salida, nombres = sys.argv[1], sys.argv[2:]
cols = 2
hoja = Image.new('RGB', (640 * cols, 380 * ((len(nombres) + cols - 1) // cols)), (20, 20, 20))
d = ImageDraw.Draw(hoja)
for i, n in enumerate(nombres):
    x, y = 640 * (i % cols), 380 * (i // cols)
    im = Image.open(os.path.join(P, n + '.png')).convert('RGB').resize((640, 360))
    g = ImageDraw.Draw(im)
    for k in range(1, 10):
        g.line([(64 * k, 0), (64 * k, 360)], fill=(255, 255, 0) if k == 5 else (120, 120, 120), width=1)
        g.line([(0, 36 * k), (640, 36 * k)], fill=(255, 255, 0) if k == 5 else (120, 120, 120), width=1)
    hoja.paste(im, (x, y + 20))
    d.text((x + 6, y + 4), n, fill=(255, 255, 255))
hoja.save(salida, quality=85)
