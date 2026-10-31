# Corto 8 · «La fórmula» (marca): en 1985 Coca-Cola cambió su fórmula, ganó las catas a ciegas y tuvo que volver atrás en
# 79 días. Lo lee canales/businessformen/kit/montar.py: cortos/08-la-formula. Vertical, unos 44 s, en bucle (GANÓ 200.000
# CATAS · Y FUE UN DESASTRE). La idea, para que se entienda: los dos vasos de la cata (gana la nueva) y los 79 días, uno a
# uno. Imágenes a pantalla completa; solo efectos fuertes con su causa en pantalla y la música baja (31-oct).
#
# Variante m2 (--variante m2, 31-oct): como la del 7, que funcionó mejor, la voz M2 del canal de supervivencia, sin
# música y con el sonido hecho de efectos (el ambiente de cada sitio, un whoosh en cada corte y las acciones). Los cortes
# que abren frase van 0,38 s antes, en la pausa, y la cortina de la lección, 0,55 s antes de «Tus clientes».
formato(1080, 1920, voz0=0.1, cola=0.45)
subtitulos()
CORTE = -0.38 if VARIANTE == 'm2' else -0.15
GOLPE = w('Tus clientes', mas=-0.55 if VARIANTE == 'm2' else -0.15)

escena('s01', 'gancho', 0, foto='lata', conf=dict(l1='Ganó 200.000<br>catas', l2='y fue un desastre', camara=[1.12, 0, -20], modo='inicio'))
escena('s02', 'catas', w('La nueva', mas=CORTE), entrada='barrido')
escena('s03', 'foto', w('Pepsi', mas=CORTE), foto='cata', entrada='subida',
       conf=dict(camara=[1.0, 1.1, 0, 0], textos=[
           dict(html='Pepsi gana clientes', clase='etiqueta', x=80, y=300, en=['Pepsi', 1, -0.05]),
           dict(html='Gana lo más dulce', clase='sello', x=80, y=960, en=['dulce', 1, -0.05], modo='sello')]))
escena('s04', 'foto', w('Así que', mas=CORTE), foto='lata', entrada='barrido',
       conf=dict(camara=[1.2, 1.32, 0, 30], textos=[
           dict(html='Una más dulce', clase='titular', x=80, y=300, en=['dulce', 2, -0.1]),
           dict(html='✓ Ganaba', clase='sello', x=80, y=960, en=['ganaba', 1, -0.05], modo='sello')]))
escena('s05', 'foto', w('La lanzó', mas=CORTE), foto='telefonos', entrada='subida',
       conf=dict(camara=[1.0, 1.1, 0, 0], textos=[
           dict(html='Abril de 1985', clase='etiqueta', x=80, y=300, en=['abril', 1, -0.05]),
           dict(html='5.000', clase='cifra', x=80, y=420, en=['cinco', 2, -0.05], modo='grande'),
           dict(html='llamadas de queja al día', clase='nota', x=86, y=640, en=['llamadas', 1, -0.05])]))
escena('s06', 'foto', w('La gente no', mas=CORTE), foto='estante', entrada='barrido',
       conf=dict(camara=[1.32, 1.38, 0, 0], origen='50% 100%', textos=[   # la fila de arriba (latas con letras), fuera
           dict(html='No querían<br>una mejor.', clase='titular', x=80, y=300, en=['quería', 1, -0.05]),
           dict(html='Querían la suya', clase='sello', x=80, y=960, en=['suya', 1, -0.08], modo='sello')]))
escena('s07', 'calendario', w('Setenta', mas=CORTE), entrada='subida')
escena('s08', 'golpe', GOLPE, entrada='cortina',
       etq='Tus clientes', b1='No compran solo<br>lo que vendes.', b2='Compran lo que<br>significa<br>para ellos.',
       conf={'etq': {'palabra': 'tus', 'grande': True}, 'b1': {'palabra': 'no', 'n': 2, 'y': 360, 'tam': 86},
             'b2': {'palabra': 'compran', 'n': 2, 'y': 640, 'tam': 86, 'sube': -24}, 'firma': True, 'firma_t': 3.9})
escena('s09', 'gancho', w('Por eso', mas=-0.15), foto='lata',
       conf=dict(l1='Ganó 200.000<br>catas', l2='y fue un desastre', modo='vuelta', en_l1=['ganó', 1, -0.05], en_l2=['ganó', 1, 0.4]))
DURACION = w('perdió', fin=True, mas=1.3)

sin_subtitulos(GOLPE - 0.05, DURACION)                            # la lección y el gancho: escritos en grande

