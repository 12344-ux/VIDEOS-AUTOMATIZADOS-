# Corto 9 · «La cámara» (estrategia): Kodak construyó la primera cámara digital en 1975, la dejó en el laboratorio para
# proteger el carrete y quebró en 2012. Lo lee canales/businessformen/kit/montar.py: cortos/09-la-camara. Vertical, unos
# 44 s, en bucle (KODAK INVENTÓ ESTO · EN 1975, sobre el prototipo). La idea, para que se entienda: la ficha de 1975 (una
# foto de 10.000 píxeles que tarda 23 s) y las dos curvas que se cruzan. Imágenes a pantalla completa; solo efectos
# fuertes con su causa en pantalla y la música baja (31-oct).
#
# Variante m2 (--variante m2, 31-oct): como la del 7, que funcionó mejor, la voz M2 del canal de supervivencia, sin
# música y con el sonido hecho de efectos (el ambiente de cada sitio, un whoosh en cada corte y las acciones). Los cortes
# que abren frase van 0,38 s antes, en la pausa, y la cortina de la lección, 0,55 s antes de «Si no».
formato(1080, 1920, voz0=0.1, cola=0.45)
subtitulos()
CORTE = -0.38 if VARIANTE == 'm2' else -0.15
GOLPE = w('Si no', mas=-0.55 if VARIANTE == 'm2' else -0.45)

escena('s01', 'gancho', 0, foto='prototipo',
       conf=dict(l1='Kodak inventó<br>esto', l2='en 1975', tam1=104, camara=[1.12, 0, -20], modo='inicio', destello=['digital', 1, 0.05, 'fin']))
escena('s02', 'pixeles', w('Pesaba', mas=CORTE), entrada='barrido')
escena('s03', 'foto', w('Kódak la', mas=CORTE), foto='laboratorio', entrada='subida',
       conf=dict(camara=[1.0, 1.08, 0, 0], textos=[dict(html='Proyecto de laboratorio', clase='etiqueta', x=80, y=300, en=['laboratorio', 1, -0.1])]))
escena('s04', 'foto', w('Por qué', mas=CORTE), foto='carretes', entrada='barrido',
       conf=dict(camara=[1.0, 1.1, 0, 0], textos=[
           dict(html='Cada carrete: $', clase='etiqueta', x=80, y=300, en=['carrete', 1, -0.08]),
           dict(html='Cada revelado: $', clase='etiqueta', x=80, y=390, en=['revelado', 1, -0.08])]))
escena('s05', 'foto', w('Una cámara', mas=CORTE), foto='prototipo', entrada='subida',
       conf=dict(camara=[1.2, 1.3, 0, 20], brillo=0.75, textos=[
           dict(html='Sin carrete', clase='titular', x=80, y=300, en=['sin', 1, -0.05]),
           dict(html='Una amenaza', clase='sello', x=80, y=960, en=['amenaza', 1, -0.05], modo='sello')]))
escena('s06', 'curvas', w('Años', mas=CORTE), entrada='barrido')
escena('s07', 'foto', w('Y en dos', mas=CORTE), foto='fabrica', entrada='subida',
       conf=dict(camara=[1.0, 1.08, 0, 0], textos=[dict(html='Quiebra · 2012', clase='sello', x=80, y=960, en=['quiebra', 1, 0.12, 'fin'], modo='sello')]))
escena('s08', 'foto', w('Había', mas=CORTE), foto='prototipo', entrada='barrido',
       conf=dict(camara=[1.0, 1.06, 0, 0], textos=[
           dict(html='Inventó<br>el futuro', clase='titular', x=80, y=300, en=['inventado', 1, -0.05]),
           dict(html='Y lo dejó pasar', clase='sello', x=80, y=960, en=['pasar', 1, -0.05], modo='sello')]))
escena('s09', 'golpe', GOLPE, entrada='cortina',
       etq='Si no cambias tu negocio,', b1='Otro lo<br>cambiará', b2='por ti.',
       conf={'etq': {'palabra': 'si', 'grande': True}, 'b1': {'palabra': 'otro', 'y': 380, 'tam': 130},
             'b2': {'palabra': 'por', 'n': 2, 'y': 680, 'tam': 150, 'sube': -24}, 'firma': True, 'firma_t': 2.8})
escena('s10', 'gancho', w('Y todo', mas=-0.15), foto='prototipo',
       conf=dict(l1='Kodak inventó<br>esto', l2='en 1975', tam1=104, modo='vuelta', en_l1=['todo', 1, -0.05], en_l2=['todo', 1, 0.3]))
DURACION = w('esto', fin=True, mas=1.4)

sin_subtitulos(GOLPE, DURACION)                                   # la lección y el gancho: escritos en grande

