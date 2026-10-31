# Corto 11 · «El pegamento» (innovación): en 1968 un químico de 3M buscaba un pegamento muy fuerte y le salió uno que
# apenas pegaba; años después, un compañero lo usó para que no se le cayeran los papelitos del libro del coro, y nació el
# Post-it (1980). Lo lee canales/businessformen/kit/montar.py: cortos/11-el-pegamento. Vertical, unos 43 s, en bucle (EL
# PEGAMENTO QUE NO PEGABA · ESTÁ EN TU ESCRITORIO, sobre las notas). La idea, para que se entienda: la nota que pega, se
# despega sin dejar marca y vuelve a pegar.
#
# La receta de los cortos 7–9 m2, que funcionó (31-oct): la voz M2 del canal de supervivencia (recursos/modelo-voz), sin
# música y el sonido hecho de efectos: el ambiente de cada sitio, un whoosh en cada corte (los cortes que abren frase,
# 0,38 s antes, en la pausa) y el golpe de cada acción un fotograma después de su imagen; el bucle no salta.
formato(1080, 1920, voz0=0.1, cola=0.45)
subtitulos()
CORTE = -0.38
GOLPE = w('Un fracaso', mas=-0.55)

escena('s01', 'gancho', 0, foto='notas',
       conf=dict(l1='El pegamento<br>que no pegaba', l2='está en tu escritorio', tam1=104, tam2=64, camara=[1.1, 0, -20], modo='inicio'))
escena('s02', 'foto', w('buscaba', mas=-0.12), foto='laboratorio',          # corte seco, en la palabra
       conf=dict(camara=[1.0, 1.08, 0, 0], textos=[
           dict(html='3M · 1968', clase='etiqueta', x=80, y=300, en=['buscaba', 1, 0.0]),
           dict(html='Un pegamento<br>muy fuerte', clase='titular', x=80, y=400, en=['pegamento', 1, -0.05])]))
escena('s03', 'despega', w('Le salió', mas=CORTE), entrada='barrido')
escena('s04', 'foto', w('No servía', mas=CORTE), foto='laboratorio', entrada='subida',
       conf=dict(camara=[1.25, 1.32, -30, 20], brillo=0.8, textos=[
           dict(html='No servía<br>para nada', clase='titular', x=80, y=300, en=['servía', 1, -0.05]),
           dict(html='Ningún uso', clase='sello', x=80, y=960, en=['uso', 1, -0.05], modo='sello')]))
escena('s05', 'foto', w('Hasta que', mas=CORTE), foto='coro', entrada='barrido',   # encuadre: los papelitos, el libro y
       conf=dict(camara=[1.5, 1.56, 0, 0], origen='100% 39%', textos=[                 # las manos; la cara del cantante, fuera
           dict(html='Un compañero, en el coro', clase='etiqueta', x=80, y=300, en=['coro', 1, -0.1]),
           dict(html='Perdía<br>las páginas', clase='sello', x=80, y=880, en=['páginas', 1, -0.05], modo='sello')]))
escena('s06', 'foto', w('Se acordó', mas=CORTE), foto='notas', entrada='subida',
       conf=dict(camara=[1.2, 1.28, 0, 0], textos=[
           dict(html='Un papel<br>que pega…', clase='titular', x=80, y=300, en=['pega', 1, -0.05]),
           dict(html='y se despega', clase='sello', x=80, y=960, en=['despega', 1, -0.05], modo='sello')]))
escena('s07', 'foto', w('En mil novecientos ochenta', mas=CORTE), foto='oficina', entrada='barrido',
       conf=dict(camara=[1.0, 1.08, 0, 0], textos=[
           dict(html='A la venta: 1980', clase='etiqueta', x=80, y=300, en=['ochenta', 1, -0.05]),
           dict(html='En cualquier<br>oficina', clase='sello', x=80, y=880, en=['oficina', 1, -0.05], modo='sello')]))
escena('s08', 'golpe', GOLPE, entrada='cortina',
       etq='Un fracaso', b1='es un producto', b2='que todavía<br>no ha encontrado<br>su problema.',
       conf={'etq': {'palabra': 'un', 'n': 7, 'grande': True}, 'b1': {'palabra': 'es', 'y': 360, 'tam': 110},
             'b2': {'palabra': 'que', 'n': 5, 'y': 560, 'tam': 92, 'sube': -24}, 'firma': True, 'firma_t': 3.7})
escena('s09', 'gancho', w('Por eso', mas=-0.15), foto='notas',
       conf=dict(l1='El pegamento<br>que no pegaba', l2='está en tu escritorio', tam1=104, tam2=64, modo='vuelta',
                 en_l1=['por', 1, -0.05], en_l2=['por', 1, 0.3]))