if VARIANTE == 'm2':
    # --- Sin música. Cada efecto, con su causa en pantalla; los golpes caen un fotograma después de su imagen.
    T2, T3, T4, T5 = w('La nueva', mas=CORTE), w('Pepsi', mas=CORTE), w('Así que', mas=CORTE), w('La lanzó', mas=CORTE)
    T6, T7 = w('La gente no', mas=CORTE), w('Setenta', mas=CORTE)
    TAPA, VUELTA = GOLPE + 0.25, w('Por eso', mas=-0.15)

    # El ambiente. Donde se ve la lata (el gancho, «una más dulce» y la vuelta), el burbujeo de un refresco recién servido
    # (el tramo estable de la grabación; la vuelta acaba donde empieza el gancho, P0, y el bucle no salta). La cata, el
    # murmullo de un bar con vasos; las quejas, una oficina con gente hablando; el estante, el calendario y la lección, el
    # aire de una sala en silencio.
    P0 = 6.0
    sonido('1933', 0, vol=1.0, ini=P0, dur=T2 + 0.35, fo=0.35)
    sonido('1933', T4 - 0.25, vol=1.0, ini=3.0, dur=T5 + 0.6 - T4, fi=0.3, fo=0.35)   # entra cruzándose con el bar
    sonido('1933', VUELTA, vol=1.0, ini=P0 - (DURACION - VUELTA), dur=DURACION - VUELTA, fi=0.3)
    sonido('0480', T2, vol=0.2, ini=6.0, dur=T4 + 0.35 - T2, fi=0.3, fo=0.35)
    sonido('3094', T5, vol=0.07, ini=5.0, dur=T6 + 0.35 - T5, fi=0.3, fo=0.35)
    sonido('1714', T6, vol=0.06, ini=5.0, dur=VUELTA + 0.3 - T6, fi=0.3, fo=0.3)

    # Las transiciones: un whoosh distinto en cada corte, con su pico en la mitad del barrido (0,21 s) más un fotograma; en
    # el del estante, las botellas que chocan. La cortina de la lección llega justo después de abrirse la botella.
    for nombre, t, pico, vol in (('1795', T2, 0.34, 0.13), ('1800', T3, 0.33, 0.2), ('whoosh', T4, 0.16, 0.09),
                                 ('1796', T5, 0.37, 0.2), ('1801', T7, 0.38, 0.2)):
        sonido(nombre, t + 0.243 - pico, vol=vol)
    sonido('1394', T6 + 0.243 - 0.10, vol=0.23, dur=1.0, fo=0.3)                            # las botellas del estante
    sonido('0572', TAPA + 0.033 - 0.44, ini=7.15, dur=1.3, fo=0.5, vol=0.3)                # la cortina de la lección

    # Las acciones (un sello cae 0,12 s después de su ancla).
    sonido('2127', w('catas', mas=-0.2 + 0.1 + 0.033 - 0.07), vol=0.18)                   # gana el vaso B: el hielo
    sonido('2461', w('errores', mas=-0.15 + 0.22 + 0.033 - 0.07), vol=0.6)                # el sello UN ERROR
    sonido('2463', w('dulce', mas=-0.05 + 0.12 + 0.033 - 0.06), vol=0.56)                 # el sello GANA LO MÁS DULCE
    sonido('2460', w('ganaba', mas=-0.05 + 0.12 + 0.033 - 0.08), vol=0.4)                 # el sello ✓ GANABA
    sonido('0253', w('llamadas', mas=-0.1), vol=0.17, dur=1.4, fo=0.2)                     # suenan los teléfonos
    sonido('0250', w('queja', mas=-0.05), vol=0.15, dur=1.2, fo=0.3)
    sonido('2461', w('suya', mas=-0.08 + 0.12 + 0.033 - 0.07), vol=0.6)                   # el sello QUERÍAN LA SUYA
    sonido('2214', w('Setenta', mas=-0.1 + 0.033 - 0.07), vol=0.4)                         # los 79 días: pasan las hojas
    sonido('1932', w('siempre', fin=True, mas=-0.1), vol=0.23, ini=0.25, dur=0.9, fo=0.3)  # vuelve la de siempre: se abre
else:
    musica('lecho', 0, DURACION, vol=0.09, fi=0.05, fo=0.3,   # en el golpe, muy baja: callada del todo dejaba silencios
           puntos=[(w('Tus clientes', mas=-0.45), 0.09), (w('Tus clientes', mas=-0.2), 0.025), (w('Por eso', mas=-0.3), 0.025), (w('Por eso', mas=0.1), 0.09)])

    sonido('0253', w('llamadas', mas=-0.1), vol=0.22, ini=0.0, dur=1.4, fo=0.2)           # suenan los teléfonos
    sonido('0253', w('llamadas', mas=0.55), vol=0.15, ini=0.3, dur=1.1, fo=0.3)
    sonido('1932', w('siempre', fin=True, mas=-0.1), vol=0.4, ini=0.25, dur=0.9, fo=0.3)   # se abre la de siempre, en la pausa
