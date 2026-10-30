# Capítulo III · Una caja con el cielo dentro. Lo lee kit/montar.py; ver su cabecera.
# Revisión 2 (la primera, en montaje/cap3_v1.py, se quedaba en «imagen + voz»): la caja y su manivela, señaladas;
# el frente se dibuja pieza a pieza y la cámara del dibujo se acerca a cada anillo cuando la voz lo nombra; la
# esfera real; las fases en lista, encendidas una a una; las láminas y sus dientes, señalados; y, para acabar, la
# Luna noche a noche, con pasos desiguales: la pregunta del capítulo IV.

TITULO_ANCHO = 760   # «Una caja con el / cielo dentro»: que no pise la caja

# 1 · La caja reconstruida, desde negro: señalada en «caja».
toma('caja', 0, entra='negro', mov='empuje', centro=(0.8, 0.42), luz=(0.66, 0.36), luzI=0.2, ventana=(0.25, 0.55, 0.6))
grafico('senal', VOZ0 - 0.2, w('manivela', mas=-0.5), id='senal-caja', z=3,
        marcas=[dict(u=0.715, v=0.55, rx=430, ry=360, t=w('caja', mas=-0.05), sale=w('manivela', mas=-0.75),
                     n='CAJA DE MADERA', s='una reconstrucción', lado='izq')])

# 2 · La manivela, de cerca, con un foco.
toma('caja', w('manivela', mas=-0.5), entra='corte', centro=(0.56, 0.64), mov=dict(zoom=(1.65, 1.72)),
     luz=(0.62, 0.5), luzI=0.16, ventana=(0.2, 0.5, 0.5), ventanaI=0.3)
grafico('senal', w('manivela', mas=-0.5), w('Al girarla', mas=-0.25), id='senal-manivela', z=3,
        marcas=[dict(u=0.56, v=0.635, rx=78, ry=118, t=w('manivela', mas=-0.1), sale=w('Al girarla', mas=-0.5),
                     n='MANIVELA', lado='izq', foco=True)])

# 3 · Se entra en el frente: la rueda mayor da una vuelta (un año); los dos anillos, cada uno de cerca al nombrarlo.
toma('placa', w('Al girarla', mas=-0.25), entra='zoom', mov=dict(zoom=(1.04, 1.1), camX=(-0.006, 0.006)),
     brillo=0.62, luz=(0.7, 0.3), luzI=0.1, ventana=(0.25, 0.45, 0.6), ventanaI=0.35)
grafico('frente', w('Al girarla', mas=-0.25), w('esfera', mas=-0.35), id='frente-a', modo='a')
bloque(150, 330, [E('RUEDA MAYOR · 223 DIENTES', w('Cada', mas=-0.1)), D('Una vuelta, un año', w('año', mas=-0.1), tam=58)],
       sale=w('En el frente', mas=-0.35))
bloque(150, 200, [E('ZODÍACO', w('doce', mas=-0.3)), C('12', w('doce'), unidad='signos', tam=210)], sale=w('otro', mas=-0.25))
bloque(150, 200, [E('CALENDARIO EGIPCIO', w('trescientos', mas=-0.1)), C('365', w('días', mas=0.1), desde=1, dur=1.5, unidad='días', tam=210)],
       sale=w('Una aguja', mas=-0.4))
sonido('manivela', w('girarla', mas=-0.1), vol=0.22, dur=2.6, fo=0.6)
sonido('tictac', w('vuelta', mas=-0.2), vol=0.2, dur=2.4, fi=0.2, fo=0.5)
sonido('whoosh', w('doce', mas=-0.5), vol=0.08)
sonido('whoosh', w('trescientos', mas=-0.4), vol=0.08)
sonido('clic', w('Sol', mas=0.05), vol=0.22, dur=0.5)
sonido('clic', w('Luna', mas=0.05), vol=0.18, dur=0.5)

