"""
Amplía una imagen al doble con EDSR, el modelo de FastSD CPU (rupeshs/edsr-onnx, 5,5 MB, ONNX).
Sirve para generar las planchas con menos píxeles, que en FLUX cuesta mucho menos, y llevarlas
a 1920 × 1080 sin perder detalle.

Se ejecuta con el Python del entorno de FastSD (trae onnxruntime):
  PY=$HERRAMIENTAS/fastsdcpu/env/bin/python
  $PY imagen/ampliar.py plancha.png -o plancha_1080.png              # ×2, recortado a 1920 × 1080
  $PY imagen/ampliar.py plancha.png -o plancha_2x.png --tamano no    # ×2 tal cual

Con --tamano (por defecto 1920x1080), la imagen ampliada se reduce, si hace falta, hasta cubrir
ese tamaño y se recorta por el centro: 960 × 544 da 1920 × 1088 y pierde 4 px arriba y abajo.
"""
import argparse
import glob
import os
import sys
import time

import numpy as np
from PIL import Image

HERRAMIENTAS = os.environ.get('HERRAMIENTAS', os.path.expanduser('~/herramientas-videos'))
MODELO = 'models--rupeshs--edsr-onnx/snapshots/*/edsr_onnxsim_2x.onnx'


def ruta_modelo():
    rutas = glob.glob(os.path.join(HERRAMIENTAS, 'hf', 'hub', MODELO))
    if not rutas:
        sys.exit('Falta el modelo EDSR. Ejecuta: ./instalar.sh imagen')
    return rutas[0]


def ampliar(imagen, sesion=None):
    """PIL RGB → PIL RGB al doble de tamaño."""
    import onnxruntime as ort

    if sesion is None:
        sesion = ort.InferenceSession(ruta_modelo(), providers=['CPUExecutionProvider'])
    x = np.asarray(imagen.convert('RGB'), dtype=np.float32).transpose(2, 0, 1)[None] / 255.0
    y = sesion.run(None, {sesion.get_inputs()[0].name: x})[0][0]
    return Image.fromarray((np.clip(y, 0, 1).transpose(1, 2, 0) * 255 + 0.5).astype(np.uint8))


def encajar(imagen, ancho, alto):
    """Reduce (nunca amplía) hasta cubrir ancho × alto y recorta por el centro."""
    escala = max(ancho / imagen.width, alto / imagen.height)
    if escala < 1:
        imagen = imagen.resize((round(imagen.width * escala), round(imagen.height * escala)), Image.LANCZOS)
    x, y = (imagen.width - ancho) // 2, (imagen.height - alto) // 2
    return imagen.crop((x, y, x + ancho, y + alto))


def main():
    p = argparse.ArgumentParser(description='Amplía una imagen ×2 con EDSR.')
    p.add_argument('entrada')
    p.add_argument('-o', '--salida', required=True)
    p.add_argument('--tamano', default='1920x1080', help='tamaño final (ANCHOxALTO) o «no»')
    args = p.parse_args()
    t = time.time()
    salida = ampliar(Image.open(args.entrada))
    if args.tamano != 'no':
        ancho, alto = (int(v) for v in args.tamano.lower().split('x'))
        salida = encajar(salida, ancho, alto)
    salida.save(args.salida)
    print(f'{args.salida}  {salida.width} × {salida.height}  {time.time() - t:.1f} s')


if __name__ == '__main__':
    main()
