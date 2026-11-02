# Corto 12 de supervivencia · «Apolo 13» (Jim Lovell, Jack Swigert y Fred Haise, del 11 al 17 de abril de 1970). Lo monta
# el kit de BusinessForMen con la marca del canal:
#   python3 canales/businessformen/kit/montar.py --canal canales/supervivencia cortos/12-apolo-13
# Vertical, unos 87 s, en bucle: el último plano («…a trescientos veinte mil kilómetros de casa») es el primero (320.000 KM
# · DE LA TIERRA). El secreto tachado: «lo que los salvó» (segundo 5), que se lee al 70 % («Cinta adhesiva, cartón y bolsas
# de plástico»). Dos escenas dibujadas: el viaje (escenas/trayectoria.html: la explosión a 320.000 km y la vuelta a la
# Luna, con la cifra hasta 400.171 km) y el aire (escenas/filtro.html: el CO₂ que sube, el filtro cuadrado que no entra en
# el hueco redondo y el arreglo). Los astronautas son personas reales: nunca de cara. Retención: ../../../RETENCION.md.
# Sonido (ver ../../CANAL.md, la regla desde el corto 3): solo efectos fuertes con su golpe en pantalla y sin ambientes de
# fondo: el golpe de la explosión (con su destello), la radio de Houston, el fuego de la reentrada y el agua al amerizar.
# La música, 16–20 LU bajo la voz. Medido con audio/revisar_mezcla.py antes de renderizar.
formato(1080, 1920, voz0=0.1, cola=0.7)
subtitulos()

FICHA = dict(cab='Lo que los salvó', linea='Lo tienes en casa:', tapada='Cinta, cartón<br>y bolsas')
GANCHO = dict(cifra='320.000', tam=200, unidad='km', linea='De la Tierra')
escena('s01', 'gancho', 0, foto='nave', conf=dict(GANCHO, camara=[1.1, 0, 30], modo='inicio'))
escena('s02', 'ficha', w('Lo que los salvó', mas=-0.12), fondo='nave',
       conf=dict(FICHA, modo='oculta', en=0.05, escribe=[['tienes', 1, -0.05], ['casa', 1, 0.0, 'fin']],
                 barra=['casa', 1, -0.1], late=['casa', 1, -0.05]))
escena('s03', 'foto', w('Trece', 1, mas=-0.12), foto='cabina',
       conf=dict(camara=[1.04, 1.14, 0, 40], techo=True, textos=[
           dict(html='13 ABR 1970', clase='diario', x=80, y=236, en=['Trece', 1, -0.05], modo='escribe', duracion=1.3),
           dict(html='Apolo 13 · rumbo a la Luna', clase='etiqueta', x=80, y=330, en=['Apolo', 1, -0.05]),
           dict(html='Jim Lovell', clase='etiqueta', x=80, y=420, en=['Yim', 1, -0.05]),
           dict(html='Jack Swigert', clase='etiqueta', x=80, y=510, en=['Yak', 1, -0.05]),
           dict(html='Fred Haise', clase='etiqueta', x=80, y=600, en=['Fred', 1, -0.05])]))
escena('s04', 'trayectoria', w('Dos días', 1, mas=-0.12), modo='explota')
escena('s05', 'foto', w('Jiúston', 1, mas=-0.12), foto='control',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='21:08 · Houston', clase='diario', x=80, y=236, en=0.05, modo='escribe', duracion=0.8),
           dict(html='«Houston, hemos', clase='diario', x=80, y=360, en=['Jiúston', 1, -0.05], modo='escribe', duracion=0.7),
           dict(html='tenido un problema»', clase='diario', x=80, y=430, en=['tenido', 1, -0.05], modo='escribe', duracion=0.9)]))
escena('s06', 'foto', w('La nave pierde', mas=-0.12), foto='nave',
       conf=dict(camara=[1.15, 1.3, -60, 80], techo=True, textos=[
           dict(html='Sin oxígeno · sin electricidad', clase='etiqueta', x=80, y=330, en=['electricidad', 1, -0.3]),
           dict(html='Alunizaje: cancelado', clase='etiqueta', x=80, y=420, en=['Luna', 2, -0.05]),
           dict(html='Volver', clase='sello', x=80, y=960, en=['volver', 1, -0.05], modo='sello')]))
escena('s07', 'foto', w('Se refugian', mas=-0.12), foto='modulo',
       conf=dict(camara=[1.0, 1.14, 0, 40], techo=True, textos=[
           dict(html='Módulo lunar', clase='etiqueta', x=80, y=330, en=['módulo', 1, -0.05]),
           dict(html='Su bote salvavidas', clase='etiqueta', x=80, y=420, en=['bote', 1, -0.05])]))
escena('s07b', 'puntos', w('Está hecho', mas=-0.12), fondo='modulo',
       conf=dict(n=3, cols=3, tam=150, hueco=60, x=150, y=640, cifra=dict(html='Hecho para 2<small>hombres, durante 2 días</small>', x=80, y=300),
                 aparecen=[['dos', 2, -0.05], ['tres', 2, 0.0]],
                 sello=dict(html='Casi 4 días', en=['cuatro', 1, -0.05], x=80, y=960)))
