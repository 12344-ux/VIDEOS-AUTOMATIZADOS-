# Capítulo I · Un bulto olvidado (Atenas, 1901–1951). Lo lee kit/montar.py; ver su cabecera.
# Revisión 2 (la primera, en montaje/cap1_v1.py, se quedaba en «imagen + voz»): un plano por idea y, en cada uno,
# algo que pasa en la palabra que lo dice. El foco se lleva a las estatuas; el bulto, solo en la oscuridad, se
# agrieta al secarse; la lupa de Stais entra hasta la rueda; su idea se tacha; en el fondo del mar, la sospecha de
# que el bronce cayó después; Rehm; la calculadora del cielo; lo que lo sella (bronce, piedra, cal); el cajón.

# 1 · La sala del museo, desde negro: el lugar.
toma('museo', 0, entra='negro', mov='der', luz=(0.66, 0.2), luzI=0.22, luzR=0.32, ventana=(0.24, 0.6, 0.6))
bloque(150, 540, [E('ATENAS · 1901', w('Atenas')), D('Museo Arqueológico Nacional', w('Museo'))], sale=w('Las estatuas', mas=-0.45))
sonido('pasos', 0.9, vol=0.22, dur=7.6, fi=0.8, fo=1.2)

# 2 · «Se llevan toda la atención»: un foco sobre las estatuas, el resto a oscuras.
toma('museo', w('Las estatuas', mas=-0.25), entra='corte', centro=(0.76, 0.52), mov=dict(zoom=(1.3, 1.36), camX=(0.008, -0.008)),
     luz=(0.66, 0.2), luzI=0.22, luzR=0.32, ventana=(0.24, 0.5, 0.5), ventanaI=0.3)
grafico('senal', w('Las estatuas', mas=-0.25), w('El bulto', mas=-0.25), id='senal-estatuas', z=3,
        marcas=[dict(u=0.72, v=0.56, rx=330, ry=250, t=w('estatuas', mas=0.05), sale=w('El bulto', mas=-0.5),
                     n='ESTATUAS DEL NAUFRAGIO', s='bronce y mármol', lado='izq', foco=True)])

# 3 · El bulto, apartado en la penumbra; la madera que lo envolvía se encoge y lo parte: grietas en «encoge» y «parte».
toma('bulto', w('El bulto', mas=-0.25), entra='oscuro', centro=(0.6, 0.5), mov=dict(zoom=(1.0, 1.14)),
     luz=(0.62, 0.3), luzI=0.16, luzR=0.3, ventana=(0.2, 0.3, 0.5), ventanaI=0.5,
     mas={'zoom': [[w('parte', mas=-0.02), 1.115], [w('parte', mas=0.06), 1.15, 'power4.out'], [w('parte', mas=0.5), 1.125, 'power2.inOut']]})
grafico('senal', w('El bulto', mas=-0.25), w('pedazos', mas=-0.12), id='senal-bulto', z=3,
        marcas=[dict(u=0.6, v=0.52, rx=520, ry=300, t=w('bulto', mas=0.05), sale=w('al secarse', mas=-0.3),
                     n='EL BULTO', s='bronce corroído', lado='izq'),
                dict(u=0.58, v=0.38, rx=210, ry=80, t=w('madera', mas=-0.05), sale=w('encoge', mas=0.2),
                     n='MADERA', lado='izq')])
grafico('grieta', w('El bulto', mas=-0.25), w('pedazos', mas=-0.12), z=2, sale=w('pedazos', mas=-0.3),
        grietas=[dict(pts=[[0.5, 0.35], [0.53, 0.47], [0.51, 0.59], [0.54, 0.73]], t=w('encoge', mas=0.05), dur=0.7),
                 dict(pts=[[0.7, 0.29], [0.67, 0.42], [0.71, 0.56], [0.69, 0.72]], t=w('encoge', mas=0.45), dur=0.6),
                 dict(pts=[[0.39, 0.57], [0.52, 0.5], [0.62, 0.54], [0.75, 0.47], [0.85, 0.5]], t=w('parte', mas=-0.02), dur=0.35, ancho=10)])
sonido('parquet', w('encoge', mas=0.02), vol=0.22, dur=0.8)
sonido('parquet', w('parte', mas=-0.04), vol=0.38, dur=1.0)

