# Corto 10 · «La carta» (organización): en 1948 los hermanos McDonald cerraron un restaurante que funcionaba, tacharon
# 16 de los 25 productos de su carta y bajaron la hamburguesa de 30 a 15 centavos. Lo lee
# canales/businessformen/kit/montar.py: cortos/10-la-carta. Vertical, unos 37 s, en bucle (CERRARON LO QUE FUNCIONABA ·
# Y LES FUE MEJOR, sobre el puesto). La idea, para que se entienda: la carta de 25 líneas y las 16 que se tachan.
#
# La receta de los cortos 7–9 m2, que funcionó (31-oct): la voz M2 del canal de supervivencia (recursos/modelo-voz), sin
# música y el sonido hecho de efectos: el ambiente de cada sitio, un whoosh en cada corte (los cortes que abren frase,
# 0,38 s antes, en la pausa) y el golpe de cada acción un fotograma después de su imagen; el bucle no salta.
formato(1080, 1920, voz0=0.1, cola=0.45)
subtitulos()
CORTE = -0.38
GOLPE = w('Crecer', mas=-0.55)

escena('s01', 'gancho', 0, foto='puesto',
       conf=dict(l1='Cerraron<br>lo que<br>funcionaba', l2='y les fue mejor', tam1=120, tam2=84, camara=[1.1, 0, -30], modo='inicio'))
escena('s02', 'foto', w('cerraron', mas=-0.12), foto='puesto',             # corte seco, en la palabra: el puesto, más cerca
       conf=dict(camara=[1.28, 1.34, 0, 40], textos=[
           dict(html='Cerrado', clase='sello', x=80, y=960, en=['cerraron', 1, -0.05], modo='sello'),
           dict(html='Y les iba bien', clase='etiqueta', x=80, y=300, en=['bien', 1, -0.12])]))
escena('s03', 'carta', w('Vendían', mas=CORTE), entrada='barrido')
escena('s04', 'foto', w('Quitaron', mas=CORTE), foto='hamburguesa', entrada='subida',
       conf=dict(camara=[1.0, 1.1, 0, 0], textos=[
           dict(html='✕ Platos', clase='etiqueta', x=80, y=300, en=['platos', 1, -0.08]),
           dict(html='✕ Cubiertos', clase='etiqueta', x=80, y=390, en=['cubiertos', 1, -0.08]),
           dict(html='✕ Camareros', clase='etiqueta', x=80, y=480, en=['camareros', 1, -0.08])]))
escena('s05', 'foto', w('Y con', mas=CORTE), foto='cocina', entrada='barrido',
       conf=dict(camara=[1.0, 1.1, 0, 0], cuenta=dict(etiqueta='La hamburguesa, en centavos', x=80, y=236,
                                                       pasos=[[30, ['treinta', 1, -0.05]], [15, ['quince', 1, -0.05]]])))
escena('s06', 'foto', w('Al principio', mas=CORTE), foto='cola', entrada='subida',
       conf=dict(camara=[1.0, 1.08, 0, 0], textos=[
           dict(html='Al principio: vendían menos', clase='etiqueta', x=80, y=300, en=['menos', 1, -0.12]),
           dict(html='No daban abasto', clase='sello', x=80, y=960, en=['abasto', 1, -0.05], modo='sello')]))
escena('s07', 'foto', w('Ese sistema', mas=CORTE), foto='puesto', entrada='barrido',
       conf=dict(camara=[1.18, 1.06, 0, 0], textos=[
           dict(html='Lo copió<br>medio mundo', clase='sello', x=80, y=880, en=['copió', 1, -0.05], modo='sello')]))
escena('s08', 'golpe', GOLPE, entrada='cortina',
       etq='Crecer', b1='No es añadir.', b2='Es quitar<br>lo que sobra.',
       conf={'etq': {'palabra': 'crecer', 'grande': True}, 'b1': {'palabra': 'no', 'n': 2, 'y': 380, 'tam': 130},
             'b2': {'palabra': 'es', 'n': 3, 'y': 640, 'tam': 130, 'sube': -24}, 'firma': True, 'firma_t': 2.6})
escena('s09', 'gancho', w('Por eso', mas=-0.15), foto='puesto',
       conf=dict(l1='Cerraron<br>lo que<br>funcionaba', l2='y les fue mejor', tam1=120, tam2=84, modo='vuelta',
                 en_l1=['por', 1, -0.05], en_l2=['por', 1, 0.3]))
