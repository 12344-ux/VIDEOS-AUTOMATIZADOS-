"""
Recorta el sujeto de una imagen (quita el fondo) con BiRefNet lite (MIT), en ONNX.
Sirve para el collage y para poner títulos detrás del sujeto. Funciona mejor si el
prompt pide el objeto aislado sobre fondo liso.

Se ejecuta con el Python del entorno de FastSD:
  PY=$HERRAMIENTAS/fastsdcpu/env/bin/python
  $PY imagen/recortar.py brujula.png -o brujula_recorte.png --ajustar

Salida: PNG con transparencia. --ajustar recorta el lienzo al sujeto con un margen.
"""
import argparse
import os
import time

import numpy as np
import onnxruntime as ort
from PIL import Image

HERRAMIENTAS = os.environ.get('HERRAMIENTAS', os.path.expanduser('~/herramientas-videos'))
MODELO = os.path.join(HERRAMIENTAS, 'extra', 'birefnet-lite', 'model.onnx')
LADO = 1024
MEDIA = np.array([0.485, 0.456, 0.406], dtype=np.float32)
DESVIACION = np.array([0.229, 0.224, 0.225], dtype=np.float32)


def main():
    p = argparse.ArgumentParser(description='Recorte del sujeto (BiRefNet lite).')
    p.add_argument('imagen')
    p.add_argument('-o', '--salida')
    p.add_argument('--ajustar', action='store_true', help='recorta el lienzo al sujeto')
    p.add_argument('--margen', type=int, default=16)
    args = p.parse_args()
    salida = args.salida or os.path.splitext(args.imagen)[0] + '_recorte.png'

    imagen = Image.open(args.imagen).convert('RGB')
    x = np.asarray(imagen.resize((LADO, LADO), Image.BILINEAR), dtype=np.float32) / 255
    x = ((x - MEDIA) / DESVIACION).transpose(2, 0, 1)[None]

    inicio = time.time()
    sesion = ort.InferenceSession(MODELO, providers=['CPUExecutionProvider'])
    logits = sesion.run(None, {'input_image': x})[0][0, 0]
    mascara = 1 / (1 + np.exp(-logits))
    alfa = Image.fromarray((mascara * 255).astype(np.uint8)).resize(imagen.size, Image.BICUBIC)

    recorte = imagen.copy()
    recorte.putalpha(alfa)
    if args.ajustar:
        caja = alfa.point(lambda v: 255 if v > 24 else 0).getbbox()
        if caja:
            m = args.margen
            recorte = recorte.crop((max(caja[0] - m, 0), max(caja[1] - m, 0),
                                    min(caja[2] + m, imagen.width), min(caja[3] + m, imagen.height)))
    recorte.save(salida)
    print(f'{salida}  {recorte.size[0]}x{recorte.size[1]}  {time.time() - inicio:.1f} s')


if __name__ == '__main__':
    main()
