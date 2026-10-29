"""
Monta la hoja comparativa: una fila por modelo, una columna por prompt, con el
tiempo medido debajo de cada imagen.

Uso (en la carpeta con las imágenes y resultados.jsonl):
  python3 hoja.py salida.png etiqueta1:"Nombre|motor|detalle" etiqueta2:"..." ...
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.getcwd()
salida, filas = sys.argv[1], [a.split(':', 1) for a in sys.argv[2:]]
prompts = list(json.load(open(os.path.join(AQUI, 'prompts.json'))))
tiempos = {}
for linea in open(os.path.join(SALIDA, 'resultados.jsonl')):
    d = json.loads(linea)
    if 'prompt' in d:
        tiempos[(d['etiqueta'], d['prompt'])] = d

LADO, MARGEN, ETIQUETA, PIE = 300, 14, 250, 34
fuente = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-SemiBold.otf', 20)
fuente_peq = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Regular.otf', 16)
ancho = ETIQUETA + len(prompts) * (LADO + MARGEN) + MARGEN
alto = 50 + len(filas) * (LADO + PIE + MARGEN)
hoja = Image.new('RGB', (ancho, alto), (250, 247, 242))
d = ImageDraw.Draw(hoja)
TITULOS = {'bolso': 'Bolso', 'cafe': 'Café', 'perro': 'Perro'}
for j, p in enumerate(prompts):
    d.text((ETIQUETA + j * (LADO + MARGEN) + LADO / 2, 26), TITULOS.get(p, p), font=fuente, fill=(29, 26, 23), anchor='mm')
for i, (etiqueta, nombre) in enumerate(filas):
    y = 50 + i * (LADO + PIE + MARGEN)
    lineas = nombre.split('|')
    for k, texto in enumerate(lineas):
        d.text((MARGEN, y + LADO / 2 - 12 * len(lineas) + k * 26), texto,
               font=fuente if k == 0 else fuente_peq, fill=(29, 26, 23) if k == 0 else (94, 87, 79))
    for j, p in enumerate(prompts):
        x = ETIQUETA + j * (LADO + MARGEN)
        ruta = os.path.join(SALIDA, f'{etiqueta}_{p}.png')
        if os.path.exists(ruta):
            hoja.paste(Image.open(ruta).convert('RGB').resize((LADO, LADO), Image.LANCZOS), (x, y))
        else:
            d.rectangle((x, y, x + LADO, y + LADO), outline=(200, 190, 180))
        t = tiempos.get((etiqueta, p))
        if t:
            nota = f"{t['segundos']} s" + (' (con carga)' if t.get('incluye_carga') else '')
            d.text((x + LADO / 2, y + LADO + 17), nota, font=fuente_peq, fill=(94, 87, 79), anchor='mm')
hoja.save(salida)
print(salida, hoja.size)
