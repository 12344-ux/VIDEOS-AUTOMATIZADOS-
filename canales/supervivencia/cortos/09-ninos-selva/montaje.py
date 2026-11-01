# Corto 9 de supervivencia · «40 días en la selva» (los cuatro hermanos de la avioneta de Araracuara, Caquetá y Guaviare,
# Colombia, 1 de mayo a 9 de junio de 2023). Lo monta el kit de BusinessForMen con la marca del canal:
#   python3 canales/businessformen/kit/montar.py --canal canales/supervivencia cortos/09-ninos-selva
# Vertical, unos 81 s, en bucle: el último plano («Cuarenta días solos en la selva») es el primero (40 DÍAS · SOLOS EN LA
# SELVA). El secreto tachado: «quién los salvó» (segundo 8), que se lee en el 69 («Su hermana de 13 años»). El mapa de
# Colombia, de Natural Earth (mapa.py y escenas/mapa.html): la ruta de la avioneta y dónde cayó. Son menores y reales:
# siempre de espaldas y de lejos. Retención: ../../../RETENCION.md.
# Sonido (ver ../../CANAL.md, la regla desde el corto 3): solo efectos fuertes con su golpe en pantalla y sin ambientes de
# fondo: las ramas que se quiebran cuando cae la avioneta (el mapa tiembla), el helicóptero y los ladridos del perro. La
# música, 16–20 LU bajo la voz. Medido con audio/revisar_mezcla.py antes de renderizar.
import json
import os

formato(1080, 1920, voz0=0.1, cola=0.7)
subtitulos()
M = json.load(open(os.path.join(AQUI, 'recursos', 'mapa.json')))

FICHA = dict(cab='Quién los salvó', linea='Durante 40 días:', tapada='Su hermana<br>de 13 años')
GANCHO = dict(cifra='40', tam=360, unidad='días', linea='Solos en la selva')
escena('s01', 'gancho', 0, foto='selva', conf=dict(GANCHO, camara=[1.1, 0, 30], modo='inicio'))
escena('s02', 'ficha', w('Pero quien', mas=-0.12), fondo='selva',
       conf=dict(FICHA, modo='oculta', en=['quien', 1, -0.1], escribe=[['quien', 1, 0.0], ['adulto', 1, 0.0, 'fin']],
                 barra=['adulto', 1, -0.1], late=['adulto', 1, 0.0]))
escena('s03', 'mapa', w('Primero', mas=-0.12), **M)
escena('s04', 'foto', w('A bordo', mas=-0.12), foto='avioneta',
       conf=dict(camara=[1.0, 1.12, 0, 40], techo=True, textos=[
           dict(html='Piloto', clase='etiqueta', x=80, y=300, en=['piloto', 1, -0.05]),
           dict(html='Líder indígena', clase='etiqueta', x=80, y=390, en=['líder', 1, -0.05]),
           dict(html='Madre y sus 4 hijos', clase='etiqueta', x=80, y=480, en=['madre', 1, -0.05])]))
escena('s05', 'mapa', w('Sobre', mas=-0.12), **M)
escena('s06', 'foto', w('Los tres', mas=-0.12), foto='restos',
       conf=dict(camara=[1.0, 1.16, 0, 30], techo=True, textos=[
           dict(html='4 niños vivos', clase='sello', x=80, y=960, en=['no', 2, -0.05], modo='sello', sale=['Dos', 2, -0.2]),
           dict(html='Día 15', clase='diario', x=80, y=236, en=['semanas', 1, -0.1], modo='escribe'),
           dict(html='No están', clase='sello', x=80, y=960, en=['están', 1, -0.05], modo='sello')]))
escena('s07', 'foto', w('Solo quedan', mas=-0.12), foto='pistas',
       conf=dict(camara=[1.0, 1.14, 0, 20], techo=True, textos=[
           dict(html='· Un tetero', clase='diario', x=80, y=236, en=['tetero', 1, -0.1], modo='escribe'),
           dict(html='· Un refugio de ramas', clase='diario', x=80, y=306, en=['refugio', 1, -0.1], modo='escribe'),
           dict(html='· Una huella pequeña', clase='diario', x=80, y=376, en=['huella', 1, -0.1], modo='escribe')]))
escena('s08', 'foto', w('Empieza', mas=-0.12), foto='busqueda',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='Operación Esperanza', clase='etiqueta', x=80, y=300, en=['Operación', 1, -0.05]),
           dict(html='Soldados e indígenas', clase='etiqueta', x=80, y=390, en=['soldados', 2, -0.05])]))