# 4 · La esfera de verdad (macro): señalada.
toma('esfera', w('esfera', mas=-0.35), entra='corte', mov=dict(zoom=(1.05, 1.12), camX=(0.008, -0.008)),
     luz=(0.7, 0.42), luzI=0.16, ventanaI=0.15)
grafico('senal', w('esfera', mas=-0.35), w('gira', mas=0.5), id='senal-esfera', z=3,
        marcas=[dict(u=0.723, v=0.472, r=150, t=w('esfera', mas=-0.1), sale=w('gira', mas=0.25),
                     n='LA LUNA', s='mitad clara, mitad oscura', lado='izq')])

# 5 · De vuelta al dibujo, ya cerca de la esfera: las fases, encendidas una a una; luego, los agujeros.
toma('placa', w('gira', mas=0.5), entra='corte', mov=dict(zoom=(1.08, 1.04), camX=(0.006, -0.006)),
     brillo=0.62, luz=(0.7, 0.3), luzI=0.1, ventana=(0.24, 0.5, 0.55), ventanaI=0.35)
grafico('frente', w('gira', mas=0.5), w('Todo', mas=-0.3), id='frente-b', modo='b')
bloque(150, 420, [E('UNA FILA DE AGUJEROS', w('fila', mas=-0.1)), T('¿Cuántos son?', w('Volveremos', mas=0.05), tam=100)],
       sale=w('Todo', mas=-0.65))
sonido('escaner', w('agujeros', mas=-0.3), vol=0.14, dur=1.0)

# 6 · Las ruedas: láminas finas de bronce...
toma('laminas', w('Todo', mas=-0.3), entra='barrido', mov='izq', luz=(0.68, 0.36), luzI=0.18, ventanaI=0.25)
grafico('senal', w('Todo', mas=-0.3), w('con dientes', mas=-0.25), id='senal-laminas', z=3,
        marcas=[dict(u=0.6, v=0.45, r=215, t=w('láminas', mas=-0.1), sale=w('con dientes', mas=-0.5),
                     n='LÁMINAS DE BRONCE', lado='izq')])

# 7 · ... con dientes triangulares tallados a mano: de cerca.
toma('laminas', w('con dientes', mas=-0.25), entra='zoom', centro=(0.53, 0.25), mov=dict(zoom=(1.75, 1.85), panX=(0.01, -0.01)),
     luz=(0.6, 0.3), luzI=0.18, ventanaI=0.2)
grafico('senal', w('con dientes', mas=-0.25), w('Pero', mas=-0.3), id='senal-dientes', z=3,
        marcas=[dict(u=0.53, v=0.245, rx=170, ry=48, t=w('triangulares', mas=-0.1), sale=w('Pero', mas=-0.55),
                     n='DIENTES TRIANGULARES', s='tallados a mano', lado='izq', vert='aba')])
sonido('lapiz', w('tallados', mas=-0.1), vol=0.16, dur=1.2, fo=0.4)

# 8 · La Luna sobre el mar. «Cómo se mueve la Luna»: noche a noche, con saltos desiguales.
toma('luna', w('Pero', mas=-0.3), entra='oscuro', mov=dict(zoom=(1.04, 1.1), camY=(0.006, -0.006)),
     luz=(0.73, 0.3), luzColor=(0.85, 0.92, 1.0), luzI=0.12, ventanaI=0.2)
grafico('lunas', w('Pero', mas=-0.3), DUR, id='lunas-avance', centro=[0.5, 1.25], radio=1081, a0=-70, a1=-120, n=8,
        exc=0.45, fase=0.15, empieza=w('cómo', mas=-0.05), paso=0.17, rluna=34, marcas=[], numeros=False, sale=DUR - 0.9)

MUSICA = dict(subidas=[(w('año', fin=True, mas=0.1), w('En el frente', mas=-0.1), 0.3),
                       (w('nueva', fin=True, mas=0.2), w('Debajo', mas=-0.1), 0.3)])
