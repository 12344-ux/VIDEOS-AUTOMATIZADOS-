# Corto 18 de supervivencia · «Atrapados en el hielo» (la expedición del Endurance de Ernest Shackleton, 1914–1916). Lo
# monta el kit de BusinessForMen con la marca del canal:
#   python3 canales/businessformen/kit/montar.py --canal canales/supervivencia cortos/18-shackleton
# Vertical, unos 82 s, en bucle: el último plano («Veintiocho hombres atrapados en el hielo de la Antártida») es el primero
# (28 HOMBRES · ATRAPADOS EN EL HIELO). El secreto tachado: de dónde venía el barco que los salvó (segundo 7), que se lee al
# 78 % («Chile»: el Yelcho, de la Armada de Chile, al mando del piloto Luis Pardo). El mapa (mapa.py y escenas/mapa.html)
# sale cinco veces: el barco que queda atrapado, el bote hasta Georgia del Sur, la isla, los tres intentos que paró el hielo
# y la ruta del Yelcho; y el Endurance aplastado, dibujado (escenas/barco.html). Shackleton y sus hombres son personas
# reales: nunca de cara. Retención: ../../../RETENCION.md.
import json
import os

M = json.load(open(os.path.join(AQUI, 'recursos', 'mapa.json')))
formato(1080, 1920, voz0=0.1, cola=0.7)
subtitulos()

FICHA = dict(cab='El rescate', linea='El barco venía de:', tapada='Chile', tam=190)
GANCHO = dict(cifra='28', unidad='hombres', linea='Atrapados en el hielo')
escena('s01', 'gancho', 0, foto='hielo', conf=dict(GANCHO, camara=[1.1, 0, 30], modo='inicio'))
escena('s02', 'foto', w('Casi', mas=-0.12), foto='refugio',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='Casi 2 años después', clase='etiqueta', x=80, y=330, en=['Casi', 1, -0.05]),
           dict(html='Todos', clase='sello', x=80, y=960, en=['volvieron', 1, -0.05], modo='sello')]))
escena('s03', 'ficha', w('Y', 1, mas=0.0), fondo='yelcho',
       conf=dict(FICHA, modo='oculta', en=0.05, escribe=[['Y', 1, 0.1], ['salvó', 1, 0.0, 'fin']],
                 barra=['no', 1, -0.05], late=['británico', 1, -0.05]))
escena('s04', 'foto', w('Mil', 1, mas=-0.12), foto='cubierta',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='1915', clase='diario', x=80, y=230, en=['Mil', 1, -0.05], modo='escribe', duracion=0.6),
           dict(html='Ernest Shackleton', clase='etiqueta', x=80, y=330, en=['Érnest', 1, -0.05]),
           dict(html='Cruzar la Antártida a pie', clase='etiqueta', x=80, y=420, en=['quiere', 1, -0.05])]))
escena('s05', 'mapa', w('Pero', 1, mas=-0.12), modo='atrapado', **M)
escena('s06', 'barco', w('Nueve', mas=-0.12), modo='aplasta')
escena('s07', 'foto', w('Y', 2, mas=-0.12), foto='hundido',
       conf=dict(camara=[1.0, 1.1, 0, 40], techo=True, temblores=[['hunde', 1, 0.0]], textos=[
           dict(html='21 nov 1915', clase='etiqueta', x=80, y=330, en=['Y', 2, -0.05])]))
escena('s08', 'foto', w('Acampan', mas=0.1), foto='campamento',
       conf=dict(camara=[1.0, 1.14, 0, 30], techo=True, temblores=[['parte', 1, 0.0]], textos=[
           dict(html='5 meses sobre el hielo', clase='etiqueta', x=80, y=330, en=['cinco', 1, -0.05]),
           dict(html='3 botes', clase='etiqueta', x=80, y=420, en=['botes', 1, -0.05]),
           dict(html='Abril de 1916', clase='etiqueta', x=80, y=510, en=['abril', 1, -0.05])]))
escena('s09', 'foto', w('Reman', mas=-0.12), foto='botes',
       conf=dict(camara=[1.0, 1.1, 0, 20], techo=True, textos=[
           dict(html='Isla Elefante', clase='etiqueta', x=80, y=330, en=['Reman', 1, -0.05])]))
escena('s10', 'foto', w('Pisan', mas=-0.12), foto='isla',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='Por fin, tierra', clase='etiqueta', x=80, y=330, en=['Pisan', 1, -0.05]),
           dict(html='497 días', clase='golpe', x=80, y=420, en=['cuatrocientos', 1, -0.05], modo='grande')]))
escena('s11', 'mapa', w('Pero', 2, mas=-0.12), modo='caird', **M)
escena('s12', 'foto', w('Con', 2, mas=-0.12), foto='caird',
       conf=dict(camara=[1.0, 1.14, 0, 30], techo=True, temblores=[['olas', 1, 0.0], ['había', 1, 0.0]], textos=[
           dict(html='Océano Austral', clase='etiqueta', x=80, y=330, en=['olas', 1, -0.05])]))
