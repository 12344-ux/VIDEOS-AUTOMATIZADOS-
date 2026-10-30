# Capítulo VIII · Lo que el mar guardó. Lo lee kit/montar.py; ver su cabecera.
# Forma: el hueco de más de mil cuatrocientos años en una línea de tiempo; la fundición (por qué no quedan más);
# las dos preguntas abiertas (el anillo de 354 agujeros y las ruedas que se atascan); el museo de hoy, la noche
# sobre la isla y, de vuelta al principio, el fragmento: el cielo se oscurece y aterriza el título con los créditos.

DURACION = round(ULTIMA + 13.0, 2)

# 1 · El reloj astronómico medieval, bajo el rótulo del capítulo.
toma('reloj', 0, entra='negro', mov='empuje', luz=(0.68, 0.36), luzI=0.2, ventana=(0.25, 0.5, 0.62), ventanaI=0.45)
sonido('tictac3', 0.5, vol=0.16, dur=2.6, fi=0.6, fo=0.6)

# 2 · La línea de tiempo: del siglo II a. C. al siglo XIV, nada igual.
toma('placa', VOZ0 - 0.05, entra='oscuro', mov=dict(zoom=(1.04, 1.08)), brillo=0.55, luz=(0.7, 0.3), luzI=0.08, ventanaI=0.2)
grafico('linea', VOZ0 - 0.05, w('El bronce', mas=-0.3), id='linea-b', rango=[-300, 1500],
        dibuja=[w('Anticitera', mas=-0.2), 3.2],
        marcas=[dict(a=-100, n='ANTICITERA', s='siglo II a. C.', t=w('Anticitera'), alto=90),
                dict(a=1364, n='1364', s='el astrario de Dondi', t=w('relojes', mas=0.2), alto=90)],
        tramo=dict(a0=-100, a1=1364, t=w('complejo', mas=-0.2), n='más de 1.400 años sin nada igual'),
        camara=[[VOZ0 - 0.05, 1.5, 560, 560], [w('pierde'), 1.5, 640, 560, 'sine.inOut'], [w('relojes', mas=-0.9), 1.0, 960, 590, 'power2.inOut']])
sonido('viento', VOZ0, vol=0.1, dur=9.0, fi=0.8, fo=1.0)

# 3 · La fundición: el bronce valía dinero.
toma('fundicion', w('El bronce', mas=-0.3), entra='corte', mov='empuje', luz=(0.72, 0.5), luzColor=(1.0, 0.7, 0.4), luzI=0.22,
     ventana=(0.25, 0.5, 0.6), ventanaI=0.45)
bloque(150, 560, [E('FUNDIDAS', w('fundidas', mas=-0.3)), D('Casi todo el bronce antiguo acabó reciclado', w('fundidas', mas=0.3))],
       sale=w('Y aún', mas=-0.6))
sonido('fuego', w('El bronce', mas=-0.3), vol=0.2, dur=8.6, ini=3, fi=0.3, fo=0.6)
sonido('yunque', w('valía', mas=0.1), vol=0.16, dur=1.2)

# 4 · La primera pregunta: el anillo de agujeros.
toma('placa', w('Y aún', mas=-0.3), entra='oscuro', mov=dict(zoom=(1.04, 1.08), camX=(-0.006, 0.006)), brillo=0.58,
     luz=(0.7, 0.3), luzI=0.1, ventana=(0.24, 0.5, 0.55), ventanaI=0.35)
grafico('anillo', w('Y aún', mas=-0.3), w('Otros', mas=-0.3), n=354, cx=1300, arco=0.23,
        aparece=w('agujeros', mas=-0.2), cuenta0=w('contaron'), cuenta1=w('cuatro', mas=0.1))
bloque(150, 300, [E('GLASGOW · 2024', w('veinticuatro')), D('Graham Woan y Joseph Bayley', w('astrónomos'))], sale=w('Lo más', mas=-0.5))
bloque(150, 330, [E('AGUJEROS', w('probable')), C('354', w('cuatro', mas=0.1), desde=0, dur=1.6, tam=200),
                  D('365: el año del Sol', w('lunar'), tacha=w('Sol', mas=0.1))], sale=w('Otros', mas=-0.55))