# 4 · Golpe de zoom a los pedazos; la fecha, cifra a cifra.
toma('pedazos', w('pedazos', mas=-0.12), entra='zoom', mov=dict(zoom=(1.05, 1.1), camX=(0.0, 0.0)),
     luz=(0.62, 0.42), luzI=0.18, ventana=(0.22, 0.5, 0.55), ventanaI=0.55)
bloque(150, 330, [E('17 DE MAYO', w('diecisiete')), C('1902', w('mil'), tam=230)], sale=w('el arqueólogo', mas=-0.4))
sonido('golpe2', w('pedazos', mas=-0.1), vol=0.22)

# 5 · Stais se fija en uno de ellos: su nombre y un foco sobre la lupa.
toma('lupa', w('el arqueólogo', mas=-0.2), entra='corte', mov='empuje', luz=(0.7, 0.45), luzI=0.2,
     ventana=(0.24, 0.42, 0.6), ventanaI=0.5)
bloque(150, 470, [E('ARQUEÓLOGO', w('arqueólogo')), N('Valerios Stais', w('Valerios'))], sale=w('Incrustada', mas=-0.45))
grafico('senal', w('el arqueólogo', mas=-0.2), w('Incrustada', mas=-0.25), id='senal-lupa', z=3,
        marcas=[dict(u=0.656, v=0.39, r=132, t=w('fija', mas=-0.05), sale=w('Incrustada', mas=-0.45), foco=True)])

# 6 · Dentro de la lente: la rueda se dibuja encima de la de verdad.
toma('lupa', w('Incrustada', mas=-0.25), entra='zoom', centro=(0.6475, 0.398), mov=dict(zoom=(2.05, 2.2)),
     luz=(0.7, 0.45), luzI=0.12, ventana=(0.2, 0.5, 0.5), ventanaI=0.45)
grafico('rueda', w('Incrustada', mas=-0.25), w('Stais', 2, mas=-0.3), centro=[0.6475, 0.398], radio=64, dientes=24, giro=0,
        en=w('rueda', mas=-0.1), sale=w('Stais', 2, mas=-0.55))
bloque(150, 470, [E('EN LA PIEDRA', w('piedra')), D('una rueda dentada', w('hay'), tam=58)], sale=w('Stais', 2, mas=-0.5))
sonido('clic', w('rueda', mas=0.05), vol=0.3, dur=0.6)

# 7 · Su idea: un reloj astronómico. «Casi nadie le cree»: se tacha y la imagen se apaga.
toma('reloj', w('Stais', 2, mas=-0.3), entra='oscuro', sat=0.55, mov=dict(zoom=(1.06, 1.12), camX=(-0.01, 0.01)),
     luz=(0.62, 0.5), luzI=0.16, luzR=0.3, ventana=(0.24, 0.5, 0.6), ventanaI=0.55,
     mas={'brillo': [[w('Casi', mas=-0.05), 1.0], [w('cree', mas=0.4), 0.5, 'power2.inOut']]})
bloque(150, 470, [E('LA IDEA DE STAIS', w('piensa')), D('Un reloj astronómico', w('reloj'), tacha=w('cree', mas=-0.05), tam=58)],
       sale=w('algo así', mas=-0.4))
sonido('tictac', w('reloj', mas=-0.1), vol=0.26, dur=2.6, fo=0.8)

# 8 · El fondo del mar: el naufragio es del siglo I a. C.; ¿y si el bulto cayó después? Un aro a trazos que se hunde.
toma('estatuas', w('algo así', mas=-0.25), entra='corte', centro=(0.45, 0.5), mov=dict(zoom=(1.12, 1.2), panX=(0.01, -0.01)),
     luz=(0.5, 0.1), luzColor=(0.7, 0.95, 1.0), luzI=0.18, luzR=0.35, ventana=(0.22, 0.75, 0.5), ventanaI=0.3)
grafico('senal', w('algo así', mas=-0.25), w('Años', mas=-0.25), id='senal-fondo', z=3,
        marcas=[dict(u=0.52, v=0.34, rx=170, ry=110, t=w('encaja', mas=0.1), sale=w('Años', mas=-0.5),
                     n='EL NAUFRAGIO', s='siglo I a. C.', lado='der'),
                dict(u=0.3, v=0.8, r=70, t=w('cayó', mas=-0.1), sale=w('Años', mas=-0.5), cae=0.55, discontinua=True,
                     n='¿EL BULTO?', s='¿siglos después?', lado='der')])
