# Corto 21 de supervivencia · «Lo imposible» (la familia de María Belón en el tsunami del 26 de diciembre de 2004, en Khao
# Lak, Tailandia). Lo monta el kit de BusinessForMen con la marca del canal:
#   python3 canales/businessformen/kit/montar.py --canal canales/supervivencia cortos/21-belon
# Vertical, unos 83 s, en bucle: el último plano («Un tsunami separó a esta familia de cinco. Y sobrevivieron los cinco»)
# es el primero (5 DE 5 · VIVOS TRAS EL TSUNAMI). El secreto tachado: adónde llegó su historia (segundo 4), que se lee
# al 88 % (la película «Lo imposible»). El mapa (mapa.py y escenas/mapa.html) sale dos veces: dónde está Khao Lak y la ola
# desde el terremoto; la familia, dibujada (escenas/familia.html), tres: juntos, separados y otra vez los cinco. María
# Belón, su marido y sus hijos son personas reales: nunca de cara. Retención: ../../../RETENCION.md.
import json
import os

M = json.load(open(os.path.join(AQUI, 'recursos', 'mapa.json')))
formato(1080, 1920, voz0=0.1, cola=0.7)
subtitulos()

FICHA = dict(cab='Años después', linea='Su historia llegó a:', tapada='El cine:<br>«Lo imposible»', tam=110)
GANCHO = dict(cifra='5', unidad='de 5', linea='Vivos tras el tsunami')
escena('s01', 'gancho', 0, foto='ola', conf=dict(GANCHO, camara=[1.1, 0, 30], modo='inicio'))
escena('s02', 'ficha', w('Años', 1, mas=-0.12), fondo='cine',
       conf=dict(FICHA, modo='oculta', en=0.05, escribe=[['historia', 1, -0.1], ['llegó', 1, 0.0, 'fin']],
                 barra=['sitio', 1, -0.05], late=['conoces', 1, -0.05]))
escena('s03', 'mapa', w('Tailandia', mas=-0.12), modo='lugar', **M)
escena('s04', 'foto', w('María Belón', mas=-0.12), foto='piscina',
       conf=dict(camara=[1.0, 1.1, 0, 20], techo=True, textos=[
           dict(html='María Belón', clase='etiqueta', x=80, y=330, en=['María', 1, -0.05]),
           dict(html='Médica', clase='etiqueta', x=80, y=420, en=['médica', 1, -0.05])]))
escena('s05', 'familia', w('Su marido', mas=-0.12), modo='juntos')
escena('s06', 'foto', w('De repente', mas=-0.12), foto='resaca',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, temblores=[['ruido', 1, 0.0]]))
escena('s07', 'mapa', w('Es el tsunami', mas=-0.12), modo='ola', **M)
escena('s08', 'foto', w('El agua arrastra', mas=-0.12), foto='arrastre',
       conf=dict(camara=[1.0, 1.14, 0, 40], techo=True, temblores=[['arrastra', 1, 0.0]]))
escena('s09', 'foto', w('Ella está', mas=-0.12), foto='arbol',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='Gravemente herida', clase='etiqueta', x=80, y=330, en=['gravemente', 1, -0.05])]))
escena('s10', 'foto', w('Unos tailandeses', mas=-0.12), foto='rescate',
       conf=dict(camara=[1.0, 1.1, 0, 20], techo=True))
escena('s11', 'familia', w('Mientras', mas=-0.12), modo='separados')
escena('s12', 'foto', w('Los manda', mas=-0.12), foto='padre',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='Quique', clase='etiqueta', x=80, y=330, en=['manda', 1, -0.05])]))
escena('s13', 'foto', w('En el hospital', 1, mas=-0.12), foto='hospital',
       conf=dict(camara=[1.0, 1.1, 0, 20], techo=True, textos=[
           dict(html='Lucas, 10 años', clase='etiqueta', x=80, y=330, en=['Lucas', 3, -0.05])]))
escena('s14', 'foto', w('A los pequeños', mas=-0.12), foto='coche',
       conf=dict(camara=[1.0, 1.1, 0, 20], techo=True))
escena('s15', 'familia', w('Y Simón se baja', mas=-0.12), modo='cinco')
escena('s16', 'foto', w('A María la trasladan', mas=-0.12), foto='avion',
       conf=dict(camara=[1.0, 1.1, 0, 20], techo=True, textos=[
           dict(html='Singapur', clase='etiqueta', x=80, y=330, en=['Singapur', 1, -0.05])]))
escena('s17', 'ficha', w('Ocho años después', mas=-0.12), fondo='cine',
       conf=dict(FICHA, modo='revela', en=0.05, fondo_en=0.0, quita=['cine', 1, -0.05]))
escena('s18', 'foto', w('Y María eligió', mas=-0.12), foto='cine',   # «Lo imposible», revelado, se queda 2,3 s en la ficha
       conf=dict(camara=[1.0, 1.1, 0, 20], techo=True, textos=[
           dict(html='Naomi Watts', clase='etiqueta', x=80, y=330, en=['actriz', 1, -0.05])]))
escena('s19', 'gancho', w('Un tsunami', 2, mas=-0.12), foto='ola',
       conf=dict(GANCHO, modo='vuelta', en_cifra=['tsunami', 3, -0.05], en_linea=['tsunami', 3, 0.1]))
DURACION = w('cinco', 6, fin=True, mas=0.9)

# Subtítulos, salvo donde la pantalla ya escribe en grande lo que dice la voz.
sin_subtitulos(w('Están', mas=-0.1), w('A María la trasladan', mas=-0.12))     # 5 DE 5 y VIVOS
sin_subtitulos(w('Ocho años después', mas=-0.1), w('Y María eligió', mas=-0.12))  # «Lo imposible», revelado en la ficha
sin_subtitulos(w('Un tsunami', 2, mas=-0.12), DURACION)                        # vuelve el gancho

# --- Música: 16–20 LU bajo la voz (CANAL.md); se retira para la revelación y vuelve con la actriz.
musica('lecho', 0, DURACION, vol=0.1, fi=0.05, fo=0.1,
       puntos=[(w('Ocho años después', mas=-0.4), 0.05), (w('Y María eligió', mas=-0.2), 0.1)])

# --- Efectos: solo los fuertes, con su golpe en pantalla (se ajustan con audio/revisar_mezcla.py).
sonido('2570', w('ruido', mas=-0.1), vol=0.12, ini=0.0, dur=3.0, fi=0.3, fo=1.0)          # el estruendo de la ola que llega (tiembla)
sonido('2570', w('arrastra', mas=-0.2), vol=0.16, ini=0.0, dur=3.5, fi=0.2, fo=1.2)        # el agua que lo arrastra todo (tiembla)
