# Corto 13 de supervivencia · «Cinco días bajo una roca» (Aron Ralston, cañón Bluejohn, Utah, del 26 de abril al 1 de mayo
# de 2003; la película «127 horas»). Lo monta el kit de BusinessForMen con la marca del canal:
#   python3 canales/businessformen/kit/montar.py --canal canales/supervivencia cortos/13-ralston
# Vertical, unos 79 s, en bucle: el último plano («Cinco días bajo una roca») es el primero (5 DÍAS · BAJO UNA ROCA). El
# secreto tachado: «su error» (segundo 5), que se lee al 60 % («No avisó a nadie»). El cañón, en corte y dibujado
# (escenas/canon.html): la roca que cae y le atrapa la mano, los intentos y el rapel de 20 m. Aron Ralston es una persona
# real: nunca de cara. Nada de sangre ni de la amputación en imagen: la cuenta la voz. Retención: ../../../RETENCION.md.
# Sonido (ver ../../CANAL.md, la regla desde el corto 3): solo efectos fuertes con su golpe en pantalla: la roca que cae
# (tiembla), la navaja contra la piedra al picarla y al tallar su nombre, y el helicóptero. La música, 16–20 LU bajo la voz.
formato(1080, 1920, voz0=0.1, cola=0.7)
subtitulos()

FICHA = dict(cab='Su error', linea='Antes de salir:', tapada='No avisó<br>a nadie')
GANCHO = dict(cifra='5', unidad='días', linea='Bajo una roca')
escena('s01', 'gancho', 0, foto='canon', conf=dict(GANCHO, camara=[1.1, 0, 30], modo='inicio'))
escena('s02', 'ficha', w('Y todo', mas=-0.12), fondo='canon',
       conf=dict(FICHA, modo='oculta', en=0.05, escribe=[['antes', 1, -0.05], ['casa', 1, 0.0, 'fin']],
                 barra=['casa', 1, -0.1], late=['casa', 1, -0.05]))
escena('s03', 'foto', w('Veintiséis', mas=-0.12), foto='desierto',
       conf=dict(camara=[1.04, 1.16, 0, 40], techo=True, textos=[
           dict(html='26 ABR 2003', clase='diario', x=80, y=236, en=['Veintiséis', 1, -0.05], modo='escribe', duracion=1.3),
           dict(html='Utah · Estados Unidos', clase='etiqueta', x=80, y=330, en=['Utah', 1, -0.05])]))
escena('s03b', 'foto', w('Áron', mas=-0.12), foto='descenso',
       conf=dict(camara=[1.0, 1.14, 0, 60], techo=True, textos=[
           dict(html='Aron Ralston · 27 años', clase='etiqueta', x=80, y=330, en=['Áron', 1, 0.0]),
           dict(html='Solo', clase='sello', x=80, y=960, en=['solo', 1, -0.05], modo='sello')]))
escena('s04', 'canon', w('Una roca', 2, mas=-0.12), modo='cae')
escena('s05', 'foto', w('Lleva', mas=-0.12), foto='inventario',
       conf=dict(camara=[1.0, 1.14, 0, 30], techo=True, textos=[
           dict(html='Agua: 1/3 de litro', clase='diario', x=80, y=236, en=['agua', 1, -0.1], modo='escribe', duracion=0.8),
           dict(html='2 burritos', clase='diario', x=80, y=306, en=['burritos', 1, -0.1], modo='escribe', duracion=0.5),
           dict(html='1 navaja sin filo', clase='diario', x=80, y=376, en=['navaja', 1, -0.1], modo='escribe', duracion=0.7)]))
escena('s06', 'canon', w('Intenta', mas=-0.12), modo='intentos')
escena('s07', 'foto', w('Grita', mas=0.0), foto='noche',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True,
                 cuenta=dict(etiqueta='DÍA', x=80, y=176, pasos=[[2, 0.0], [3, ['Nadie', 1, -0.05]], [4, ['oye', 1, 0.15]]])))
escena('s08', 'foto', w('Día cinco', mas=-0.12), foto='botella',
       conf=dict(camara=[1.0, 1.14, 0, 20], techo=True,
                 cuenta=dict(etiqueta='DÍA', x=80, y=176, pasos=[[5, 0.0]]),
                 textos=[dict(html='Sin agua', clase='sello', x=80, y=960, en=['agua', 2, -0.05], modo='sello')]))
