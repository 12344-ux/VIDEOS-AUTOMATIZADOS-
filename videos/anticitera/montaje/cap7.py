# Capítulo VII · ¿Quién lo construyó? Lo lee kit/montar.py; ver su cabecera.
# Forma: una investigación con tres clases de pistas: las monedas (el mapa desde el naufragio hasta Pérgamo y
# Éfeso), la fecha de la espiral (una línea de tiempo) y el calendario (el mapa de Corinto a Siracusa); luego los
# textos de Cicerón y Rodas, y al final las manos de un artesano: no fue la primera máquina.

ANT, PER, EFE, COR, SIR, ROD = (1248, 765), (1587, 404), (1601, 536), (1216, 536), (549, 632), (1677, 703)

# 1 · El barco cargado: nadie firmó la máquina.
toma('carguero', 0, entra='negro', mov='der', luz=(0.66, 0.32), luzI=0.2, ventana=(0.25, 0.55, 0.6))
sonido('olas', 0.3, vol=0.18, dur=w('El barco', mas=-0.2), ini=8, fi=1.0, fo=0.5)
sonido('jarcias', 0.6, vol=0.22, dur=w('El barco', mas=-0.5), ini=1, fi=0.8, fo=0.5)

# 2 · Las monedas del naufragio.
toma('monedas', w('El barco', mas=-0.3), entra='corte', capas=False, mov=dict(zoom=(1.05, 1.11), panX=(0.01, -0.005)),
     luz=(0.66, 0.3), luzColor=(0.75, 0.95, 0.9), luzI=0.18, ventana=(0.25, 0.5, 0.6), ventanaI=0.5)
bloque(150, 400, [E('HUNDIMIENTO', w('hundió')), C('70–60', w('setenta', mas=0.1), unidad='a. C.', tam=190)], sale=w('Lo dicen', mas=-0.55))
sonido('monedas', w('El barco', mas=-0.1), vol=0.3, dur=1.6, fo=0.4)

# 3 · El mapa: del naufragio a Pérgamo y Éfeso.
toma('placa', w('Lo dicen', mas=-0.25), entra='corte', mov=dict(zoom=(1.04, 1.07)), brillo=0.55, luz=(0.7, 0.3), luzI=0.08,
     ventanaI=0.2)
grafico('mapa', w('Lo dicen', mas=-0.25), w('La máquina podría', mas=-0.3), id='mapa-a',
        revela=dict(t=w('Lo dicen', mas=-0.2), x=ANT[0], y=ANT[1]),
        puntos=[dict(n='ANTICITERA', s='el naufragio', x=ANT[0], y=ANT[1], t=w('dicen', mas=0.1), lado='izq'),
                dict(n='PÉRGAMO', s='monedas', x=PER[0], y=PER[1], t=w('Pérgamo'), lado='der'),
                dict(n='ÉFESO', s='monedas', x=EFE[0], y=EFE[1], t=w('Éfeso'), lado='der')],
        arcos=[dict(de=PER, a=ANT, t=w('Pérgamo', mas=0.35)), dict(de=EFE, a=ANT, t=w('Éfeso', mas=0.35))],
        camara=[[w('Lo dicen', mas=-0.25), 1.0, 1100, 580], [w('Pérgamo', mas=-0.3), 1.12, 1300, 600, 'power2.inOut'],
                [w('La máquina podría'), 1.2, 1340, 600, 'sine.inOut']])
sonido('whoosh', w('Lo dicen', mas=-0.3), vol=0.16)

# 4 · La fecha: la espiral empieza en el 205 a. C., mucho antes del naufragio.
toma('placa', w('La máquina podría', mas=-0.3), entra='oscuro', mov=dict(zoom=(1.07, 1.04)), brillo=0.55, luz=(0.7, 0.3), luzI=0.08,
     ventanaI=0.2)
grafico('linea', w('La máquina podría', mas=-0.3), w('Los meses', mas=-0.3), id='linea-a', rango=[-300, 0],
        dibuja=[w('La máquina podría'), 1.2], tramo=None,
        marcas=[dict(a=-65, n='h. 65 a. C.', s='naufragio', t=w('máquina podría', mas=0.4)),
                dict(a=-205, n='205 a. C.', s='la espiral de eclipses', t=w('doscientos', mas=0.15), lado='aba')],
        camara=[[w('La máquina podría', mas=-0.3), 1.0, 960, 560], [w('Los meses'), 1.06, 900, 570, 'sine.inOut']])