escena('s08', 'trayectoria', w('Para volver', mas=-0.12), modo='luna')
escena('s09', 'foto', w('Para ahorrar', mas=-0.12), foto='frio',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='Todo apagado', clase='etiqueta', x=80, y=330, en=['apagan', 1, -0.05]),
           dict(html='Pocos grados sobre cero', clase='etiqueta', x=80, y=420, en=['temperatura', 1, -0.05]),
           dict(html='Agua: unos 180 <i class="m">ml</i> al día', clase='etiqueta', x=80, y=510, en=['Beben', 1, -0.05])]))
escena('s10', 'filtro', w('Pero lo peor', mas=-0.12), modo='sube')
escena('s11', 'filtro', w('Hay filtros', mas=-0.12), modo='cuadrado')
escena('s12', 'foto', w('En Jiúston', mas=-0.12), foto='ingenieros',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='Ingenieros de la NASA', clase='etiqueta', x=80, y=330, en=['inventan', 1, -0.05]),
           dict(html='Por radio:', clase='diario', x=80, y=440, en=['dictan', 1, -0.05], modo='escribe', duracion=0.6),
           dict(html='paso 1… paso 2…', clase='diario', x=80, y=510, en=['radio', 1, 0.0], modo='escribe', duracion=0.9)]))
escena('s13', 'ficha', w('Cinta adhesiva', mas=-0.12), fondo='adaptador',
       conf=dict(FICHA, modo='revela', en=0.05, fondo_en=0.0, quita=['Cinta', 1, -0.05]))
escena('s14', 'filtro', w('plástico', fin=True, mas=0.15), modo='arreglo')   # usa la pausa tras la revelación
escena('s15', 'foto', w('Casi cuatro días después', mas=-0.12), foto='reentrada',
       conf=dict(camara=[1.0, 1.14, 0, -30], techo=True,
                 cuenta=dict(etiqueta='SIN RADIO · MIN', x=80, y=176,
                             pasos=[[0, ['radio', 2, -0.1]], [1, ['radio', 2, 0.3]], [2, ['radio', 2, 0.6]], [3, ['radio', 2, 0.9]],
                                    [4, ['cuatro', 4, -0.05]], [5, ['cinco', 1, -0.05]]]),
                 textos=[dict(html='17 ABR 1970', clase='diario', x=80, y=520, en=['atmósfera', 1, -0.3], modo='escribe', duracion=1.0)]))
escena('s16', 'foto', w('Y por fin', mas=-0.12), foto='paracaidas',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='Océano Pacífico', clase='etiqueta', x=80, y=330, en=['Pacífico', 1, -0.05]),
           dict(html='Vivos', clase='sello', x=80, y=960, en=['vivos', 2, -0.05], modo='sello')]))
escena('s17', 'gancho', w('Con cinta', mas=-0.12), foto='nave',
       conf=dict(GANCHO, modo='vuelta', en_cifra=['trescientos', 2, -0.05], en_linea=['veinte', 2, 0.0]))
DURACION = w('casa', 2, fin=True, mas=0.9)

# Subtítulos, salvo donde la pantalla ya escribe en grande lo que dice la voz.
sin_subtitulos(w('Jiúston', 1, mas=-0.1), w('La nave pierde', mas=-0.12))           # «HOUSTON, HEMOS TENIDO UN PROBLEMA»
sin_subtitulos(w('Cinta adhesiva', mas=-0.1), w('El aire', 2, mas=-0.12))           # lo que los salvó, revelado en la ficha
sin_subtitulos(w('Los tres', 2, mas=-0.1), w('Con cinta', mas=-0.12))               # VIVOS
sin_subtitulos(w('Con cinta', mas=-0.12), DURACION)                                   # vuelve el gancho

# --- Música: 16–20 LU bajo la voz (CANAL.md); se retira para lo que los salvó y en el silencio de radio, y vuelve al
# amerizar. Sin callarla del todo (deja huecos en las pausas de la voz).
musica('lecho', 0, DURACION, vol=0.075, fi=0.05, fo=0.1,
       puntos=[(w('Se lo dictan', mas=-0.3), 0.075), (w('Cinta adhesiva', mas=-0.2), 0.05), (w('El aire', 2, mas=-0.1), 0.075),
               (w('Lo normal', mas=-0.3), 0.075), (w('Pasan cuatro', mas=-0.2), 0.04), (w('Y por fin', mas=-0.1), 0.075)])

# --- Efectos: solo los fuertes, con su golpe en pantalla (se ajustan con audio/revisar_mezcla.py).
sonido('1023', w('explota', 2, mas=-0.08), vol=0.25, ini=0.0, dur=2.4, fo=1.0)                 # el golpe de la explosión, con el destello
sonido('2380', w('Jiúston', 1, mas=-0.45), vol=0.06, ini=0.0, dur=0.5, fo=0.1)                  # el pitido de la radio de Houston
sonido('1341', w('Casi cuatro días después', mas=-0.1), vol=0.22, ini=0.0, dur=3.0, fo=1.2)   # el fuego de la reentrada
sonido('1521', w('Caen', mas=-0.3), vol=0.14, ini=0.0, dur=1.6, fo=0.5)                        # la cápsula cae al mar