escena('s09', 'foto', w('Desde', mas=-0.12), foto='helicoptero',
       conf=dict(camara=[1.0, 1.12, 0, -30], textos=[
           dict(html='La voz de su abuela', clase='etiqueta', x=80, y=300, en=['abuela', 1, -0.05]),
           dict(html='En su lengua, el huitoto', clase='etiqueta', x=80, y=390, en=['lengua', 1, -0.05])]))
escena('s10', 'foto', w('Un perro', mas=-0.12), foto='perro',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='Wilson', clase='etiqueta', x=80, y=300, en=['uílson', 1, -0.05]),
           dict(html='Se pierde', clase='sello', x=80, y=960, en=['pierde', 1, -0.05], modo='sello')]))
escena('s11', 'foto', w('Pasan', mas=-0.12), foto='selva',
       conf=dict(camara=[1.2, 1.35, 0, 60], techo=True,
                 cuenta=dict(etiqueta='DÍA', x=80, y=236, pasos=[[20, 0.1], [25, 0.55], [30, 1.0], [35, 1.45], [40, ['cuarenta', 2, -0.05]]]),
                 textos=[dict(html='Encontrados', clase='sello', x=80, y=960, en=['encuentra', 2, -0.05], modo='sello')]))
escena('s12', 'foto', w('Desnutridos', mas=-0.12), foto='hermanos',
       conf=dict(camara=[1.0, 1.12, 0, 40], techo=True, textos=[
           dict(html='Desnutridos', clase='diario', x=80, y=236, en=['Desnutridos', 1, -0.05], modo='escribe'),
           dict(html='Picaduras', clase='diario', x=80, y=306, en=['picaduras', 1, -0.1], modo='escribe'),
           dict(html='Vivos', clase='sello', x=80, y=960, en=['vivos', 2, -0.05], modo='sello'),
           dict(html='Los cuatro', clase='etiqueta', x=80, y=1090, en=['cuatro', 4, -0.05])]))
escena('s13', 'ficha', w('Quién', mas=-0.12), fondo='hermanos',
       conf=dict(FICHA, modo='revela', en=0.05, fondo_en=0.0, quita=['lésli', 1, -0.1]))
escena('s14', 'foto', w('Sacó', mas=-0.12), foto='hermanos',
       conf=dict(camara=[1.15, 1.25, -30, 60], techo=True, textos=[
           dict(html='· La fariña de la avioneta', clase='diario', x=80, y=236, en=['fariña', 1, -0.1], modo='escribe'),
           dict(html='· Frutas de la selva', clase='diario', x=80, y=306, en=['frutas', 1, -0.1], modo='escribe'),
           dict(html='Lo aprendió en su comunidad', clase='etiqueta', x=80, y=400, en=['aprendido', 1, -0.05])]))
escena('s15', 'gancho', w('Cuarenta', 3, mas=-0.12), foto='selva',
       conf=dict(GANCHO, modo='vuelta', en_cifra=['cuarenta', 3, -0.05], en_linea=['selva', 5, 0.0]))
DURACION = w('selva', 5, fin=True, mas=0.9)

# Subtítulos, salvo donde la pantalla ya escribe en grande lo que dice la voz.
sin_subtitulos(w('pero vivos', mas=-0.1), w('Quién', mas=-0.12))              # VIVOS · LOS CUATRO
sin_subtitulos(w('Lésli', mas=-0.12), w('Sacó', mas=-0.12))                    # quién los salvó, revelado en la ficha
sin_subtitulos(w('Cuarenta', 3, mas=-0.12), DURACION)                          # vuelve el gancho

# --- Música: 16–20 LU bajo la voz (CANAL.md); se retira para la ficha revelada y vuelve con la fariña.
musica('lecho', 0, DURACION, vol=0.09, fi=0.05, fo=0.1,
       puntos=[(w('Quién', mas=-0.3), 0.09), (w('Lésli', mas=-0.2), 0.055), (w('Sacó', mas=-0.1), 0.09)])

# --- Efectos: solo los fuertes, con su golpe en pantalla.
sonido('1299', w('cae', mas=0.15), vol=0.25, ini=0.1, dur=2.0, fo=0.5)                    # las ramas (el mapa tiembla)
sonido('0264', w('Desde', mas=-0.1), vol=0.08, ini=0.0, dur=3.2, fi=0.4, fo=1.2)           # el helicóptero
sonido('2954', w('perro', mas=-0.05), vol=0.12, ini=0.0, dur=0.9, fo=0.2)                 # los ladridos de Wilson
