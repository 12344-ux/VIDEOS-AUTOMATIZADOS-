# Capítulo III · Una caja con el cielo dentro. Lo lee kit/montar.py; ver su cabecera.
# Forma: de la caja reconstruida se entra en su frente, que se dibuja pieza a pieza a medida que la voz las
# nombra (graficos/frente.html); corte a la esfera real y vuelta al dibujo, ya en las fases; los agujeros
# quedan como pregunta para el capítulo VIII. Acaba en la Luna sobre el mar, que abre el capítulo IV.

TITULO_ANCHO = 760   # «Una caja con el / cielo dentro»: que no pise la caja

# 1 · La caja reconstruida, desde negro.
toma('caja', 0, entra='negro', mov='empuje', centro=(0.8, 0.42), luz=(0.66, 0.36), luzI=0.2, ventana=(0.25, 0.55, 0.6))
bloque(150, 600, [E('RECONSTRUCCIÓN', w('caja'))], sale=w('Al girarla', mas=-0.6))

# 2 · Se entra en el frente: la rueda mayor da una vuelta (un año) y se dibujan los anillos y las agujas.
toma('placa', w('Al girarla', mas=-0.25), entra='zoom', mov=dict(zoom=(1.04, 1.08), camX=(-0.006, 0.006)),
     brillo=0.62, luz=(0.7, 0.3), luzI=0.1, ventana=(0.25, 0.45, 0.6), ventanaI=0.35)
grafico('frente', w('Al girarla', mas=-0.25), w('esfera', mas=-0.35), id='frente-a', modo='a')
bloque(150, 330, [E('RUEDA MAYOR', w('Cada')), C('365', w('año', mas=0.15), desde=1, dur=1.7, unidad='días', tam=200),
                  D('223 dientes', w('rueda', mas=0.2))],
       sale=w('En el frente', mas=-0.35))
sonido('manivela', w('girarla', mas=-0.1), vol=0.22, dur=2.6, fo=0.6)
sonido('tictac', w('vuelta', mas=-0.2), vol=0.2, dur=2.4, fi=0.2, fo=0.5)
sonido('clic', w('Sol', mas=0.05), vol=0.22, dur=0.5)
sonido('clic', w('Luna', mas=0.05), vol=0.18, dur=0.5)

# 3 · La esfera de verdad (macro), un instante.
toma('esfera', w('esfera', mas=-0.35), entra='corte', mov=dict(zoom=(1.05, 1.12), camX=(0.008, -0.008)),
     luz=(0.7, 0.42), luzI=0.16, ventanaI=0.15)

# 4 · De vuelta al dibujo, ya cerca de la esfera: las fases; luego se aleja hasta los agujeros.
toma('placa', w('gira', mas=0.5), entra='corte', mov=dict(zoom=(1.08, 1.04), camX=(0.006, -0.006)),
     brillo=0.62, luz=(0.7, 0.3), luzI=0.1, ventana=(0.24, 0.5, 0.55), ventanaI=0.35)
grafico('frente', w('gira', mas=0.5), w('Todo', mas=-0.3), id='frente-b', modo='b')
bloque(150, 500, [E('¿CUÁNTOS?', w('Volveremos', mas=0.1))], sale=w('Todo', mas=-0.65))
sonido('escaner', w('agujeros', mas=-0.3), vol=0.14, dur=1.0)

# 5 · Las ruedas en láminas de bronce, con sus dientes triangulares.
toma('laminas', w('Todo', mas=-0.3), entra='barrido', mov='izq', luz=(0.68, 0.36), luzI=0.18, ventanaI=0.25)

# 6 · La Luna sobre el mar: lo que viene.
toma('luna', w('Pero', mas=-0.3), entra='oscuro', mov=dict(zoom=(1.04, 1.1), camY=(0.006, -0.006)),
     luz=(0.73, 0.3), luzColor=(0.85, 0.92, 1.0), luzI=0.12, ventanaI=0.2)

MUSICA = dict(subidas=[(w('año', fin=True, mas=0.1), w('En el frente', mas=-0.1), 0.3),
                       (w('nueva', fin=True, mas=0.2), w('Debajo', mas=-0.1), 0.3)])
