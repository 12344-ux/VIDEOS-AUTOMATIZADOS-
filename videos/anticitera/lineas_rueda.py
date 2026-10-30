"""Contornos de la rueda del fragmento en ámbar (PNG con transparencia), para que el «escáner» los revele."""
import sys
import cv2
import numpy as np
P, S = sys.argv[1], sys.argv[2]
im = cv2.imread(P + '/fragmento.jpg')
g = cv2.bilateralFilter(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY), 9, 40, 9)
bordes = cv2.Canny(cv2.GaussianBlur(g, (0, 0), 1.6), 40, 110)
# Solo las piezas de la máquina: la corona dentada, los cuatro radios y el buje.
C, BUJE = (1405, 538), (1403, 502)
mascara = np.zeros_like(g)
cv2.ellipse(mascara, C, (452, 424), 0, 0, 360, 255, -1)
cv2.ellipse(mascara, C, (372, 350), 0, 0, 360, 0, -1)
cv2.rectangle(mascara, (BUJE[0] - 44, 130), (BUJE[0] + 44, 960), 255, -1)
cv2.rectangle(mascara, (960, BUJE[1] - 44), (1850, BUJE[1] + 44), 255, -1)
cv2.circle(mascara, BUJE, 78, 255, -1)
exterior = np.zeros_like(g)
cv2.ellipse(exterior, C, (452, 424), 0, 0, 360, 255, -1)
bordes = cv2.bitwise_and(cv2.bitwise_and(bordes, mascara), exterior)
n, etiquetas, stats, _ = cv2.connectedComponentsWithStats((bordes > 0).astype(np.uint8), connectivity=8)
limpio = np.zeros_like(bordes)
for i in range(1, n):
    if stats[i, cv2.CC_STAT_AREA] >= 60:
        limpio[etiquetas == i] = 255
print('píxeles de línea', int((limpio > 0).sum()))
# Trazo de unos 3 px: con 2 px casi desaparece en la pantalla de un móvil.
lineas = cv2.GaussianBlur(cv2.dilate(limpio, np.ones((3, 3), np.uint8)).astype(np.float32), (0, 0), 0.7)
alfa = np.clip(lineas / lineas.max() * 1.6, 0, 1)
rgba = np.zeros((1080, 1920, 4), np.uint8)
rgba[..., 0], rgba[..., 1], rgba[..., 2] = 0x6A, 0xB6, 0xE8          # #E8B66A en BGR
rgba[..., 3] = (alfa * 255).astype(np.uint8)
cv2.imwrite(P + '/fragmento_lineas.png', rgba)
vista = (im * 0.45).astype(np.float32)
a = alfa[..., None]
vista = vista * (1 - a) + np.array([0x6A, 0xB6, 0xE8], np.float32) * a
cv2.imwrite(S + '/fragmento_lineas_vista.jpg', cv2.resize(vista.astype(np.uint8), (960, 540)))
