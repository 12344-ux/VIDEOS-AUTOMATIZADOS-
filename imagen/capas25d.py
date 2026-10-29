"""
Prepara una imagen para el efecto 2.5D por capas: separa el sujeto (frente) del fondo
usando el mapa de profundidad y rellena el hueco que deja en el fondo. Así, cuando la
cámara se mueve, el sujeto se desplaza más que el fondo sin que su borde salga doble
(el defecto típico de desplazar una sola imagen con su profundidad).

Se ejecuta con el Python del entorno de FastSD (trae OpenCV):
  PY=$HERRAMIENTAS/fastsdcpu/env/bin/python
  $PY imagen/profundidad.py faro.png -o faro_prof.png
  $PY imagen/capas25d.py faro.png faro_prof.png -o salida/faro
  $PY imagen/capas25d.py manos.png manos_prof.png -o salida/manos --tapar 1610,560,95

Escribe <salida>_fondo.jpg (el fondo con el hueco rellenado), <salida>_frente.png (el sujeto
con transparencia) y <salida>_prof.png (R: profundidad del frente, ensanchada; G: profundidad
del fondo, rellenada). El umbral entre frente y fondo sale solo (Otsu) o con --umbral.
--tapar X,Y,R borra un defecto de la imagen (un círculo de radio R) rellenándolo.
"""
import argparse
import time

import cv2
import numpy as np


def rellenar(imagen, hueco, escala=0.5, radio=6):
    """Rellena el hueco con lo que lo rodea (Telea), a media resolución para ir rápido."""
    alto, ancho = hueco.shape
    peq = cv2.resize(imagen, (int(ancho * escala), int(alto * escala)), interpolation=cv2.INTER_AREA)
    hueco_peq = cv2.resize(hueco, (peq.shape[1], peq.shape[0]), interpolation=cv2.INTER_NEAREST)
    lleno = cv2.inpaint(peq, hueco_peq, radio, cv2.INPAINT_TELEA)
    lleno = cv2.resize(lleno, (ancho, alto), interpolation=cv2.INTER_CUBIC)
    # Fuera del hueco se queda la imagen original; el borde del hueco se funde 6 px.
    peso = cv2.GaussianBlur(hueco.astype(np.float32) / 255, (0, 0), 3)
    if imagen.ndim == 3:
        peso = peso[..., None]
    return (imagen * (1 - peso) + lleno * peso).astype(imagen.dtype)


def main():
    p = argparse.ArgumentParser(description='Capas para 2.5D: frente, fondo rellenado y profundidad.')
    p.add_argument('imagen')
    p.add_argument('profundidad')
    p.add_argument('-o', '--salida', required=True, help='prefijo de los archivos de salida')
    p.add_argument('--umbral', type=float, help='profundidad (0–1) a partir de la cual es frente')
    p.add_argument('--suavidad', type=float, default=0.05, help='transición del borde del frente')
    p.add_argument('--tapar', action='append', default=[], help='X,Y,R: círculo a borrar antes de separar')
    args = p.parse_args()

    inicio = time.time()
    imagen = cv2.imread(args.imagen, cv2.IMREAD_COLOR)
    alto, ancho = imagen.shape[:2]
    prof = cv2.imread(args.profundidad, cv2.IMREAD_GRAYSCALE)
    prof = cv2.resize(prof, (ancho, alto), interpolation=cv2.INTER_CUBIC).astype(np.float32) / 255

    for circulo in args.tapar:
        x, y, r = (int(v) for v in circulo.split(','))
        defecto = np.zeros((alto, ancho), np.uint8)
        cv2.circle(defecto, (x, y), r, 255, -1)
        imagen = rellenar(imagen, defecto, escala=1.0, radio=9)

    umbral = args.umbral
    if umbral is None:
        umbral, _ = cv2.threshold((prof * 255).astype(np.uint8), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        umbral /= 255
    s = args.suavidad
    alfa = np.clip((prof - (umbral - s)) / (2 * s), 0, 1)
    alfa = alfa * alfa * (3 - 2 * alfa)
    # Se encoge 2 px para no arrastrar el color del fondo pegado al borde.
    alfa = cv2.erode(alfa, np.ones((5, 5), np.uint8))
    alfa = cv2.GaussianBlur(alfa, (0, 0), 1.2)

    # El fondo pierde todo lo que es frente, con 30 px de margen (se llevan los detalles finos
    # pegados al sujeto, como una barandilla, que el mapa de profundidad no recoge), y se rellena.
    hueco = cv2.dilate((alfa > 0.02).astype(np.uint8) * 255, np.ones((61, 61), np.uint8))
    fondo = rellenar(imagen, hueco)
    prof_fondo = rellenar((prof * 255).astype(np.uint8), hueco) / 255
    # La profundidad del frente se ensancha para que el borde use la del propio sujeto.
    prof_frente = cv2.GaussianBlur(cv2.dilate(prof, np.ones((9, 9), np.uint8)), (0, 0), 2)

    cv2.imwrite(args.salida + '_fondo.jpg', fondo, [cv2.IMWRITE_JPEG_QUALITY, 93])
    frente = np.dstack([imagen, (alfa * 255).astype(np.uint8)])
    cv2.imwrite(args.salida + '_frente.png', frente)
    mapa = np.dstack([np.zeros_like(prof), prof_fondo, prof_frente])  # OpenCV guarda en BGR
    cv2.imwrite(args.salida + '_prof.png', (np.clip(mapa, 0, 1) * 255).astype(np.uint8))
    print(f'{args.salida}: umbral {umbral:.2f}, frente {alfa.mean() * 100:.0f} % del cuadro, {time.time() - inicio:.1f} s')


if __name__ == '__main__':
    main()
