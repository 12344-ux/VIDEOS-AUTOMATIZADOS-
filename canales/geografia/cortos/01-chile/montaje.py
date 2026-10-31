# Corto 1 de geografía · «¿Por qué Chile es tan largo?». Lo monta el kit de BusinessForMen con la marca del canal:
#   python3 canales/businessformen/kit/montar.py --canal canales/geografia cortos/01-chile
# Vertical, unos 60 s, en bucle: el último plano (Sudamérica, Chile en amarillo, la pregunta) es el primero. El mapa es el
# protagonista y la cámara vuela por él; cada razón tiene su propio mundo (el mapa del centro, el corte de la cordillera,
# el norte). Mapas: mapa.py (Natural Earth). Retención: ../../RETENCION.md.
import json
import os

formato(1080, 1920, voz0=0.1, cola=0.6)
subtitulos()
M = json.load(open(os.path.join(AQUI, 'recursos', 'mapa.json')))
sa, eu, ce, no = M['sa'], M['eu'], M['centro'], M['norte']
vecinos = ''.join(sa[k] for k in ('Argentina', 'Peru', 'Brazil', 'Paraguay', 'Uruguay'))

escena('g01', 'gancho', 0, tierra=sa['tierra'], vecinos=vecinos + sa['Bolivia'], chile=sa['Chile'], norte=sa['norte'],
       sur=sa['sur'], estrecho=sa['estrecho'])
escena('g02', 'europa', w('Puesto', mas=-0.12), tierra=eu['tierra'], chile=eu['chile'], oslo=eu['oslo'], sur=eu['sur'])
escena('g03', 'pregunta', w('Cómo', mas=-0.12), chile=sa['Chile'])
escena('g04', 'muralla', w('La primera', mas=-0.12), tierra=ce['tierra'], chile=ce['Chile'], argentina=ce['Argentina'],
       frontera=ce['frontera'], estrecho=ce['estrecho'])
escena('g05', 'tratado', w('La segunda', mas=-0.12))
escena('g06', 'largo', w('Pero eso', mas=-0.12), chile=sa['Chile'])
escena('g07', 'guerra', w('era', mas=-0.1), tierra=no['tierra'], vecinos=no['Argentina'], bolivia=no['Bolivia'],
       peru=no['Peru'], antes=no['antes'], ganado=no['ganado'], ex_bolivia=no['ex_bolivia'], ex_peru=no['ex_peru'],
       y24=no['y24'], ytope=no['ytope'], x_costa=no['x_costa'], x_frontera=no['x_frontera'])
escena('g08', 'respuesta', w('Una muralla', 2, mas=-0.12), chile=sa['Chile'])
escena('g09', 'puerta', w('Y por eso', mas=-0.12), tierra=sa['tierra'], vecinos=vecinos, bolivia=sa['Bolivia'],
       chile=sa['Chile'], marca_bolivia=sa['bolivia'])
DURACION = w('historia', fin=True, mas=0.9)

# Subtítulos, salvo donde la pantalla ya escribe lo que dice la voz.
sin_subtitulos(w('Puesto', mas=-0.12), w('La primera', mas=-0.12))       # NORUEGA, SÁHARA; ¿CÓMO…?, 3 RAZONES
sin_subtitulos(w('Pero eso', mas=-0.12), w('era', mas=-0.1))             # ¿Y LO LARGO?
sin_subtitulos(w('Una muralla', 2, mas=-0.12), w('Y por eso', mas=-0.12))  # MURALLA · TRATADO · GUERRA · CINTA

# --- Música: un lecho sin entrada (el bucle no empieza en silencio); se retira antes de la respuesta y vuelve.
musica('lecho', 0, DURACION, vol=0.26, fi=0.05, fo=0.3,
       puntos=[(w('Una muralla', 2, mas=-0.6), 0.26), (w('Una muralla', 2, mas=-0.15), 0.06),
               (w('cinta', mas=0.1), 0.06), (w('Y por eso', mas=-0.1), 0.26)])

# --- Efectos (cada uno con su causa en pantalla)
sonido('whoosh-short', w('cuatro', mas=-0.1), vol=0.22)                    # la regla se dibuja
sonido('pop', w('kilómetros', mas=0.05), vol=0.32)                         # 4.270 km aterriza
sonido('whoosh-cinematic', w('estrecho', mas=-0.25), vol=0.22, dur=1.4, fo=0.4)   # la cámara baja al punto más estrecho
sonido('click', w('noventa', mas=0.1), vol=0.45)                           # 90 km
sonido('whoosh', w('Puesto', mas=-0.15), vol=0.24)                         # Chile vuela a Europa
sonido('pop', w('Noruega', mas=0.02), vol=0.32)
sonido('pop', w('Sáhara', mas=0.02), vol=0.32)
sonido('whoosh-short', w('Cómo', mas=-0.15), vol=0.24)
for t in (w('tres'), w('tres', mas=0.12), w('tres', mas=0.24)):
    sonido('click', t, vol=0.35)                                            # las tres casillas
sonido('impact-bass-1', w('mapa', mas=0.0), vol=0.24)                      # la tercera, con candado
sonido('whoosh', w('La primera', mas=-0.15), vol=0.22)
sonido('0155', w('montañas', mas=-0.15), vol=0.28, ini=2.0, dur=2.0, fi=0.2, fo=0.5)   # viento en los Andes
sonido('pop', w('metros', mas=0.1), vol=0.3)
sonido('whoosh-short', w('oeste', mas=-0.15), vol=0.22)
sonido('click', w('franja', mas=0.0), vol=0.4)
sonido('whoosh', w('La segunda', mas=-0.15), vol=0.22)
sonido('key-press', w('mil', 3, mas=-0.03), vol=0.4)                       # 1881
sonido('1386', w('dividen', mas=-0.1), vol=0.55, ini=0.45, dur=0.7, fo=0.2)   # la gota cae en la cumbre
sonido('whoosh-short', w('Pacífico', 2, mas=-0.2), vol=0.2)
sonido('whoosh-short', w('Atlántico', mas=-0.2), vol=0.2)
sonido('impact-bass-2', w('largo', 2, mas=0.0), vol=0.3)                   # ¿Y LO LARGO?
sonido('whoosh', w('era', mas=-0.15), vol=0.22)
sonido('key-press', w('nueve', mas=-0.03), vol=0.4)                        # 1879
sonido('key-press', w('cuatro', 2, mas=-0.03), vol=0.4)                    # 1884
sonido('riser', w('ganó', mas=-1.6), vol=0.24, ini=2.3, dur=1.6, fo=0.1)          # el riser sube hasta 3,9 s
sonido('impact-bass-1', w('ganó', mas=0.02), vol=0.26)                     # el norte se vuelve amarillo
sonido('pop', w('setecientos', mas=0.25), vol=0.32)
for k, t in enumerate((w('muralla', 2), w('tratado', 2), w('guerra', 2))):
    sonido('click', t, vol=0.45)
sonido('chime', w('cinta', mas=0.0), vol=0.3)
sonido('whoosh', w('Y por eso', mas=-0.15), vol=0.22)
sonido('pop', w('Bolivia', 3, mas=0.02), vol=0.32)
sonido('click', w('mar', mas=0.0), vol=0.45)
sonido('whoosh-short', w('historia', fin=True, mas=0.15), vol=0.2, dur=0.35)  # vuelve al principio