sonido('escaner', w('agujeros', mas=-0.3), vol=0.12, dur=1.0)

# 5 · La segunda pregunta: ¿funcionaba? Dos ruedas que se atascan.
toma('placa', w('Otros', mas=-0.3), entra='corte', mov=dict(zoom=(1.06, 1.1), camX=(0.006, -0.006)), brillo=0.58,
     luz=(0.7, 0.3), luzI=0.1, ventana=(0.24, 0.5, 0.55), ventanaI=0.35)
grafico('atasco', w('Otros', mas=-0.3), w('Quizá', mas=-0.3), entra=w('dudan'), atasco=w('atascado', mas=0.1))
bloque(150, 300, [E('MAR DEL PLATA', w('argentinos')), D('Preprint de 2025, sin revisión por pares', w('argentinos', mas=0.3))], sale=w('errores', mas=-0.3))
bloque(150, 330, [E('ATASCO ANTES DE', w('dientes', mas=-0.2)), C('120', w('meses', mas=0.1), desde=0, dur=1.2, unidad='días', tam=200)],
       sale=w('Quizá', mas=-0.6))
sonido('tictac', w('dudan', mas=0.2), vol=0.2, dur=w('atascado', mas=0.1) - w('dudan', mas=0.2))
sonido('clic', w('atascado', mas=0.08), vol=0.32, dur=0.5)

# 6 · El museo hoy.
toma('vitrina', w('Quizá', mas=-0.3), entra='oscuro', mov='retroceso', luz=(0.7, 0.35), luzI=0.18, ventanaI=0.3)

# 7 · La noche sobre la isla.
toma('noche', w('Pero', mas=-0.3), entra='corte', mov=dict(zoom=(1.05, 1.1), panY=(0.01, -0.01)), luz=(0.6, 0.25),
     luzColor=(0.85, 0.92, 1.0), luzI=0.1, ventanaI=0.2)
sonido('grillos', w('Pero', mas=-0.3), vol=0.12, dur=w('Un trozo') - w('Pero') + 0.4, fi=0.6, fo=0.6)
sonido('olas', w('Pero', mas=-0.3), vol=0.14, dur=w('Un trozo') - w('Pero') + 0.4, ini=60, fi=0.6, fo=0.6)

# 8 · El fragmento de la apertura: el cielo se oscurece y aterriza el título.
toma('fragmento', w('Un trozo', mas=-0.3), entra='oscuro', capas=False, centro=(0.7307, 0.4648),
     mov=dict(zoom=(1.04, 1.12)), luz=(0.72, 0.3), luzI=0.15, ventana=(0.3, 0.5, 0.75), ventanaI=0.45,
     mas={'brillo': [[w('oscurecerse', mas=-0.2), 1.0], [w('cielo', fin=True, mas=0.8), 0.32, 'power2.inOut']]})
bloque(150, 250, [T('El mecanismo de Anticitera', ULTIMA + 1.0, em='Anticitera', tam=118),
                  P('Voz sintética generada por IA (Supertonic-3).', ULTIMA + 2.6),
                  P('Imágenes generadas por IA: ilustraciones, no fotografías del mecanismo.', ULTIMA + 2.85),
                  P('Música: MusicGen (Meta). Efectos: BigSoundBank (CC0).', ULTIMA + 3.1),
                  P('Fuentes: Freeth y otros (Nature, 2006 y 2008; Scientific Reports, 2021) · Price (1974) · '
                    'Carman y Evans (2014) · Woan y Bayley (2024) · Szigety y Arenas (2025, sin revisar).', ULTIMA + 3.35)],
       sale=DURACION - 0.95, ancho=1560)
sonido('golpe', ULTIMA + 0.96, vol=0.5, dur=2.1)

MUSICA = dict(subidas=[(w('hundió', fin=True, mas=0.1), w('Y aún', mas=-0.1), 0.32)])
