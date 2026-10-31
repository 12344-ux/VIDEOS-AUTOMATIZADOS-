# Corto 7 · «El sueldo» (gestión de equipos): Henry Ford pagó 5 $ al día en 1914 para dejar de perder gente. Lo lee
# canales/businessformen/kit/montar.py: cortos/07-el-sueldo. Vertical, unos 45 s, en bucle (el último plano es el primero:
# PAGÓ EL DOBLE · PARA AHORRAR). La idea, para que se entienda: la puerta giratoria (entran 50.000 para 14.000 puestos) y
# las dos barras (1913 frente a 1915). Imágenes a pantalla completa (el velo ligero del kit) y, por petición del usuario
# (31-oct), solo efectos fuertes con su causa en pantalla («como el rayo») y la música más baja.
#
# Variante m2 (--variante m2, 31-oct, a petición del usuario: «la voz del canal de supervivencia, sin música de fondo y
# solo efectos de sonido, como transiciones o efectos adicionales»): la voz M2 (voz-m2/, recursos/variantes.json), sin
# música, y el sonido hecho de efectos: el ambiente de cada sitio, un whoosh distinto en cada corte y las acciones de la
# pantalla. Los cortes que abren una frase van 0,38 s antes, en la pausa, para que el whoosh no pise la voz (y la cortina
# del golpe, 0,55 s antes de «Lo más»: el interruptor suena antes de que hable).
formato(1080, 1920, voz0=0.1, cola=0.45)
subtitulos()
CORTE = -0.38 if VARIANTE == 'm2' else -0.15
GOLPE = w('Lo más', mas=-0.55 if VARIANTE == 'm2' else -0.45)

escena('s01', 'gancho', 0, foto='cadena', conf=dict(l1='Pagó<br>el doble', l2='para ahorrar', tam1=150, tam2=84, camara=[1.1, 0, -30], modo='inicio'))
escena('s02', 'foto', w('cinco', mas=-0.15), foto='sobre', entrada='barrido',
       conf=dict(camara=[1.0, 1.1, 0, 0], textos=[
           dict(html='5 $<small>al día</small>', clase='cifra', x=80, y=300, en=['cinco', 1, -0.05], modo='grande'),
           dict(html='Más del doble', clase='sello', x=80, y=960, en=['doble', 1, -0.05], modo='sello')]))
escena('s03', 'foto', w('Parecía', mas=CORTE), foto='puerta', entrada='subida',
       conf=dict(camara=[1.0, 1.08, 0, 20], textos=[
           dict(html='¿Una locura?', clase='titular', x=80, y=300, en=['locura', 1, -0.1]),
           dict(html='Su gente se iba', clase='sello', x=80, y=960, en=['iba', 1, -0.05], modo='sello')]))
escena('s04', 'flujo', w('El año', mas=CORTE), modo='entra', entrada='barrido')
escena('s05', 'foto', w('A cada', mas=CORTE), foto='taller', entrada='subida',
       conf=dict(camara=[1.0, 1.1, 0, 0], textos=[
           dict(html='1 · Buscarla', clase='etiqueta', x=80, y=300, en=['buscarla', 1, -0.08]),
           dict(html='2 · Enseñarle', clase='etiqueta', x=80, y=390, en=['enseñarle', 1, -0.08]),
           dict(html='Y perderla', clase='sello', x=80, y=960, en=['marchar', 1, -0.05], modo='sello')]))
escena('s06', 'flujo', w('Con los', mas=CORTE), modo='quedo', entrada='barrido')
escena('s07', 'barras', w('Al año', mas=CORTE), entrada='subida')
escena('s08', 'foto', w('El propio', mas=CORTE), foto='cadena', entrada='barrido',
       conf=dict(camara=[1.15, 1.25, -40, 0], textos=[
           dict(html='Para Ford:', clase='titular', x=80, y=300, en=['propio', 1, -0.05]),
           dict(html='Un recorte<br>de costes', clase='sello', x=80, y=880, en=['recortes', 1, -0.05], modo='sello')]))
escena('s09', 'golpe', GOLPE, entrada='cortina',
       etq='Lo más caro de un equipo', b1='No es<br>su sueldo.', b2='Es tener que<br>sustituirlo.',
       conf={'etq': {'palabra': 'lo', 'n': 3, 'grande': True}, 'b1': {'palabra': 'no', 'y': 380, 'tam': 130},
             'b2': {'palabra': 'es', 'n': 2, 'y': 680, 'tam': 130, 'sube': -24}, 'firma': True, 'firma_t': 3.4})
escena('s10', 'gancho', w('Por eso', mas=-0.15), foto='cadena',
       conf=dict(l1='Pagó<br>el doble', l2='para ahorrar', tam1=150, tam2=84, modo='vuelta', en_l1=['por', 1, -0.05], en_l2=['por', 1, 0.3]))
DURACION = w('doble', 2, fin=True, mas=1.3)

sin_subtitulos(GOLPE, DURACION)                  # la lección y el gancho: escritos en grande

