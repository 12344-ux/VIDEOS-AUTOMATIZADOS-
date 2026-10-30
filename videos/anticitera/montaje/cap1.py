# Capítulo I · Un bulto olvidado (Atenas, 1901–1951). Lo lee kit/montar.py; ver su cabecera.
# Forma: del brillo de las estatuas al olvido del bronce. La cámara se acerca cada vez más al fragmento
# (sala → bandeja → lupa → rueda) y, cuando nadie cree a Stais, vuelve a alejarse; acaba en un cajón a
# oscuras mientras el contador recorre los años hasta 1951, el año en que empieza el capítulo II.

# 1 · La sala del museo, desde negro. Rótulo del capítulo y lugar.
toma('museo', 0, entra='negro', mov='der', luz=(0.66, 0.2), luzI=0.22, luzR=0.32, ventana=(0.24, 0.6, 0.6))
bloque(150, 560, [E('ATENAS · 1901', w('Atenas')), D('37° 59′ N · 23° 44′ E', w('Nacional'))], sale=w('bulto', mas=-0.45))
sonido('pasos', 0.9, vol=0.22, dur=7.6, fi=0.8, fo=1.2)

# 2 · El bulto queda apartado; al secarse se parte: golpe de zoom en «pedazos».
toma('pedazos', w('El bulto', mas=-0.12), entra='corte', mov=dict(zoom=(1.05, 1.09), camX=(0.0, 0.0)),
     luz=(0.62, 0.42), luzI=0.18, ventana=(0.25, 0.5, 0.55), ventanaI=0.2,
     mas={'zoom': [[w('pedazos', mas=-0.05), 1.075], [w('pedazos', mas=0.3), 1.13, 'expo.out'], [w('El diecisiete'), 1.15, 'sine.inOut']]})
sonido('parquet', w('parte', mas=-0.08), vol=0.35, dur=1.0)

# 3 · La lupa de Stais: la fecha cifra a cifra, su nombre y la rueda que se dibuja donde está.
toma('lupa', w('El diecisiete', mas=-0.3), entra='barrido', mov='empuje', luz=(0.7, 0.45), luzI=0.2,
     ventana=(0.24, 0.42, 0.6), ventanaI=0.45)
bloque(150, 300, [E('17 DE MAYO', w('diecisiete')), C('1902', w('mil'), tam=210)], sale=w('el arqueólogo', mas=-0.25))
bloque(150, 470, [E('ARQUEÓLOGO', w('arqueólogo')), N('Valerios Stais', w('Valerios'))], sale=w('Incrustada', mas=1.0))
grafico('rueda', w('Incrustada'), w('Stais', 2, mas=-0.3), centro=[0.66, 0.40], radio=70, dientes=30, giro=0,
        en=w('rueda', mas=-0.1), sale=w('Stais', 2, mas=-0.55))
sonido('clic', w('rueda', mas=0.05), vol=0.3, dur=0.6)

# 4 · De vuelta en la sala, desde más cerca: nadie le cree; la fecha que se tacha.
toma('museo', w('Stais', 2, mas=-0.3), entra='corte', mov='retroceso', luz=(0.66, 0.2), luzI=0.22, luzR=0.32,
     ventana=(0.25, 0.55, 0.62), ventanaI=0.45)
sonido('tictac', w('reloj', mas=-0.1), vol=0.28, dur=2.2, fo=0.6)
bloque(150, 480, [E('DATACIÓN', w('encaja')), D('Siglo I a. C.', w('encaja', mas=0.25), tacha=w('después', mas=0.05)),
                  D('¿Muy posterior?', w('después', mas=0.4))], sale=w('Años', mas=-0.5))

# 5 · Rehm: la bandeja otra vez, muy cerca del borde de la rueda.
toma('pedazos', w('Años', mas=-0.25), entra='oscuro', mov=dict(zoom=(1.22, 1.3), panX=(-0.05, -0.04), panY=(-0.02, -0.03)),
     luz=(0.62, 0.42), luzI=0.18, ventana=(0.26, 0.5, 0.6), ventanaI=0.5)
bloque(150, 470, [E('FILÓLOGO ALEMÁN', w('filólogo')), N('Albert Rehm', w('Albert'))], sale=w('El bronce', mas=-0.55))

# 6 · El cajón a oscuras: los años pasan hasta 1951.
toma('cajon', w('El bronce', mas=-0.3), entra='corte', mov=dict(zoom=(1.04, 1.12), camX=(-0.01, 0.01)),
     luz=(0.7, 0.35), luzI=0.2, luzR=0.3, ventana=(0.27, 0.48, 0.62), ventanaI=0.45)
sonido('cajon', w('El bronce', mas=-0.25), vol=0.32, dur=2.0, fo=0.4)
bloque(150, 360, [E('MEDIO SIGLO', w('medio')), C('1951', w('él', mas=0.2), desde=1902, dur=2.4, tam=210)], sale=DUR - 0.75)
sonido('tictac2', w('medio', mas=-0.1), vol=0.18, dur=3.6, fi=0.3, fo=0.8)

MUSICA = dict(subidas=[(w('pedazos', fin=True, mas=0.15), w('El diecisiete', mas=-0.1), 0.3)])