sonido('travesia', w('algo así', mas=-0.3), vol=0.14)
sonido('whoosh', w('cayó', mas=0.2), vol=0.14)

# 9 · Rehm, ante los pedazos; la rueda de Stais, señalada en «sospecha».
toma('pedazos', w('Años', mas=-0.25), entra='oscuro', centro=(0.735, 0.48), mov=dict(zoom=(1.5, 1.6), panY=(-0.01, 0.0)),
     luz=(0.62, 0.42), luzI=0.18, ventana=(0.22, 0.6, 0.6), ventanaI=0.6)
bloque(150, 560, [E('FILÓLOGO ALEMÁN', w('filólogo')), N('Albert Rehm', w('Albert'))], sale=w('calculadora', mas=-0.5))
grafico('senal', w('Años', mas=-0.25), w('calculadora', mas=-0.25), id='senal-rehm', z=3,
        marcas=[dict(u=0.735, v=0.48, rx=70, ry=118, t=w('sospecha', mas=-0.05), sale=w('calculadora', mas=-0.5),
                     n='LA RUEDA', lado='izq')])

# 10 · «Una calculadora del cielo»: una rueda que gira sobre las estrellas.
toma('noche', w('calculadora', mas=-0.25), entra='corte', mov=dict(zoom=(1.08, 1.13), panY=(-0.01, 0.01)),
     luz=(0.4, 0.3), luzColor=(0.75, 0.85, 1.0), luzI=0.1, ventana=(0.24, 0.72, 0.5), ventanaI=0.45)
grafico('rueda', w('calculadora', mas=-0.25), w('pero', mas=-0.3), id='rueda-cielo', centro=[0.3, 0.34], radio=210, dientes=48,
        giro=9, en=w('calculadora', mas=-0.1), sale=w('pero', mas=-0.5))
bloque(150, 700, [T('Una calculadora del cielo', w('calculadora', mas=0.05), em='cielo', tam=96)], sale=w('pero', mas=-0.45))
sonido('grillos', w('calculadora', mas=-0.25), vol=0.1, dur=2.4, fi=0.3, fo=0.5)

# 11 · Pero no puede ver dentro: el bulto de cerca, y lo que lo sella, señalado palabra a palabra.
toma('bulto', w('pero', mas=-0.25), entra='corte', centro=(0.62, 0.52), mov=dict(zoom=(1.55, 1.7), camX=(0.01, -0.01)),
     luz=(0.62, 0.3), luzI=0.14, luzR=0.3, ventana=(0.22, 0.45, 0.55), ventanaI=0.45)
grafico('senal', w('pero', mas=-0.25), w('Durante', mas=-0.3), id='senal-sello', z=3,
        marcas=[dict(u=0.62, v=0.5, r=170, t=w('dentro', mas=-0.1), sale=w('El bronce', mas=-0.3), n='¿QUÉ HAY DENTRO?', lado='izq', foco=True),
                dict(u=0.63, v=0.48, r=70, t=w('bronce', 2, mas=-0.05), sale=w('Durante', mas=-0.55), n='BRONCE', lado='izq'),
                dict(u=0.56, v=0.67, r=64, t=w('piedra', 2, mas=-0.05), sale=w('Durante', mas=-0.55), n='PIEDRA', lado='izq', vert='aba'),
                dict(u=0.78, v=0.56, r=72, t=w('cal', mas=-0.05), sale=w('Durante', mas=-0.55), n='CAL MARINA', lado='izq', vert='aba')])

# 12 · El cajón a oscuras: los años pasan hasta 1951.
toma('cajon', w('Durante', mas=-0.3), entra='corte', mov=dict(zoom=(1.04, 1.12), camX=(-0.01, 0.01)),
     luz=(0.7, 0.35), luzI=0.2, luzR=0.3, ventana=(0.27, 0.48, 0.62), ventanaI=0.45)
sonido('cajon', w('Durante', mas=-0.25), vol=0.32, dur=2.0, fo=0.4)
bloque(150, 360, [E('MEDIO SIGLO', w('medio')), C('1951', w('él', mas=0.2), desde=1902, dur=2.4, tam=230)], sale=DUR - 0.75)
sonido('tictac2', w('medio', mas=-0.1), vol=0.18, dur=3.6, fi=0.3, fo=0.8)

MUSICA = dict(subidas=[(w('pedazos', fin=True, mas=0.15), w('El diecisiete', mas=-0.1), 0.3)])