if VARIANTE == 'm2':
    # --- Sin música. Cada efecto, con su causa en pantalla; los golpes caen un fotograma después de su imagen.
    T2, T3, T4, T5 = w('Pesaba', mas=CORTE), w('Kódak la', mas=CORTE), w('Por qué', mas=CORTE), w('Una cámara', mas=CORTE)
    T6, T7, T8 = w('Años', mas=CORTE), w('Y en dos', mas=CORTE), w('Había', mas=CORTE)
    TAPA, VUELTA = GOLPE + 0.25, w('Y todo', mas=-0.15)

    # El ambiente: el aire del laboratorio (una ventilación), más alto donde se ve el prototipo o el laboratorio y bajo en
    # los carretes y las curvas; en la fábrica abandonada, el viento dentro de la nave; bajo la lección, el aire de una sala
    # en silencio. La vuelta acaba donde empieza el gancho (P0): el bucle no salta.
    P0, ALTA, BAJA = 10.0, 0.04, 0.02
    sonido('3598', 0, vol=ALTA, ini=P0, dur=TAPA + 0.05,
           puntos=[(T4, ALTA), (T4 + 0.4, BAJA), (T5, BAJA), (T5 + 0.4, ALTA), (T6, ALTA), (T6 + 0.4, BAJA),
                   (T7, BAJA), (T7 + 0.4, 0.0), (T8, 0.0), (T8 + 0.4, ALTA), (TAPA - 0.04, ALTA), (TAPA + 0.03, 0.0)])
    sonido('3598', VUELTA, vol=ALTA, ini=P0 - (DURACION - VUELTA), dur=DURACION - VUELTA, fi=0.3)
    sonido('1714', T7, vol=0.09, ini=20.0, dur=T8 + 0.4 - T7, fi=0.3, fo=0.4)              # la fábrica abandonada
    sonido('1714', TAPA, vol=0.06, ini=5.0, dur=VUELTA + 0.3 - TAPA, fi=0.05, fo=0.3)       # la lección

    # Las transiciones: un whoosh distinto en cada corte, salvo donde ya suena la acción (el disparo al entrar la ficha, el
    # arrastre del carrete al entrar los carretes y el portazo antes del último prototipo). La cortina de la lección se
    # cierra como un obturador.
    for nombre, t, pico, vol in (('1795', T3, 0.34, 0.17), ('1800', T5, 0.33, 0.2), ('whoosh', T6, 0.16, 0.13),
                                 ('1796', T7, 0.37, 0.19)):
        sonido(nombre, t + 0.243 - pico, vol=vol)
    sonido('2819', T4 + 0.243 - 0.13, vol=0.5, dur=0.9)                                     # los carretes: el arrastre
    sonido('0572', TAPA + 0.033 - 0.44, ini=7.15, dur=1.3, fo=0.5, vol=0.3)                 # la cortina de la lección…
    sonido('2822', TAPA + 0.033 - 0.08, vol=0.5)                                             # …y el obturador

    # Las acciones (un sello cae 0,12 s después de su ancla).
    sonido('2821', w('digital', fin=True), vol=0.6, dur=0.4)                                 # el disparo, con el destello
    sonido('2463', w('cuatro', mas=-0.1 + 0.033 - 0.06), vol=0.6)                            # 3,6 KG: pesa
    T_FOTO = w('diez', mas=-0.1)                                                             # la foto se dibuja y se guarda:
    sonido('2157', T_FOTO + 0.033 - 0.11, vol=0.25, dur=0.5, fo=0.15)                         # arranca la cinta…
    sonido('2832', T_FOTO, vol=0.6, ini=1.0, dur=w('segundos', fin=True, mas=0.3) - T_FOTO, fi=0.1, fo=0.2)   # …y gira
    sonido('0339', w('carrete', mas=-0.08 + 0.033 - 0.05), vol=0.21)                         # CADA CARRETE: $
    sonido('0340', w('revelado', mas=-0.08 + 0.033 - 0.05), vol=0.34)                        # CADA REVELADO: $
    sonido('2461', w('amenaza', mas=-0.05 + 0.12 + 0.033 - 0.07), vol=0.6)                  # el sello UNA AMENAZA
    T_LAPIZ = T6 + 0.1
    sonido('0221', T_LAPIZ, vol=0.29, ini=18.5, dur=w('carrete', 3, fin=True) - T_LAPIZ, fi=0.1, fo=0.2)   # las curvas, a lápiz
    sonido('1501', w('quiebra', fin=True, mas=0.10), vol=0.21, ini=0.05, dur=0.8, fo=0.3)   # el portazo, con QUIEBRA · 2012
    sonido('2460', w('pasar', mas=-0.05 + 0.12 + 0.033 - 0.08), vol=0.47)                   # el sello Y LO DEJÓ PASAR
else:
    musica('lecho', 0, DURACION, vol=0.1, fi=0.05, fo=0.3,   # en el golpe, muy baja: callada del todo dejaba silencios
           puntos=[(w('Si no', mas=-0.45), 0.1), (w('Si no', mas=-0.2), 0.025), (w('Y todo', mas=-0.3), 0.025), (w('Y todo', mas=0.1), 0.1)])

    sonido('2821', w('digital', fin=True, mas=0.0), vol=0.6, ini=0.0, dur=0.4)           # el disparo (con el destello)
    sonido('2819', w('carrete', mas=-0.25), vol=0.5, ini=0.0, dur=0.9)                    # el arrastre del carrete
    sonido('1501', w('quiebra', fin=True, mas=0.05), vol=0.33, ini=0.05, dur=0.8, fo=0.3)  # el portazo, con el sello (en la pausa)
    sonido('impact-bass-2', w('Si no', mas=-0.45), vol=0.02)                              # el golpe rojo, con la cortina (en la pausa)
