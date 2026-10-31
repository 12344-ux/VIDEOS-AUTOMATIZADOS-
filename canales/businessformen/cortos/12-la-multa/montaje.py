# Corto 12 · «La multa» (estrategia y clientes): en el año 2000 Blockbuster ganó unos 800 millones de dólares con las
# multas por devolver tarde las películas, lo que más odiaban sus clientes; Netflix, que las había quitado en 1999, le
# ofreció venderse por 50 millones y Blockbuster dijo que no; quebró en 2010. Lo lee canales/businessformen/kit/montar.py:
# cortos/12-la-multa. Vertical, unos 42 s, en bucle (800 MILLONES EN MULTAS · Y QUEBRÓ, sobre el videoclub). La idea,
# para que se entienda: dos barras a la misma escala, las multas (800 M$) y lo que pedía Netflix (50 M$), y el NO.
#
# La receta de los cortos 7–9 m2, que funcionó (31-oct): la voz M2 del canal de supervivencia (recursos/modelo-voz), sin
# música y el sonido hecho de efectos: el ambiente de cada sitio, un whoosh en cada corte (los cortes que abren frase,
# 0,38 s antes, en la pausa) y el golpe de cada acción un fotograma después de su imagen; el bucle no salta.
formato(1080, 1920, voz0=0.1, cola=0.45)
subtitulos()
CORTE = -0.38
GOLPE = w('Si tu', mas=-0.55)

escena('s01', 'gancho', 0, foto='tienda',
       conf=dict(l1='800 millones<br>en multas', l2='y quebró', tam1=110, tam2=84, camara=[1.1, 0, -20], modo='inicio'))
escena('s02', 'cifras', w('unos', mas=-0.15), modo='multas', foto='tienda', titulo='Año 2000 · multas por devolver tarde')   # corte seco
escena('s03', 'foto', w('Un año antes', mas=CORTE), foto='sobre', entrada='subida',
       conf=dict(camara=[1.0, 1.08, 0, 0], textos=[
           dict(html='Alquiler por correo · 1999', clase='etiqueta', x=80, y=300, en=['correo', 1, -0.1]),
           dict(html='Sin multas', clase='sello', x=80, y=960, en=['multas', 2, -0.05], modo='sello'),
           dict(html='Netflix', clase='titular', x=80, y=400, en=['nétflix', 1, -0.05])]))
escena('s04', 'foto', w('Pagabas', mas=-0.12), foto='sobre',                # corte seco: el sobre, más cerca
       conf=dict(camara=[1.25, 1.32, 0, 30], textos=[
           dict(html='✓ Una cuota al mes', clase='etiqueta', x=80, y=300, en=['mes', 1, -0.1]),
           dict(html='✓ Sin fecha de devolución', clase='etiqueta', x=80, y=390, en=['quisieras', 1, -0.15])]))
escena('s05', 'cifras', w('En el año', 2, mas=CORTE), modo='oferta', foto='reunion', titulo='Año 2000 · la oferta de Netflix',
       entrada='barrido')
escena('s06', 'foto', w('Diez años', mas=CORTE), foto='cerrada', entrada='subida',
       conf=dict(camara=[1.0, 1.08, 0, 0], textos=[
           dict(html='Quiebra · 2010', clase='sello', x=80, y=960, en=['quebró', 1, 0.12, 'fin'], modo='sello')]))
escena('s07', 'golpe', GOLPE, entrada='cortina',
       etq='Si tu negocio vive', b1='del enfado<br>de tus clientes,', b2='alguien vendrá<br>a llevárselos.',
       conf={'etq': {'palabra': 'si', 'grande': True}, 'b1': {'palabra': 'del', 'y': 360, 'tam': 104},
             'b2': {'palabra': 'alguien', 'y': 640, 'tam': 104, 'sube': -24}, 'firma': True, 'firma_t': 3.4})
escena('s08', 'gancho', w('Por eso', mas=-0.15), foto='tienda',
       conf=dict(l1='800 millones<br>en multas', l2='y quebró', tam1=110, tam2=84, modo='vuelta',
                 en_l1=['por', 3, -0.05], en_l2=['por', 3, 0.3]))
DURACION = w('quebró', 2, fin=True, mas=1.3)

sin_subtitulos(GOLPE, DURACION)                                   # la lección y el gancho: escritos en grande

# --- Sin música. Cada efecto, con su causa en pantalla.
T2, T4 = w('unos', mas=-0.15), w('Pagabas', mas=-0.12)
T3, T5, T6 = w('Un año antes', mas=CORTE), w('En el año', 2, mas=CORTE), w('Diez años', mas=CORTE)
TAPA, VUELTA = GOLPE + 0.25, w('Por eso', mas=-0.15)

# El ambiente: el aire del videoclub de noche (una ventilación), más bajo bajo las cifras y en casa (el sobre); en la
# tienda cerrada, el viento dentro; en la lección, el aire de una sala en silencio. La vuelta acaba donde empieza el
# gancho (P0) y el bucle no salta.
P0, ALTA, BAJA = 10.0, 0.045, 0.025
sonido('3598', 0, vol=ALTA, ini=P0, dur=T6 + 0.45,
       puntos=[(T2, ALTA), (T2 + 0.3, BAJA), (T6, BAJA), (T6 + 0.4, 0.0)])
sonido('3598', VUELTA - 0.25, vol=ALTA, ini=P0 - (DURACION - VUELTA + 0.25), dur=DURACION - VUELTA + 0.25, fi=0.3)
sonido('1714', T6, vol=0.09, ini=20.0, dur=TAPA + 0.05 - T6, fi=0.3, fo=0.05)          # la tienda cerrada
sonido('1714', TAPA, vol=0.06, ini=5.0, dur=VUELTA + 0.3 - TAPA, fi=0.05, fo=0.3)       # la lección

# Las transiciones: en la del sobre suena el buzón; en las otras dos, un whoosh. La cortina de la lección es la persiana
# metálica que se cierra: su golpe final, al tapar.
sonido('1527', T3 - 0.05 - 0.15, vol=0.25, ini=0.4, dur=0.9, fo=0.3)                   # el sobre cae en el buzón, en la pausa
for nombre, t, pico, vol in (('1800', T5, 0.33, 0.17), ('1796', T6, 0.37, 0.18)):
    sonido(nombre, t + 0.243 - pico, vol=vol)
T_PERSIANA = TAPA + 0.033 - 1.2                                                           # la persiana baja…
sonido('2475', T_PERSIANA, vol=0.08, ini=8.9, dur=1.6, fo=0.4,
       puntos=[(TAPA - 0.12, 0.08), (TAPA - 0.02, 0.3)])                                  # …y golpea al tapar la cortina

# Las acciones.
sonido('3555', w('ochocientos', mas=-0.1), vol=0.3, ini=0.65, dur=0.8, fo=0.3)          # las multas se imprimen
sonido('2461', w('odiaban', mas=-0.1 + 0.22 + 0.033 - 0.07), vol=0.6)                   # el sello LO QUE MÁS ODIABAN
sonido('2463', w('multas', 2, mas=-0.05 + 0.12 + 0.033 - 0.06), vol=0.6)                 # el sello SIN MULTAS
sonido('2460', w('no', mas=-0.05 + 0.2 + 0.033 - 0.08), vol=0.48)                        # el NO de Blockbuster
sonido('2461', w('quebró', fin=True, mas=0.12 + 0.12 + 0.033 - 0.07), vol=0.6)           # el sello QUIEBRA · 2010
