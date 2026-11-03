# Corto 2 del canal de incidentes · «El ovni Tic Tac» (el encuentro de los cazas del portaaviones Nimitz con un objeto
# blanco frente a California, el 14 de noviembre de 2004). Lo monta el kit de BusinessForMen con la marca del canal:
#   python3 canales/businessformen/kit/montar.py --canal canales/incidentes cortos/02-tictac
# Vertical, unos 86 s, en bucle: la última frase («Solo queda lo que vieron cuatro aviadores») empalma con la primera
# («Desapareció delante de nosotros») y el último plano es el primero. El secreto tachado en el expediente: «lo que marcó el
# radar» (segundo 6), que se lee al 67 % («A 97 km en un minuto»). Dibujados: el mapa frente a California (mapa.py y
# escenas/mapa.html), el radar del crucero (radar.html), el encuentro visto desde arriba (encuentro.html) y la cámara
# térmica (flir.html), todos recreaciones. La fuente principal es la declaración escrita de David Fravor ante el Congreso
# (2023). Fravor, Dietrich y los demás aviadores son personas reales: nunca de cara. Las reglas: ../../CANAL.md.
import json
import os

M = json.load(open(os.path.join(AQUI, 'recursos', 'mapa.json')))
formato(1080, 1920, voz0=0.1, cola=0.7)
subtitulos()

EXPEDIENTE = dict(cab='Expediente 002 · Nimitz', linea='Lo que marcó el radar:', tapada='A 97 km,<br>en un minuto')
GANCHO = dict(etiqueta='14 nov 2004 · Marina de EE. UU.', frase='«Desapareció<br>delante de<br>nosotros»', tam=170,
              linea='Y nadie sabe qué era')
escena('s01', 'gancho', 0, foto='tictac', conf=dict(GANCHO, camara=[1.08, 0, -24], modo='inicio', velo_en=['dijo', 1, -0.4]))
escena('s02', 'expediente', w('Y lo que', mas=-0.12), fondo='radar',
       conf=dict(EXPEDIENTE, modo='oculta', en=0.05, escribe=[['marcó', 1, -0.15], ['radar', 1, 0.0, 'fin']],
                 barra=['sigue', 1, -0.05], late=['explicación', 1, -0.05]))
escena('s03', 'mapa', w('Océano', mas=-0.12), modo='zona', **M)
escena('s04', 'foto', w('El radar', 2, mas=-0.12), foto='flota',
       conf=dict(camara=[1.0, 1.1, 0, 30], techo=True,
                 cuenta=dict(etiqueta='DÍAS', x=80, y=180, pasos=[[1, 0.0], [7, ['dos', 2, 0.0]], [14, ['semanas', 1, 0.0]]]),
                 textos=[dict(html='Crucero Princeton · radar', clase='etiqueta', x=80, y=420, en=['crucero', 1, -0.05]),
                         dict(html='Algo raro', clase='sello', x=80, y=960, en=['raro', 1, -0.05], modo='sello')]))
escena('s05', 'radar', w('Objetos', mas=-0.12))
escena('s06', 'foto', w('El catorce', mas=-0.12), foto='cazas',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='14 NOV 2004', clase='diario', x=80, y=236, en=['catorce', 1, -0.05], modo='escribe', duracion=0.9),
           dict(html='2 cazas · 4 tripulantes', clase='etiqueta', x=80, y=330, en=['cazas', 1, -0.05]),
           dict(html='Cielo despejado · mar en calma', clase='etiqueta', x=80, y=420, en=['Cielo', 1, -0.05])]))
escena('s07', 'foto', w('Y sobre', mas=-0.12), foto='mancha',
       conf=dict(camara=[1.0, 1.16, 0, 0], origen='50% 50%', techo=True, textos=[
           dict(html='Una mancha blanca', clase='etiqueta', x=80, y=330, en=['mancha', 1, -0.05])]))
escena('s08', 'foto', w('Encima', mas=-0.12), foto='tictac',
       conf=dict(camara=[1.0, 1.18, 0, 40], techo=True, textos=[
           dict(html='Forma de Tic Tac', clase='etiqueta', x=80, y=330, en=['Tic', 1, -0.05]),
           dict(html='Unos 12 <i class="m">m</i>', clase='etiqueta', x=80, y=420, en=['doce', 1, -0.05]),
           dict(html='Sin alas', clase='etiqueta', x=80, y=510, en=['alas', 1, -0.05]),
           dict(html='Sin rotores', clase='etiqueta', x=80, y=600, en=['rotores', 1, -0.05])]))
escena('s09', 'foto', w('El comandante', mas=-0.12), foto='picado',
       conf=dict(camara=[1.0, 1.14, 0, 40], techo=True, textos=[
           dict(html='Cmdte. David Fravor', clase='etiqueta', x=80, y=330, en=['David', 1, -0.05])]))
