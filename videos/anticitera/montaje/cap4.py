# Capítulo IV · La Luna que acelera. Lo lee kit/montar.py; ver su cabecera.
# Forma: de la Luna real a su órbita dibujada (las marcas de igual tiempo muestran que corre y se frena), al
# astrónomo que lo explicó y al bronce que lo reproduce: el perno y la ranura (graficos/perno.html), que se
# adelanta y se retrasa ante una aguja de ritmo constante, y al final va montado sobre la rueda mayor.

# 1 · La Luna sobre el mar (el mismo plano con el que acabó el capítulo III).
toma('luna', 0, entra='negro', mov=dict(zoom=(1.1, 1.14), camY=(-0.006, 0.006)),
     luz=(0.73, 0.3), luzColor=(0.85, 0.92, 1.0), luzI=0.12, ventana=(0.25, 0.55, 0.6))
bloque(150, 560, [E('CADA NOCHE', w('mes')), D('Avanza entre 12° y 15° de cielo', w('extraño', mas=0.2))], sale=w('Hoy', mas=-0.6))
sonido('grillos', 0.4, vol=0.16, dur=w('Hoy') - 0.2, fi=1.0, fo=0.8)

# 2 · Su órbita: una elipse; las marcas, cada mismo tiempo.
toma('placa', w('Hoy', mas=-0.25), entra='oscuro', mov=dict(zoom=(1.04, 1.07), camX=(-0.006, 0.006)), brillo=0.6,
     luz=(0.7, 0.3), luzI=0.1, ventana=(0.25, 0.45, 0.6), ventanaI=0.35)
grafico('orbita', w('Hoy', mas=-0.25), w('Los griegos', mas=-0.3))
sonido('escaner', w('órbita', mas=-0.2), vol=0.12, dur=1.0)

# 3 · Hiparco.
toma('hiparco', w('Los griegos', mas=-0.3), entra='corte', mov='retroceso', luz=(0.75, 0.25), luzColor=(0.85, 0.92, 1.0),
     luzI=0.12, ventana=(0.25, 0.5, 0.6), ventanaI=0.42)
bloque(150, 470, [E('ASTRÓNOMO · SIGLO II a. C.', w('astrónomo')), N('Hiparco', w('Hiparco'))], sale=w('Y alguien', mas=-0.6))
sonido('viento', w('Los griegos', mas=-0.3), vol=0.18, dur=7.4, fi=0.6, fo=0.8)

# 4 · En bronce: el perno y la ranura; luego, montado sobre la rueda mayor que gira despacio.
toma('placa', w('Y alguien', mas=-0.3), entra='corte', mov=dict(zoom=(1.05, 1.1), camX=(0.006, -0.006)), brillo=0.6,
     luz=(0.7, 0.3), luzI=0.1, ventana=(0.24, 0.5, 0.55), ventanaI=0.35)
grafico('perno', w('Y alguien', mas=-0.3), w('Una teoría', mas=-0.3))
bloque(150, 330, [E('PERNO Y RANURA', w('perno', mas=0.1))], sale=w('Al girar', mas=-0.3))
bloque(150, 330, [E('LA RUEDA DE ARRIBA', w('adelanta', mas=-0.2)), C('± 6,5°', w('retrasa', mas=0.15), tam=180)], sale=w('El punto', mas=-0.5))
bloque(150, 330, [E('GIRO DEL PERIGEO', w('desplaza', mas=0.2)), C('8,85', w('nueve', mas=0.1), unidad='años', tam=180)], sale=w('Una teoría', mas=-0.7))
sonido('tictac3', w('Al girar', mas=-0.1), vol=0.2, dur=6.0, fi=0.3, fo=1.0)
sonido('manivela', w('conjunto', mas=-0.2), vol=0.16, dur=2.4, fo=0.6)

# 5 · La Luna roja: lo que anuncia (abre el capítulo V).
toma('luna-roja', w('Una teoría', mas=-0.3), entra='oscuro', mov='empuje', luz=(0.73, 0.28), luzColor=(1.0, 0.6, 0.45),
     luzI=0.14, ventanaI=0.25)

MUSICA = dict(subidas=[(w('frena', fin=True, mas=0.1), w('Hoy', mas=-0.1), 0.3),
                       (w('vez', fin=True, mas=0.1), w('Igual', 2, mas=-0.1), 0.28)])