DURACION = w('funcionaba', fin=True, mas=1.3)

sin_subtitulos(GOLPE, DURACION)                                   # la lección y el gancho: escritos en grande

# --- Sin música. Cada efecto, con su causa en pantalla.
T3, T4, T5, T6, T7 = (w(p, mas=CORTE) for p in ('Vendían', 'Quitaron', 'Y con', 'Al principio', 'Ese sistema'))
TAPA, VUELTA = GOLPE + 0.25, w('Por eso', mas=-0.15)

# El ambiente. Fuera, en el puesto (el gancho, «cerrado», la carta, el sistema y la vuelta): gente hablando al aire libre,
# más alta en la cola; la vuelta acaba donde empieza el gancho (P0) y el bucle no salta. En la cocina, la plancha. En la
# lección, el aire de una sala en silencio.
P0, FUERA, CERCA = 10.0, 0.07, 0.11
sonido('3094', 0, vol=FUERA, ini=P0, dur=TAPA + 0.05,
       puntos=[(T4, FUERA), (T4 + 0.4, 0.05), (T5, 0.05), (T5 + 0.4, 0.03), (T6, 0.03), (T6 + 0.4, CERCA), (T7, CERCA),
               (T7 + 0.4, FUERA), (TAPA - 0.04, FUERA), (TAPA + 0.03, 0.0)])
sonido('3094', VUELTA - 0.25, vol=FUERA, ini=P0 - (DURACION - VUELTA + 0.25), dur=DURACION - VUELTA + 0.25, fi=0.3)
sonido('0144', T5 - 0.25, vol=0.12, ini=2.0, dur=T6 + 0.65 - T5, fi=0.3, fo=0.4)                  # la plancha de la cocina
sonido('1714', TAPA, vol=0.06, ini=5.0, dur=VUELTA + 0.3 - TAPA, fi=0.05, fo=0.3)          # la lección

# Las transiciones: un whoosh distinto en cada corte, con su pico en la mitad del barrido (0,21 s) más un fotograma.
for nombre, t, pico, vol in (('1795', T3, 0.34, 0.2), ('1800', T4, 0.33, 0.17), ('whoosh', T5, 0.16, 0.17),
                             ('1796', T6, 0.37, 0.18), ('1801', T7, 0.38, 0.2)):
    sonido(nombre, t + 0.243 - pico, vol=vol)
sonido('0572', TAPA + 0.033 - 0.44, ini=7.15, dur=1.3, fo=0.5, vol=0.3)                  # la cortina de la lección
sonido('2463', TAPA + 0.033 - 0.06, vol=0.5)                                               # …y su golpe

# Las acciones (un sello cae 0,12 s después de su ancla).
sonido('2460', w('cerraron', mas=-0.05 + 0.12 + 0.033 - 0.08), vol=0.6)                  # el sello CERRADO
sonido('0221', w('tacharon', mas=-0.05), vol=0.3, ini=18.5, dur=w('dieciséis', fin=True, mas=0.3) - w('tacharon', mas=-0.05),
       fi=0.05, fo=0.15)                                                                   # las 16 rayas, a lápiz
sonido('2461', w('dieciséis', mas=-0.1 + 0.22 + 0.033 - 0.07), vol=0.5)                   # −16
sonido('1184', w('platos', mas=-0.08 + 0.033 - 0.05), vol=0.25, ini=1.70, dur=0.6, fo=0.2)  # se llevan los platos
sonido('1174', w('cubiertos', mas=-0.08 + 0.033 - 0.1), vol=0.35, ini=0.4, dur=0.7, fo=0.2)  # y los cubiertos
sonido('2530', w('quince', mas=-0.05 + 0.033 - 0.15), vol=0.1, dur=1.2, fo=0.5)          # 15 centavos: el timbre del mostrador
sonido('2463', w('abasto', mas=-0.05 + 0.12 + 0.033 - 0.06), vol=0.5)                     # el sello NO DABAN ABASTO
sonido('2531', w('abasto', fin=True, mas=0.05), vol=0.22, dur=1.0, fo=0.4)                 # …y los pedidos, uno tras otro
sonido('0479', w('abasto', fin=True, mas=0.32), vol=0.2, dur=0.9, fo=0.4)
sonido('2461', w('copió', mas=-0.05 + 0.12 + 0.033 - 0.07), vol=0.6)                       # el sello LO COPIÓ MEDIO MUNDO
