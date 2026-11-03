# Corto 14 de supervivencia · «El verdadero Robinson Crusoe» (Alexander Selkirk, isla Más a Tierra, hoy Isla Robinson Crusoe,
# Chile, de septiembre de 1704 al 2 de febrero de 1709). Lo monta el kit de BusinessForMen con la marca del canal:
#   python3 canales/businessformen/kit/montar.py --canal canales/supervivencia cortos/14-selkirk
# Vertical, unos 87 s, en bucle: el último plano («Cuatro años solo en una isla desierta») es el primero (4 AÑOS · SOLO EN
# UNA ISLA). El secreto tachado: «por qué se quedó» (segundo 5), que se lee al 75 % («Que el barco se hundiera»: se hundió
# frente a la actual Colombia). El mapa de la costa del Pacífico, de Natural Earth (mapa.py y escenas/mapa.html): la isla a
# 670 km de Chile, el rumbo del barco hasta Malpelo y el nombre de hoy. Selkirk es una persona real: de espaldas o de lejos.
# Sonido (ver ../../CANAL.md, la regla desde el corto 3): solo efectos fuertes con su golpe en pantalla: el balido de las
# cabras, los disparos (con sus destellos) y la ola del naufragio. La música, 16–20 LU bajo la voz.
import json
import os

M = json.load(open(os.path.join(AQUI, 'recursos', 'mapa.json')))
formato(1080, 1920, voz0=0.1, cola=0.7)
subtitulos()

FICHA = dict(cab='Por qué se quedó', linea='Lo que temía:', tapada='Que el barco<br>se hundiera')
GANCHO = dict(cifra='4', unidad='años', linea='Solo en una isla')
escena('s01', 'gancho', 0, foto='isla', conf=dict(GANCHO, camara=[1.1, 0, 30], modo='inicio'))
escena('s02', 'ficha', w('Y lo más', mas=-0.12), fondo='isla',
       conf=dict(FICHA, modo='oculta', en=0.05, escribe=[['él', 1, -0.05], ['quedarse', 1, 0.0, 'fin']],
                 barra=['quedarse', 1, -0.1], late=['quedarse', 1, -0.05]))
escena('s03', 'mapa', w('Septiembre', mas=-0.12), modo='isla', **M)
escena('s04', 'foto', w('Alexander', mas=-0.12), foto='barco',
       conf=dict(camara=[1.04, 1.14, 0, 40], techo=True, temblores=[['agua', 1, -0.05]], textos=[
           dict(html='Alexander Selkirk · 28 años', clase='etiqueta', x=80, y=330, en=['Alexander', 1, -0.05]),
           dict(html='Barco corsario inglés', clase='etiqueta', x=80, y=420, en=['corsario', 1, -0.05]),
           dict(html='Hace agua', clase='sello', x=80, y=960, en=['agua', 1, -0.05], modo='sello')]))
escena('s04b', 'foto', w('Selkirk discute', mas=-0.12), foto='discusion',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, temblores=[['discute', 1, 0.1]], textos=[
           dict(html='Contra el capitán', clase='etiqueta', x=80, y=330, en=0.1)]))
escena('s05', 'mapa', w('pide', mas=-0.3), modo='distancia', **M)
escena('s06', 'foto', w('El capitán', 2, mas=-0.12), foto='abandono',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='Abandonado', clase='sello', x=80, y=960, en=['tarde', 1, -0.05], modo='sello')]))
escena('s07', 'foto', w('Le dejan', mas=-0.12), foto='inventario',
       conf=dict(camara=[1.0, 1.14, 0, 30], techo=True, textos=[
           dict(html='· 1 mosquete y pólvora', clase='diario', x=80, y=236, en=['mosquete', 1, -0.1], modo='escribe', duracion=0.8),
           dict(html='· 1 hacha, 1 cuchillo', clase='diario', x=80, y=306, en=['hacha', 1, -0.1], modo='escribe', duracion=0.8),
           dict(html='· 1 olla, 1 Biblia', clase='diario', x=80, y=376, en=['olla', 1, -0.1], modo='escribe', duracion=0.8)]))
escena('s08', 'foto', w('Por las noches', mas=-0.12), foto='gatos',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='Ratas', clase='etiqueta', x=80, y=330, en=['ratas', 1, -0.05]),
           dict(html='Gatos salvajes, domesticados', clase='etiqueta', x=80, y=420, en=['gatos', 1, -0.05])]))
escena('s09', 'foto', w('Cuando se', mas=-0.12), foto='cabras',
       conf=dict(camara=[1.0, 1.14, 0, 40], techo=True, textos=[
           dict(html='Sin pólvora', clase='etiqueta', x=80, y=330, en=['pólvora', 2, -0.05]),
           dict(html='Las caza corriendo', clase='etiqueta', x=80, y=420, en=['corriendo', 1, -0.05]),
           dict(html='Ropa de cabra', clase='etiqueta', x=80, y=510, en=['viste', 1, -0.1])]))