bloque(150, 160, [E('CARMAN Y EVANS · 2014', w('estudio'))], sale=w('Los meses', mas=-0.7))

# 5 · El calendario: Corinto y una de sus colonias, Siracusa.
toma('placa', w('Los meses', mas=-0.3), entra='corte', mov=dict(zoom=(1.04, 1.07)), brillo=0.55, luz=(0.7, 0.3), luzI=0.08,
     ventanaI=0.2)
grafico('mapa', w('Los meses', mas=-0.3), w('Más de un siglo', mas=-0.3), id='mapa-b',
        revela=dict(t=w('Los meses', mas=-0.3), x=COR[0], y=COR[1]),
        puntos=[dict(n='CORINTO', s='su calendario', x=COR[0], y=COR[1], t=w('Corinto'), lado='der'),
                dict(n='SIRACUSA', s='Arquímedes', x=SIR[0], y=SIR[1], t=w('Siracusa'), lado='aba')],
        arcos=[dict(de=COR, a=SIR, t=w('colonias', mas=-0.2))],
        camara=[[w('Los meses', mas=-0.3), 1.12, 1050, 560], [w('Siracusa', mas=-0.6), 1.0, 900, 600, 'power2.inOut'],
                [w('Más de un siglo'), 1.04, 880, 600, 'sine.inOut']])

# 6 · Cicerón y la esfera de Arquímedes.
toma('armilar', w('Más de un siglo', mas=-0.3), entra='oscuro', mov='empuje', luz=(0.75, 0.3), luzI=0.18,
     ventana=(0.25, 0.5, 0.62), ventanaI=0.45)
bloque(150, 430, [E('CICERÓN', w('Cicerón')), D('«Sobre la república»', w('escribió')),
                  D('La esfera que Marcelo se llevó de Siracusa', w('esfera'))],
       sale=w('Y contó', mas=-0.6))
sonido('paginas', w('Cicerón', mas=-0.2), vol=0.2, dur=1.4)

# 7 · Rodas, en el mapa: Posidonio (el plano de la ciudad parecía moderno; el mapa sigue la investigación).
toma('placa', w('Y contó', mas=-0.3), entra='barrido', mov=dict(zoom=(1.04, 1.07)), brillo=0.55, luz=(0.7, 0.3), luzI=0.08,
     ventanaI=0.3)
grafico('mapa', w('Y contó', mas=-0.3), w('Ninguna', mas=-0.3), id='mapa-c',
        revela=dict(t=w('Y contó', mas=-1.9), x=ROD[0], y=ROD[1]),
        puntos=[dict(n='RODAS', s='Posidonio · Hiparco', x=ROD[0], y=ROD[1], t=w('Rodas'), lado='aba'),
                dict(n='ANTICITERA', x=ANT[0], y=ANT[1], t=w('Y contó', mas=-0.2), lado='izq')],
        arcos=[dict(de=ROD, a=ANT, t=w('astrónomos', mas=-0.2))],
        camara=[[w('Y contó', mas=-0.3), 1.3, 1460, 690], [w('Ninguna'), 1.4, 1480, 700, 'sine.inOut']])
bloque(150, 470, [E('MAESTRO DE CICERÓN', w('maestro')), N('Posidonio', w('Posidonio'))], sale=w('Ninguna', mas=-0.6))
sonido('olas', w('Y contó', mas=-0.3), vol=0.1, dur=6.2, ini=40, fi=0.6, fo=0.8)

# 8 · Las manos de un artesano: no fue la primera.
toma('artesano', w('Ninguna', mas=-0.3), entra='oscuro', mov=dict(zoom=(1.05, 1.13), camX=(0.01, -0.01)), luz=(0.7, 0.4),
     luzI=0.2, ventanaI=0.25)
sonido('fuego', w('Ninguna', mas=-0.3), vol=0.12, dur=DUR - w('Ninguna'), ini=5, fi=0.8, fo=1.4)

MUSICA = dict(subidas=[(w('pistas', fin=True, mas=0.1), w('El barco', mas=-0.1), 0.32)])
