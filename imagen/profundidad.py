"""
Mapa de profundidad de una imagen con Depth Anything V2 Small (Apache 2.0), en ONNX.
Sirve para el efecto 2.5D: la cámara se mueve un poco y lo cercano se desplaza más
que el fondo, como en un documental.

Se ejecuta con el Python del entorno de FastSD (trae onnxruntime, numpy y Pillow):
  PY=$HERRAMIENTAS/fastsdcpu/env/bin/python
  $PY imagen/profundidad.py plancha.png -o plancha_prof.png

Salida: PNG en escala de grises del mismo tamaño que la imagen; blanco es cerca.
"""
import argparse
import os
import time

import numpy as np
import onnxruntime as ort
from PIL import Image, ImageFilter

HERRAMIENTAS = os.environ.get('HERRAMIENTAS', os.path.expanduser('~/herramientas-videos'))
MODELO = os.path.join(HERRAMIENTAS, 'extra', 'depth-anything-v2-small', 'model.onnx')
MEDIA = np.array([0.485, 0.456, 0.406], dtype=np.float32)
DESVIACION = np.array([0.229, 0.224, 0.225], dtype=np.float32)


def multiplo_14(x):
    return max(14, round(x / 14) * 14)


def main():
    p = argparse.ArgumentParser(description='Mapa de profundidad (Depth Anything V2 Small).')
    p.add_argument('imagen')
    p.add_argument('-o', '--salida')
    p.add_argument('--lado', type=int, default=518, help='lado corto al que trabaja el modelo')
    p.add_argument('--suavizado', type=float, default=2.0, help='desenfoque del mapa, en píxeles de salida')
    args = p.parse_args()
    salida = args.salida or os.path.splitext(args.imagen)[0] + '_prof.png'

    imagen = Image.open(args.imagen).convert('RGB')
    ancho, alto = imagen.size
    escala = args.lado / min(ancho, alto)
    entrada = imagen.resize((multiplo_14(ancho * escala), multiplo_14(alto * escala)), Image.BICUBIC)
    x = (np.asarray(entrada, dtype=np.float32) / 255 - MEDIA) / DESVIACION
    x = x.transpose(2, 0, 1)[None]

    inicio = time.time()
    sesion = ort.InferenceSession(MODELO, providers=['CPUExecutionProvider'])
    profundidad = sesion.run(None, {'pixel_values': x})[0][0]
    # Normaliza con percentiles para que un punto suelto no aplaste el resto.
    bajo, alto_p = np.percentile(profundidad, [1, 99])
    profundidad = np.clip((profundidad - bajo) / max(alto_p - bajo, 1e-6), 0, 1)
    mapa = Image.fromarray((profundidad * 255).astype(np.uint8)).resize((ancho, alto), Image.BICUBIC)
    if args.suavizado > 0:
        mapa = mapa.filter(ImageFilter.GaussianBlur(args.suavizado))
    mapa.save(salida)
    print(f'{salida}  {time.time() - inicio:.1f} s')


if __name__ == '__main__':
    main()