escena('s10', 'foto', w('Un día', mas=-0.12), foto='arbol',
       conf=dict(camara=[1.0, 1.12, 0, -30], techo=True, destellos=[['disparan', 1, 0.05], ['disparan', 1, 0.35]], textos=[
           dict(html='Barcos españoles', clase='etiqueta', x=80, y=330, en=['españoles', 1, -0.05]),
           dict(html='Enemigos', clase='sello', x=80, y=960, en=['enemigos', 1, -0.05], modo='sello', sale=['disparan', 1, -0.3])]))
escena('s11', 'foto', w('Pasan', mas=-0.12), foto='chozas',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True,
                 cuenta=dict(etiqueta='AÑOS', x=80, y=176, pasos=[[1, 0.0], [2, ['cuatro', 3, -0.1]], [3, ['cuatro', 3, 0.25]], [4, ['años', 2, 0.0]]]),
                 textos=[dict(html='+ 4 meses', clase='diario', x=80, y=520, en=['meses', 1, -0.1], modo='escribe', duracion=0.6)]))
escena('s12', 'foto', w('Hasta que', mas=-0.12), foto='rescate',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='2 FEB 1709', clase='diario', x=80, y=236, en=['febrero', 1, -0.05], modo='escribe', duracion=1.0),
           dict(html='Woodes Rogers · Duke y Duchess', clase='etiqueta', x=80, y=330, en=['llegan', 2, -0.05])]))
escena('s12b', 'foto', w('Encuentran', mas=-0.12), foto='encuentro',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='4 años y 4 meses solo', clase='etiqueta', x=80, y=330, en=['cabra', 1, -0.05]),
           dict(html='Casi no puede hablar', clase='etiqueta', x=80, y=420, en=['entiende', 1, -0.05])]))
escena('s13', 'ficha', w('Y entonces', mas=-0.12), fondo='naufragio',
       conf=dict(FICHA, modo='revela', en=0.05, fondo_en=0.0, quita=['hundió', 1, -0.05]))
escena('s14', 'mapa', w('Frente', 2, mas=-0.12), modo='hundido', **M)
escena('s15', 'foto', w('Diez', mas=-0.12), foto='libro',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='1719 · Daniel Defoe', clase='etiqueta', x=80, y=330, en=['publicó', 1, -0.05]),
           dict(html='«Robinson<br>Crusoe»', clase='golpe', x=80, y=560, en=['Robinson', 2, -0.05])]))
escena('s16', 'mapa', w('Y hoy', mas=-0.12), modo='hoy', **M)
escena('s17', 'gancho', w('Cuatro años', 3, mas=-0.12), foto='isla',
       conf=dict(GANCHO, modo='vuelta', en_cifra=['cuatro', 5, -0.05], en_linea=['cuatro', 5, 0.1]))
DURACION = w('desierta', 2, fin=True, mas=0.9)

# Subtítulos, salvo donde la pantalla ya escribe en grande lo que dice la voz.
sin_subtitulos(w('Se hundió', mas=-0.1), w('Frente', 2, mas=-0.12))          # lo que temía, revelado en la ficha
sin_subtitulos(w('Él tenía', mas=-0.1), w('Diez', mas=-0.12))                 # TENÍA RAZÓN
sin_subtitulos(w('Cuatro años', 3, mas=-0.12), DURACION)                      # vuelve el gancho

# --- Música: 16–20 LU bajo la voz (CANAL.md); se retira para lo que temía y vuelve con el libro.
musica('lecho', 0, DURACION, vol=0.105, fi=0.05, fo=0.1,
       puntos=[(w('Y entonces', mas=-0.3), 0.105), (w('Se hundió', mas=-0.2), 0.06), (w('Diez', mas=-0.1), 0.105)])

# --- Efectos: solo los fuertes, con su golpe en pantalla (se ajustan con audio/revisar_mezcla.py).
sonido('0279', w('cabras', mas=-0.1), vol=0.06, ini=0.2, dur=0.8, fo=0.25)              # el balido
sonido('2854', w('disparan', mas=0.0), vol=0.25, ini=0.0, dur=1.2, fo=0.5)              # el primer disparo (destello)
sonido('2853', w('disparan', mas=0.3), vol=0.22, ini=0.0, dur=1.2, fo=0.5)               # el segundo
sonido('2570', w('hundió', mas=-0.5), vol=0.15, ini=293.2, dur=2.6, fi=0.1, fo=1.0)     # la ola del naufragio
