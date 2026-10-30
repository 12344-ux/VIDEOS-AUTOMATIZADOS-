# Capítulo V · Anunciar la oscuridad. Lo lee kit/montar.py; ver su cabecera.
# Forma: la cara de atrás dibujada (graficos/espirales.html): la cámara recorre la espiral de 19 años, baja a la
# de saros, entra en sus casillas hasta leer los signos de eclipse y acaba en el dial de los juegos. Dos cortes a
# lo que esas casillas anuncian: un eclipse de Sol y Olimpia. Acaba bajo la Luna roja.

# 1 · El rótulo sobre el eclipse (un anticipo).
toma('eclipse', 0, entra='negro', mov=dict(zoom=(1.06, 1.08)), luz=(0.7, 0.3), luzI=0.08, ventana=(0.25, 0.45, 0.6))

# 2 · Las espirales: arriba, 19 años y 235 meses; la aguja sigue el surco; abajo, el saros.
toma('placa', VOZ0 - 0.05, entra='oscuro', mov=dict(zoom=(1.04, 1.1), camY=(-0.006, 0.006)), brillo=0.58,
     luz=(0.7, 0.3), luzI=0.1, ventana=(0.24, 0.45, 0.55), ventanaI=0.35)
grafico('espirales', VOZ0 - 0.05, w('eclipse', mas=1.0), id='espirales-a')
bloque(150, 380, [E('19 AÑOS', w('diecinueve')), C('235', w('meses', mas=0.3), desde=0, dur=1.4, unidad='meses', tam=190)],
       sale=w('Sus', mas=-0.4))
bloque(150, 420, [E('MESES GRIEGOS', w('calendario'))], sale=w('La de abajo', mas=-0.5))
bloque(150, 380, [E('SAROS', w('Cuenta', 2)), C('223', w('meses', 3, mas=0.3), desde=0, dur=1.3, unidad='meses', tam=190)],
       sale=w('eclipse', mas=0.6))
sonido('escaner', w('espirales', mas=-0.4), vol=0.14, dur=1.0)
sonido('tictac', w('aguja', mas=-0.1), vol=0.2, dur=3.4, fi=0.2, fo=0.8)

# 3 · Lo que anuncia: un eclipse.
toma('eclipse', w('eclipse', mas=1.0), entra='corte', mov='retroceso', luz=(0.72, 0.28), luzI=0.06, ventanaI=0.2)
sonido('vendaval', w('eclipse', mas=0.9), vol=0.16, dur=3.6, fi=0.5, fo=0.8)

# 4 · De vuelta en las casillas: los signos; luego la rueda de 223 dientes y el dial de los juegos.
toma('placa', w('En sus', mas=-0.3), entra='corte', mov=dict(zoom=(1.06, 1.1), camX=(0.006, -0.006)), brillo=0.58,
     luz=(0.7, 0.3), luzI=0.1, ventana=(0.24, 0.45, 0.55), ventanaI=0.35)
grafico('espirales', w('En sus', mas=-0.3), w('Olímpicos', mas=-0.3), id='espirales-b')
bloque(150, 380, [E('SU RUEDA', w('rueda')), C('223', w('dientes', mas=0.15), desde=0, dur=1.3, unidad='dientes', tam=190)],
       sale=w('Dentro', mas=-0.3))
bloque(150, 380, [E('LOS JUEGOS', w('dial')), D('Cuatro años, uno por sector', w('marca'))], sale=w('Olímpicos', mas=-0.6))
sonido('clic', w('signos', mas=-0.3), vol=0.18, dur=0.5)
sonido('manivela', w('rueda', mas=-0.1), vol=0.15, dur=2.0, fo=0.5)

# 5 · Olimpia.
toma('olimpia', w('Olímpicos', mas=-0.3), entra='barrido', mov=dict(zoom=(1.22, 1.26), panX=(-0.1, -0.085)), luz=(0.3, 0.3), luzI=0.18, ventana=(0.25, 0.55, 0.6), ventanaI=0.42)
bloque(150, 560, [E('OLIMPIA', w('Olímpicos', mas=0.1)), D('Los primeros juegos, en el 776 a. C.', w('Olímpicos', mas=0.6))], sale=w('En la Antigüedad', mas=-0.6))
sonido('viento', w('Olímpicos', mas=-0.3), vol=0.14, dur=4.6, fi=0.4, fo=0.6)

# 6 · La Luna roja: predecir la oscuridad.
toma('luna-roja', w('En la Antigüedad', mas=-0.3), entra='oscuro', mov='empuje', luz=(0.73, 0.28), luzColor=(1.0, 0.6, 0.45),
     luzI=0.14, ventanaI=0.25)
sonido('olas', w('En la Antigüedad', mas=-0.3), vol=0.16, dur=DUR - w('En la Antigüedad'), ini=20, fi=0.8, fo=1.2)

MUSICA = dict(subidas=[(w('igual', fin=True, mas=0.1), w('En sus', mas=-0.1), 0.32)])