DURACION = w('escritorio', fin=True, mas=1.3)

sin_subtitulos(GOLPE, DURACION)                                   # la lección y el gancho: escritos en grande

# --- Sin música. Cada efecto, con su causa en pantalla.
T2 = w('buscaba', mas=-0.12)
T3, T4, T5, T6, T7 = (w(p, mas=CORTE) for p in ('Le salió', 'No servía', 'Hasta que', 'Se acordó', 'En mil novecientos ochenta'))
TAPA, VUELTA = GOLPE + 0.25, w('Por eso', mas=-0.15)

# El ambiente: el aire de un despacho o de un laboratorio (una ventilación), más alto donde se ve la mesa con las notas y
# en el laboratorio; en la iglesia del coro, el aire de una nave grande; en la oficina, gente tecleando; en la lección,
# el aire de una sala en silencio. La vuelta acaba donde empieza el gancho (P0) y el bucle no salta.
P0, ALTA, BAJA = 10.0, 0.04, 0.025
sonido('3598', 0, vol=ALTA, ini=P0, dur=TAPA + 0.05,
       puntos=[(T3, ALTA), (T3 + 0.4, BAJA), (T4, BAJA), (T4 + 0.4, ALTA), (T5, ALTA), (T5 + 0.4, 0.0), (T6, 0.0),
               (T6 + 0.4, ALTA), (T7, ALTA), (T7 + 0.4, BAJA), (TAPA - 0.04, BAJA), (TAPA + 0.03, 0.0)])
sonido('3598', VUELTA - 0.25, vol=ALTA, ini=P0 - (DURACION - VUELTA + 0.25), dur=DURACION - VUELTA + 0.25, fi=0.3)
sonido('1714', T5, vol=0.09, ini=20.0, dur=T6 + 0.4 - T5, fi=0.3, fo=0.4)               # la nave de la iglesia
sonido('1726', T7, vol=0.18, ini=3.0, dur=TAPA + 0.05 - T7, fi=0.3, fo=0.2)             # la oficina: teclados
sonido('1714', TAPA, vol=0.06, ini=5.0, dur=VUELTA + 0.3 - TAPA, fi=0.05, fo=0.3)       # la lección

# Las transiciones: un whoosh distinto en cada corte, con su pico en la mitad del barrido (0,21 s) más un fotograma.
for nombre, t, pico, vol in (('1795', T3, 0.34, 0.14), ('1800', T4, 0.33, 0.2), ('whoosh', T5, 0.16, 0.13),
                             ('1796', T6, 0.37, 0.16), ('1801', T7, 0.38, 0.2)):
    sonido(nombre, t + 0.243 - pico, vol=vol)
sonido('0572', TAPA + 0.033 - 0.44, ini=7.15, dur=1.3, fo=0.5, vol=0.3)                # la cortina de la lección
sonido('2463', TAPA + 0.033 - 0.06, vol=0.5)                                             # …y su golpe

# Las acciones (un sello cae 0,12 s después de su ancla; la nota de la escena dibujada, cuando la animación lo dice).
sonido('1242', T2, vol=0.18, ini=0.3, dur=1.6, fo=0.4)                                   # el químico vierte el líquido
sonido('2460', w('apenas', mas=-0.1 + 0.35 + 0.033 - 0.08), vol=0.4)                    # la nota cae y se pega
sonido('0299', w('despegaba', mas=-0.05), vol=0.25, ini=0.05, dur=0.45, fo=0.15)        # se despega
sonido('2463', w('volver', mas=-0.05 + 0.3 + 0.033 - 0.06), vol=0.4)                    # y vuelve a pegar
sonido('2460', w('uso', mas=-0.05 + 0.12 + 0.033 - 0.08), vol=0.6)                       # el sello NINGÚN USO
sonido('2212', w('páginas', mas=-0.3), vol=0.4, ini=0.6, dur=0.9, fo=0.3)               # pasan las páginas del libro
sonido('2461', w('páginas', mas=-0.05 + 0.12 + 0.033 - 0.07), vol=0.6)                   # el sello PERDÍA LAS PÁGINAS
sonido('2463', w('pega', mas=-0.05 + 0.033 - 0.06), vol=0.35)                           # UN PAPEL QUE PEGA…
sonido('0298', w('despega', mas=-0.12), vol=0.25, ini=0.05, dur=0.5, fo=0.15)            # …Y SE DESPEGA
sonido('2461', w('oficina', mas=-0.05 + 0.12 + 0.033 - 0.07), vol=0.6)                   # el sello EN CUALQUIER OFICINA