escena('s13', 'mapa', w('Llegan', mas=-0.12), modo='georgia', **M)
escena('s14', 'foto', w('Tres', 2, mas=-0.12), foto='montanas',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True,
                 cuenta=dict(etiqueta='HORAS', x=80, y=176, pasos=[[0, 0.0], [9, ['montañas', 1, 0.0]], [18, ['pie', 2, 0.0]], [27, ['mapa', 1, 0.0]], [36, ['Treinta', 1, 0.0]]]),
                 textos=[dict(html='Sin mapa', clase='etiqueta', x=80, y=520, en=['sin', 1, -0.1])]))
escena('s15', 'foto', w('Y', 6, mas=-0.12), foto='ballenera',
       conf=dict(camara=[1.0, 1.1, 0, 20], techo=True, textos=[
           dict(html='Stromness · 20 may 1916', clase='etiqueta', x=80, y=330, en=['oyen', 1, -0.05])]))
escena('s16', 'puntos', w('Faltan', mas=-0.12), fondo='refugio',
       conf=dict(n=22, cols=6, tam=72, hueco=26, x=80, y=470, aparecen=[['veintidós', 1, -0.05], ['Elefante', 2, 0.0]],
                 cifra=dict(html='22 <small>en la isla Elefante</small>', x=80, y=220)))
escena('s17', 'mapa', w('Tres', 3, mas=-0.12), modo='intentos', **M)
escena('s18', 'foto', w('El', 11, mas=-0.12), foto='yelcho',
       conf=dict(camara=[1.0, 1.1, 0, 20], techo=True, textos=[
           dict(html='Pequeño', clase='etiqueta', x=80, y=330, en=['cuarto', 1, -0.05]),
           dict(html='Sin radio ni calefacción', clase='etiqueta', x=80, y=420, en=['sin', 2, -0.05])]))
escena('s19', 'ficha', w('Es', 2, mas=-0.12), fondo='yelcho',
       conf=dict(FICHA, modo='revela', en=0.05, fondo_en=0.0, quita=['Chile', 1, -0.05]))
escena('s20', 'mapa', w('agosto', mas=-0.3), modo='yelcho', **M)   # «Chile», la revelación, se queda 1,2 s
escena('s21', 'puntos', w('Están', mas=-0.12), fondo='refugio',
       conf=dict(n=22, cols=6, tam=72, hueco=26, x=80, y=470, aparecen=[0.0, 0.35],
                 cifra=dict(html='22 <small>30 de agosto de 1916</small>', x=80, y=220),
                 apaga=dict(en=['veintidós', 2, -0.05], menos=list(range(22))),
                 sello=dict(html='Vivos', en=['Vivos', 1, -0.1], x=80, y=1000)))
escena('s22', 'foto', w('En', 5, mas=-0.12), foto='pecio',
       conf=dict(camara=[1.0, 1.12, 0, 40], techo=True, textos=[
           dict(html='2022', clase='etiqueta', x=80, y=330, en=['dos', 2, -0.05]),
           dict(html='El Endurance', clase='etiqueta', x=80, y=420, en=['encontraron', 1, -0.05]),
           dict(html='A 3.000 <i class="m">m</i> de profundidad', clase='etiqueta', x=80, y=510, en=['tres', 4, -0.05])]))
escena('s23', 'gancho', w('Veintiocho', 2, mas=-0.12), foto='hielo',
       conf=dict(GANCHO, modo='vuelta', en_cifra=['Veintiocho', 2, -0.05], en_linea=['Veintiocho', 2, 0.1]))
DURACION = w('Antártida', 3, fin=True, mas=0.9)

# Subtítulos, salvo donde la pantalla ya escribe en grande lo que dice la voz.
sin_subtitulos(w('cuatrocientos', mas=-0.1), w('Pero', 2, mas=-0.12))  # 497 DÍAS, en grande
sin_subtitulos(w('Treinta', 1, mas=-0.1), w('Y', 6, mas=-0.12))       # el contador de horas llega a 36
sin_subtitulos(w('Es', 2, mas=-0.1), w('El', 13, mas=-0.12))          # Chile, revelado en la ficha
sin_subtitulos(w('Vivos', mas=-0.15), w('En', 5, mas=-0.12))          # VIVOS
sin_subtitulos(w('Veintiocho', 2, mas=-0.12), DURACION)               # vuelve el gancho

# --- Música: 16–20 LU bajo la voz (CANAL.md); se retira para la revelación y vuelve con la ruta del Yelcho.
musica('lecho', 0, DURACION, vol=0.1, fi=0.05, fo=0.1,
       puntos=[(w('Es', 2, mas=-0.4), 0.05), (w('El', 13, mas=-0.2), 0.1), (w('En', 5, mas=-0.3), 0.085)])

# --- Efectos: solo los fuertes, con su golpe en pantalla (se ajustan con audio/revisar_mezcla.py).
sonido('2206', w('aplasta', mas=-0.05), vol=0.15, ini=0.0, dur=2.0, fo=0.8)       # el hielo aplasta el casco (tiembla)
sonido('2206', w('parte', mas=-0.05), vol=0.12, ini=0.0, dur=1.6, fo=0.6)         # el hielo se parte bajo el campamento
sonido('2570', w('olas', mas=-0.2), vol=0.12, ini=0.0, dur=2.2, fi=0.2, fo=0.8)   # la ola contra el bote
sonido('0226', w('silbato', mas=0.1), vol=0.065, ini=0.0, dur=3.0, fi=0.1, fo=1.2)      # el silbato de vapor de Stromness
