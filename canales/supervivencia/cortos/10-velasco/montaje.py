# Corto 10 de supervivencia · «El náufrago» (Luis Alejandro Velasco, destructor Caldas, Caribe colombiano, 28 de febrero
# a marzo de 1955; el «Relato de un náufrago» de Gabriel García Márquez). Lo monta el kit de BusinessForMen con la marca
# del canal:
#   python3 canales/businessformen/kit/montar.py --canal canales/supervivencia cortos/10-velasco
# Vertical, unos 85 s, en bucle: el último plano («Diez días en una balsa, sin comer ni beber») es el primero (10 DÍAS ·
# EN UNA BALSA). El secreto tachado: «lo que pasó en el barco» (segundo 6), que se lee en el 57 («No hubo tormenta»). El
# barco, dibujado (escenas/barco.html): primero, la carga bajo las lonas y los ocho que caen; después, lo que había debajo.
# Velasco y García Márquez son personas reales: nunca de cara. Retención: ../../../RETENCION.md.
# Sonido (ver ../../CANAL.md, la regla desde el corto 3): solo efectos fuertes con su golpe en pantalla y sin ambientes de
# fondo: la ola contra el barco (tiembla), los marineros que caen al agua, el avión que pasa y la carga que cae al mar. La
# música, 16–20 LU bajo la voz. Medido con audio/revisar_mezcla.py antes de renderizar.
formato(1080, 1920, voz0=0.1, cola=0.7)
subtitulos()

FICHA = dict(cab='Lo que pasó en el barco', linea='La verdad:', tapada='No hubo<br>tormenta')
GANCHO = dict(cifra='10', tam=360, unidad='días', linea='En una balsa')
escena('s01', 'gancho', 0, foto='balsa', conf=dict(GANCHO, camara=[1.1, 0, 30], modo='inicio'))
escena('s02', 'ficha', w('Hasta que', mas=-0.12), fondo='balsa',
       conf=dict(FICHA, modo='oculta', en=0.05, escribe=[['contó', 1, -0.05], ['verdad', 1, 0.0, 'fin']],
                 barra=['verdad', 1, -0.1], late=['verdad', 1, -0.05]))
escena('s03', 'foto', w('Veintiocho', mas=-0.12), foto='destructor',
       conf=dict(camara=[1.04, 1.14, 0, 40], techo=True, textos=[
           dict(html='28 FEB 1955', clase='diario', x=80, y=236, en=['Veintiocho', 1, -0.05], modo='escribe', duracion=1.4),
           dict(html='Destructor Caldas', clase='etiqueta', x=80, y=330, en=['destructor', 1, -0.05]),
           dict(html='Armada de Colombia', clase='etiqueta', x=80, y=420, en=['Armada', 1, -0.05]),
           dict(html='Rumbo a Cartagena', clase='etiqueta', x=80, y=510, en=['Cartagena', 1, -0.05])]))
escena('s04', 'barco', w('En cubierta', 1, mas=-0.12), modo='golpe')
escena('s05', 'foto', w('Diez', 2, mas=-0.12), foto='tiburones',
       conf=dict(camara=[1.0, 1.14, 0, 30], techo=True, textos=[
           dict(html='Sin agua.', clase='diario', x=80, y=236, en=['llueve', 1, -0.1], modo='escribe'),
           dict(html='Sin comida.', clase='diario', x=80, y=306, en=['tiburones', 1, -0.1], modo='escribe')]))
escena('s06', 'foto', w('Caza', mas=-0.12), foto='gaviota', conf=dict(camara=[1.0, 1.14, 0, 20]))
escena('s07', 'foto', w('Pasan', mas=-0.12), foto='avion',
       conf=dict(camara=[1.0, 1.12, 0, -30], textos=[
           dict(html='No lo ven', clase='sello', x=80, y=960, en=['ven', 1, -0.05], modo='sello')]))
escena('s08', 'foto', w('Al décimo', mas=-0.12), foto='playa',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='Día 10', clase='diario', x=80, y=236, en=['décimo', 1, -0.05], modo='escribe')]))
escena('s09', 'foto', w('Lo condecora', mas=-0.12), foto='heroe',
       conf=dict(camara=[1.0, 1.12, 0, 40], techo=True, textos=[
           dict(html='Condecorado', clase='etiqueta', x=80, y=300, en=['condecora', 1, -0.05]),
           dict(html='Besado por reinas de belleza', clase='etiqueta', x=80, y=390, en=['besan', 1, -0.05]),
           dict(html='Rico', clase='etiqueta', x=80, y=480, en=['rico', 1, -0.05])]))
