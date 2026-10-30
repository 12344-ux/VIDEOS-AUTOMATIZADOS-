"""Versión «radiografía» de una plancha, para el escáner de graficos/rayos.html: la luminancia invertida y
contrastada solo dentro del objeto (el fondo, como el aire en una placa, queda oscuro), en gris azulado, con los
bordes de Canny reforzados y, si se piden, ruedas ocultas dibujadas dentro (las que solo deja ver la radiografía). Con el Python del entorno de FastSD (OpenCV):
  $PYF videos/anticitera/kit/rayosx.py salidas/anticitera/planchas/fragmento.jpg -o .../fragmento_rx.jpg
                                        [--lineas .../fragmento_lineas.png]   (contornos ya extraídos, opcional)"""
import argparse

import cv2
import numpy as np

p = argparse.ArgumentParser()
p.add_argument('plancha')
p.add_argument('-o', '--salida', required=True)
p.add_argument('--lineas', help='PNG con contornos (blanco sobre transparente o negro) que se suman')
p.add_argument('--ruedas', default='', help='ruedas ocultas «x,y,radio,dientes;…» en píxeles de la plancha')
a = p.parse_args()

im = cv2.imread(a.plancha)
gris = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
# El objeto: lo que no es fondo oscuro (terciopelo, sombra), suavizado.
mascara = cv2.GaussianBlur((cv2.GaussianBlur(gris, (0, 0), 6) > 38).astype(np.float32), (0, 0), 6)
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8)).apply(gris).astype(np.float32)
denso = np.clip((clahe - 30) * 1.25, 0, 255) * 0.55
bordes = cv2.Canny(cv2.GaussianBlur(gris, (0, 0), 2.0), 30, 90)
bordes = cv2.GaussianBlur(cv2.dilate(bordes, np.ones((2, 2), np.uint8)), (0, 0), 0.8).astype(np.float32)
v = (denso + bordes * 0.45) * mascara
if a.lineas:
    l = cv2.imread(a.lineas, cv2.IMREAD_UNCHANGED)
    l = cv2.resize(l, (im.shape[1], im.shape[0]))
    alfa = l[:, :, 3].astype(np.float32) if l.shape[2] == 4 else cv2.cvtColor(l, cv2.COLOR_BGR2GRAY).astype(np.float32)
    v = v + alfa * 0.6
# Ruedas ocultas: corona de dientes triangulares, aro, buje y cuatro radios, en trazo claro.
capa = np.zeros_like(gris)
for r in filter(None, a.ruedas.split(';')):
    x, y, rad, n = (float(c) for c in r.split(','))
    pts = []
    for k in range(int(n)):
        a0 = 2 * np.pi * k / n
        pts += [(x + (rad + 5) * np.cos(a0), y + (rad + 5) * np.sin(a0)),
                (x + (rad - 5) * np.cos(a0 + np.pi / n), y + (rad - 5) * np.sin(a0 + np.pi / n))]
    cv2.polylines(capa, [np.array(pts, np.int32)], True, 255, 2, cv2.LINE_AA)
    cv2.circle(capa, (int(x), int(y)), int(rad * 0.82), 255, 2, cv2.LINE_AA)
    cv2.circle(capa, (int(x), int(y)), max(6, int(rad * 0.13)), 255, 2, cv2.LINE_AA)
    for k in range(4):
        g = k * np.pi / 2 + 0.3
        cv2.line(capa, (int(x + rad * 0.13 * np.cos(g)), int(y + rad * 0.13 * np.sin(g))),
                 (int(x + rad * 0.82 * np.cos(g)), int(y + rad * 0.82 * np.sin(g))), 255, 2, cv2.LINE_AA)
v = np.clip(v + cv2.GaussianBlur(capa, (0, 0), 0.7).astype(np.float32) * 0.95, 0, 255)
# Gris azulado de placa de rayos X, con el negro algo levantado.
tinte = np.array([1.0, 0.93, 0.78], np.float32)  # BGR
out = np.clip(10 + v[:, :, None] * tinte, 0, 255).astype(np.uint8)
cv2.imwrite(a.salida, out, [cv2.IMWRITE_JPEG_QUALITY, 92])
print(a.salida)