escena('s09', 'foto', w('Graba', mas=-0.12), foto='camara',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='Videos de despedida', clase='etiqueta', x=80, y=330, en=['despedirse', 1, -0.05])]))
escena('s10', 'foto', w('Y talla', mas=-0.12), foto='grabado',
       conf=dict(camara=[1.0, 1.12, 0, -20], techo=True, textos=[
           dict(html='ARON', clase='diario', x=80, y=236, en=['nombre', 1, -0.05], modo='escribe', duracion=0.4),
           dict(html='OCT 1975', clase='diario', x=80, y=306, en=['nacimiento', 1, -0.05], modo='escribe', duracion=0.6),
           dict(html='ABR 2003', clase='diario', x=80, y=376, en=['muerte', 1, -0.05], modo='escribe', duracion=0.6)]))
escena('s11', 'ficha', w('Nadie va', mas=-0.12), fondo='canon',
       conf=dict(FICHA, modo='revela', en=0.05, fondo_en=0.0, quita=['nadie', 3, -0.05]))
escena('s12', 'foto', w('El sexto', mas=-0.12), foto='navaja',
       conf=dict(camara=[1.0, 1.16, 0, 30], techo=True,
                 cuenta=dict(etiqueta='DÍA', x=80, y=176, pasos=[[6, 0.0]]),
                 temblores=[['huesos', 1, 0.05]],
                 textos=[dict(html='Una idea', clase='etiqueta', x=80, y=520, en=['idea', 1, -0.05]),
                         dict(html='1 hora', clase='sello', x=80, y=960, en=['hora', 1, -0.05], modo='sello')]))
escena('s13', 'canon', w('Con un solo', mas=-0.12), modo='rapel')
escena('s14', 'foto', w('Y camina', mas=-0.12), foto='caminata',
       conf=dict(camara=[1.0, 1.1, 0, 30], techo=True, textos=[
           dict(html='Pierde el 25 % de su sangre', clase='etiqueta', x=80, y=330, en=0.1)]))
escena('s15', 'foto', w('Unos', mas=-0.12), foto='helicoptero',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='4 horas después', clase='etiqueta', x=80, y=330, en=['helicóptero', 1, -0.05]),
           dict(html='Vivo', clase='sello', x=80, y=960, en=['rescata', 1, -0.05], modo='sello')]))
escena('s16', 'foto', w('Después', 2, mas=-0.12), foto='gato',
       conf=dict(camara=[1.0, 1.1, 0, 40], techo=True, textos=[
           dict(html='Para mover la roca', clase='etiqueta', x=80, y=330, en=['mover', 1, -0.05])]))
escena('s16b', 'puntos', w('trece', mas=-0.25), fondo='gato',
       conf=dict(n=13, cols=7, tam=64, hueco=30, x=120, y=640, cifra=dict(html='13 hombres<small>y un gato hidráulico</small>', x=80, y=300),
                 aparecen=[0.15, ['hombres', 1, 0.3]]))
escena('s17', 'gancho', w('Cinco días', 2, mas=-0.12), foto='canon',
       conf=dict(GANCHO, modo='vuelta', en_cifra=['cinco', 3, -0.05], en_linea=['cinco', 3, 0.1]))
DURACION = w('roca', 7, fin=True, mas=0.9)

# Subtítulos, salvo donde la pantalla ya escribe en grande lo que dice la voz.
sin_subtitulos(w('Ni un', mas=-0.1), w('Lleva', mas=-0.12))                 # NI UN CENTÍMETRO
sin_subtitulos(w('No se mueve', mas=-0.1), w('Grita', mas=0.0))           # NO SE MUEVE
sin_subtitulos(w('no le dijo', mas=-0.1), w('El sexto', mas=-0.12))         # el error, revelado en la ficha
sin_subtitulos(w('Cinco días', 2, mas=-0.12), DURACION)                      # vuelve el gancho

# --- Música: 16–20 LU bajo la voz (CANAL.md); se retira para el error revelado y vuelve con el sexto día.
musica('lecho', 0, DURACION, vol=0.08, fi=0.05, fo=0.1,
       puntos=[(w('Nadie va', mas=-0.3), 0.08), (w('no le dijo', mas=-0.2), 0.045), (w('El sexto', mas=-0.1), 0.08)])

# --- Efectos: solo los fuertes, con su golpe en pantalla (se ajustan con audio/revisar_mezcla.py).
sonido('1023', w('suelta', mas=0.38), vol=0.22, ini=0.0, dur=2.4, fo=1.0)               # la roca cae y se encaja (tiembla)
sonido('0327', w('picar', mas=-0.05), vol=0.24, ini=0.0, dur=1.4, fo=0.3)               # la navaja contra la roca
sonido('0330', w('talla', mas=0.0), vol=0.2, ini=0.0, dur=1.6, fo=0.4)                 # talla su nombre en la piedra
sonido('0264', w('helicóptero', mas=-0.6), vol=0.05, ini=0.0, dur=3.0, fi=0.4, fo=1.2)  # el helicóptero