escena('s10', 'foto', w('La versión', mas=-0.12), foto='destructor',
       conf=dict(camara=[1.2, 1.3, 0, 60], techo=True, destellos=[['tormenta', 1, -0.02]], textos=[
           dict(html='Versión oficial:', clase='diario', x=80, y=236, en=['versión', 1, -0.05], modo='escribe'),
           dict(html='Tormenta', clase='sello', x=80, y=960, en=['tormenta', 1, -0.02], modo='sello')]))
escena('s11', 'foto', w('Pero un', mas=-0.12), foto='periodico',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='El Espectador, 1955', clase='diario', x=80, y=236, en=['periodista', 1, -0.1], modo='escribe'),
           dict(html='Gabriel García Márquez', clase='etiqueta', x=80, y=330, en=['Gabriel', 1, -0.05])]))
escena('s12', 'ficha', w('Y Velasco', mas=-0.12), fondo='cubierta',
       conf=dict(FICHA, modo='revela', en=0.05, fondo_en=0.0, quita=['hubo', 1, -0.25]))
escena('s13', 'barco', w('El barco venía', mas=-0.12), modo='carga')
escena('s14', 'foto', w('La dictadura', 1, mas=-0.12), foto='periodico',
       conf=dict(camara=[1.18, 1.28, 0, 50], techo=True, brillo=0.8, textos=[
           dict(html='No se retracta', clase='etiqueta', x=80, y=300, en=['retracta', 1, -0.05]),
           dict(html='Deja la Armada', clase='etiqueta', x=80, y=390, en=['Deja', 1, -0.05]),
           dict(html='Cerrado', clase='sello', x=80, y=960, en=['cierra', 1, -0.05], modo='sello')]))
escena('s15', 'foto', w('Quince', mas=-0.12), foto='libro',
       conf=dict(camara=[1.0, 1.1, 0, 30], techo=True, textos=[
           dict(html='1970 · García Márquez', clase='etiqueta', x=80, y=300, en=['libro', 1, -0.05]),
           dict(html='«Relato de<br>un náufrago»', clase='golpe', x=80, y=560, en=['relato', 1, -0.1])]))
escena('s16', 'gancho', w('Diez', 3, mas=-0.12), foto='balsa',
       conf=dict(GANCHO, modo='vuelta', en_cifra=['diez', 3, -0.05], en_linea=['balsa', 3, 0.0]))
DURACION = w('beber', 3, fin=True, mas=0.9)

# Subtítulos, salvo donde la pantalla ya escribe en grande lo que dice la voz.
sin_subtitulos(w('No lo ven', mas=-0.1), w('Al décimo', mas=-0.12))           # NO LO VEN
sin_subtitulos(w('una tormenta', mas=-0.1), w('Pero un', mas=-0.12))          # TORMENTA
sin_subtitulos(w('no hubo', mas=-0.12), w('El barco venía', mas=-0.12))       # la verdad, revelada en la ficha
sin_subtitulos(w('Relato', mas=-0.12), w('Diez', 3, mas=-0.12))               # «RELATO DE UN NÁUFRAGO»
sin_subtitulos(w('Diez', 3, mas=-0.12), DURACION)                              # vuelve el gancho

# --- Música: 16–20 LU bajo la voz (CANAL.md); se retira para la verdad revelada y vuelve con el contrabando.
musica('lecho', 0, DURACION, vol=0.09, fi=0.05, fo=0.1,
       puntos=[(w('Y Velasco', mas=-0.3), 0.09), (w('no hubo', mas=-0.2), 0.055), (w('El barco venía', mas=-0.1), 0.09)])

# --- Efectos: solo los fuertes, con su golpe en pantalla.
sonido('2570', w('golpe', mas=-0.7), vol=0.15, ini=293.2, dur=2.6, fi=0.1, fo=1.0)        # la ola contra el barco
sonido('1521', w('caen', mas=0.45), vol=0.13, ini=0.0, dur=1.6, fo=0.4)                  # los marineros, al agua
sonido('3008', w('aviones', mas=-0.6), vol=0.1, ini=1.2, dur=3.2, fi=0.4, fo=1.0)        # el avión que pasa
sonido('1519', w('soltó', mas=0.8), vol=0.15, ini=0.0, dur=1.4, fo=0.4)                  # la carga, al mar