if VARIANTE == 'm2':
    # --- Sin música. Cada efecto, con su causa en pantalla; los golpes caen un fotograma después de su imagen.
    T2, T3, T4, T5 = w('cinco', mas=-0.15), w('Parecía', mas=CORTE), w('El año', mas=CORTE), w('A cada', mas=CORTE)
    T6, T7, T8 = w('Con los', mas=CORTE), w('Al año', mas=CORTE), w('El propio', mas=CORTE)
    TAPA = GOLPE + 0.25                           # la cortina roja tapa la pantalla
    VUELTA, QUEDO = w('Por eso', mas=-0.15), w('quedó')

    # El ambiente. La fábrica (una imprenta Heidelberg: el traqueteo de una máquina de la época) suena fuerte donde se ve
    # la cadena de montaje (el gancho, «El propio Ford…» y la vuelta) y muy baja en lo demás. El interruptor la apaga en
    # la lección y queda el aire de la nave vacía (viento desde dentro: callada del todo, las pausas de la voz serían
    # silencios). La vuelta acaba en el punto de la grabación donde empieza el vídeo (P0): el bucle no salta.
    P0, ALTA, BAJA = 3.0, 0.08, 0.045
    sonido('3409', 0, vol=ALTA, ini=P0, dur=TAPA + 0.05,
           puntos=[(T2, ALTA), (T2 + 0.4, BAJA), (T8, BAJA), (T8 + 0.4, ALTA), (TAPA - 0.04, ALTA), (TAPA + 0.03, 0)])
    sonido('1714', TAPA, vol=0.06, ini=5.0, dur=VUELTA + 0.3 - TAPA, fi=0.05, fo=0.3)     # la nave vacía, en la lección
    sonido('3409', VUELTA, vol=ALTA, ini=P0 - (DURACION - VUELTA), dur=DURACION - VUELTA, fi=0.3)
    # La multitud: delante de la verja (la foto de la puerta), más baja en la corriente de gente del dibujo; fuera en el
    # taller; y se para con ella en «se quedó».
    sonido('3515', T3, vol=0.0, ini=17.0, dur=QUEDO + 0.5 - T3,
           puntos=[(T3 + 0.3, 0.2), (T4, 0.2), (T4 + 0.4, 0.1), (T5, 0.1), (T5 + 0.35, 0.0), (T6, 0.0), (T6 + 0.35, 0.1),
                   (QUEDO - 0.15, 0.1), (QUEDO + 0.45, 0.0)])

    # Las transiciones: un whoosh distinto en cada corte, con su pico en la mitad del barrido (0,21 s) más un fotograma.
    for nombre, t, pico, vol in (('1795', T3, 0.34, 0.21), ('1800', T5, 0.33, 0.16), ('whoosh', T6, 0.16, 0.17),
                                 ('1796', T7, 0.37, 0.2), ('1801', T8, 0.38, 0.17)):
        sonido(nombre, t + 0.243 - pico, vol=vol)
    # (en el corte al dibujo de la puerta giratoria ya suena el silbato, y en el del sobre, las monedas)
    sonido('0572', TAPA + 0.033 - 0.44, ini=7.15, dur=1.3, fo=0.5, vol=0.32)   # la cortina: el whoosh grande, con su pico al tapar
    sonido('3061', TAPA, vol=0.3)                                                # …y el interruptor: la fábrica se apaga

    # Las acciones.
    sonido('0193', w('cinco', mas=-0.02), vol=0.6, ini=0.05, dur=1.0, fo=0.3)        # las monedas caen sobre el sobre
    sonido('2460', w('doble', mas=0.02), vol=0.6)                                       # el sello MÁS DEL DOBLE: un golpe seco
    sonido('2461', w('iba', mas=0.03), vol=0.6)                                         # el sello SU GENTE SE IBA
    sonido('3321', w('iba', fin=True, mas=0.03), vol=0.23, ini=0.05, dur=0.8, fo=0.35)  # el silbato de la fábrica: se van
    sonido('3063', w('catorce', 2, mas=-0.06), vol=0.31)                               # se encienden los 14 puestos
    sonido('3283', w('contratar', mas=-0.21), vol=0.5, dur=2.0, fo=0.4)                # el contador: una calculadora de manivela
    sonido('3270', w('buscarla', mas=-0.25), vol=0.4)                                  # 1 · BUSCARLA (una tecla de la calculadora)
    sonido('3272', w('enseñarle', mas=-0.23), vol=0.4)                                 # 2 · ENSEÑARLE
    sonido('2463', w('marchar', mas=0.04), vol=0.6)                                    # el sello Y PERDERLA
    sonido('3270', w('dos', mas=-0.07), vol=0.35)                                      # la cifra de 1915: 2.000
    sonido('2460', w('recortes', mas=0.02), vol=0.6)                                   # el sello UN RECORTE DE COSTES
else:
    # --- Música: un lecho bajo (17–20 LU por debajo de la voz); se calla en el golpe.
    musica('lecho', 0, DURACION, vol=0.1, fi=0.05, fo=0.3,   # en el golpe, muy baja: callada del todo dejaba silencios
           puntos=[(w('Lo más', mas=-0.45), 0.1), (w('Lo más', mas=-0.2), 0.025), (w('Por eso', mas=-0.3), 0.025), (w('Por eso', mas=0.1), 0.1)])

    # --- Efectos: solo los que tienen su golpe en pantalla.
    sonido('0193', w('cinco', mas=-0.02), vol=0.6, ini=0.05, dur=1.0, fo=0.3)            # las monedas caen sobre el banco
    sonido('3321', w('iba', fin=True, mas=0.03), vol=0.3, ini=0.05, dur=0.8, fo=0.35)  # el silbato de la fábrica, en la pausa: se van
    sonido('impact-bass-2', w('Lo más', mas=-0.45), vol=0.02)                             # el golpe rojo, con la cortina (en la pausa)