escena('s10', 'encuentro', w('Y el objeto', mas=-0.12))
escena('s11', 'foto', w('También', mas=-0.12), foto='calma',
       conf=dict(camara=[1.0, 1.1, 0, 0], origen='50% 50%', techo=True, textos=[
           dict(html='Ni rastro en el agua', clase='etiqueta', x=80, y=330, en=0.1)]))
escena('s12', 'mapa', w('Vuelven', 2, mas=-0.12), modo='salto', **M)
escena('s13', 'expediente', w('encontrar', fin=True, mas=0.15), fondo='radar',
       conf=dict(EXPEDIENTE, modo='revela', en=0.05, fondo_en=0.0, quita=['Allí', 1, -0.05]))
escena('s14', 'flir', w('Otro', mas=-0.12))
escena('s15', 'foto', w('En dos mil veinte', mas=-0.12), foto='pentagono',
       conf=dict(camara=[1.0, 1.1, 0, 30], techo=True, textos=[
           dict(html='27 ABR 2020', clase='diario', x=80, y=236, en=['veinte', 1, -0.05], modo='escribe', duracion=0.9),
           dict(html='Publica el vídeo', clase='etiqueta', x=80, y=330, en=['publica', 1, -0.05]),
           dict(html='No identificado', clase='sello', x=80, y=960, en=['identificado', 1, -0.05], modo='sello')]))
escena('s16', 'foto', w('En dos mil veintitrés', mas=-0.12), foto='congreso',
       conf=dict(camara=[1.0, 1.1, 0, 30], techo=True, textos=[
           dict(html='26 JUL 2023', clase='diario', x=80, y=236, en=['veintitrés', 1, -0.05], modo='escribe', duracion=0.9),
           dict(html='Bajo juramento', clase='etiqueta', x=80, y=330, en=['juramento', 1, -0.05]),
           dict(html='«Muy superior a todo<br>lo que teníamos»', clase='etiqueta', x=80, y=440, en=['Era', 1, -0.05])]))
escena('s17', 'foto', w('Un fallo', mas=-0.12), foto='horizonte',
       conf=dict(camara=[1.0, 1.1, 0, 30], techo=True, textos=[
           dict(html='1 · ¿Fallo de los sensores?', clase='etiqueta', x=80, y=330, en=['fallo', 1, -0.1]),
           dict(html='2 · ¿Tecnología secreta?', clase='etiqueta', x=80, y=420, en=['Tecnología', 1, -0.1]),
           dict(html='3 · ¿O algo más?', clase='etiqueta', x=80, y=510, en=['algo', 3, -0.1]),
           dict(html='Nadie lo sabe', clase='sello', x=80, y=960, en=['Nadie', 1, -0.05], modo='sello')]))
escena('s18', 'gancho', w('Solo queda', mas=-0.12), foto='tictac',
       conf=dict(GANCHO, modo='vuelta', en_etiqueta=0.1, en_frase=['Solo', 1, 0.0], en_linea=['queda', 1, 0.0]))
DURACION = w('aviadores', fin=True, mas=0.9)

# Subtítulos, salvo donde la pantalla ya escribe en grande lo que dice la voz.
sin_subtitulos(0, w('Lo dijo', mas=-0.12))                                  # el gancho
sin_subtitulos(w('Allí', mas=-0.1), w('Otro', mas=-0.12))                    # el expediente revelado
sin_subtitulos(w('Era', mas=-0.1), w('Un fallo', mas=-0.12))                 # «MUY SUPERIOR A TODO LO QUE TENÍAMOS»
sin_subtitulos(w('Un fallo', mas=-0.12), DURACION)                           # las tres preguntas y vuelve el gancho

# --- Música: 16–20 LU bajo la voz (CANAL.md); se retira para la revelación y vuelve con la cámara térmica.
musica('lecho', 0, DURACION, vol=0.11, fi=0.05, fo=0.1,
       puntos=[(w('Y el radar', mas=-0.3), 0.11), (w('encontrar', fin=True, mas=0.05), 0.045), (w('Otro', mas=-0.3), 0.11)])

# --- Efectos (BigSoundBank, CC0): el sonar del radar cuando caen los objetos y cuando el radar lo vuelve a encontrar, los
# cazas que pasan y el rugido cuando el objeto se va. Se ajustan con audio/revisar_mezcla.py.
sonido('1920', w('caen', mas=-0.1), vol=0.12, ini=0.0, dur=2.4, fo=1.2)                     # el radar
sonido('3004', w('cazas', mas=-1.4), vol=0.2, ini=0.0, dur=5.0, fi=0.4, fo=1.5)            # los dos cazas
sonido('3006', w('acelera', mas=-0.25), vol=0.22, ini=2.6, dur=1.6, fi=0.05, fo=0.9)       # el objeto sale disparado
sonido('1920', w('radar', 3, mas=-0.05), vol=0.12, ini=0.0, dur=2.4, fo=1.2)                # el radar lo vuelve a ver
