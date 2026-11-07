# Corto 20 de supervivencia · «Fuera del avión» (el vuelo 5390 de British Airways, 10 de junio de 1990: al capitán Tim
# Lancaster se lo llevó el aire por el parabrisas, a unos 5.300 m, y la tripulación lo sujetó 22 minutos hasta aterrizar en
# Southampton). Lo monta el kit de BusinessForMen con la marca del canal:
#   python3 canales/businessformen/kit/montar.py --canal canales/supervivencia cortos/20-ba5390
# Vertical, unos 79 s, en bucle: el último plano («Salió disparado por la ventanilla de su avión, a cinco mil metros de
# altura») es el primero (5.000 METROS · FUERA DEL AVIÓN). El secreto tachado: el error de menos de un milímetro (segundo 6),
# que se lee al 84 % (84 tornillos más finos). El mapa (mapa.py y escenas/mapa.html) sale dos veces: la ruta a Málaga y el
# desvío a Southampton; el morro del avión, dibujado (escenas/cabina.html), tres: el parabrisas que sale volando, medio
# cuerpo fuera y los golpes; y el avión desde arriba (escenas/planta.html), el ala y el motor. Tim Lancaster, Nigel Ogden y
# la tripulación son personas reales: nunca de cara. Retención: ../../../RETENCION.md.
import json
import os

M = json.load(open(os.path.join(AQUI, 'recursos', 'mapa.json')))
formato(1080, 1920, voz0=0.1, cola=0.7)
subtitulos()

FICHA = dict(cab='La causa', linea='El error:', tapada='84 tornillos<br>más finos')
GANCHO = dict(cifra='5.000', unidad='metros', linea='Fuera del avión', tam=220)
escena('s01', 'gancho', 0, foto='fuera', conf=dict(GANCHO, camara=[1.1, 0, 30], modo='inicio'))
escena('s01b', 'foto', w('Y sobrevivió', mas=-0.12), foto='fuera',   # el mismo plano, más cerca: el sello
       conf=dict(camara=[1.3, 1.36, 0, 0], techo=True, textos=[
           dict(html='Sobrevivió', clase='sello', x=80, y=960, en=['sobrevivió', 1, -0.1], modo='sello')]))
escena('s02', 'ficha', w('Todo por', mas=-0.12), fondo='cabina',
       conf=dict(FICHA, modo='oculta', en=0.05, escribe=[['Todo', 1, 0.1], ['error', 1, 0.0, 'fin']],
                 barra=['menos', 1, -0.05], late=['milímetro', 1, -0.05]))
escena('s03', 'foto', w('Inglaterra', mas=-0.12), foto='despegue',
       conf=dict(camara=[1.0, 1.1, 0, 20], techo=True, textos=[
           dict(html='10 jun 1990', clase='diario', x=80, y=230, en=['diez', 1, -0.05], modo='escribe', duracion=0.7),
           dict(html='Inglaterra', clase='etiqueta', x=80, y=330, en=['Inglaterra', 1, -0.05])]))
escena('s04', 'mapa', w('Un avión de', mas=-0.12), modo='ruta', **M)
escena('s05', 'cabina', w('A los trece', mas=-0.12), modo='sale')
escena('s06', 'foto', w('Tim', mas=-0.12), foto='cabina',
       conf=dict(camara=[1.0, 1.14, 0, 30], techo=True, temblores=[['disparado', 2, 0.0]], textos=[
           dict(html='Tim Lancaster', clase='etiqueta', x=80, y=330, en=['Tim', 1, -0.05]),
           dict(html='Capitán', clase='etiqueta', x=80, y=420, en=['disparado', 2, -0.05])]))
escena('s07', 'cabina', w('Se queda', mas=-0.12), modo='rodillas')
escena('s08', 'foto', w('Fuera hay', mas=-0.12), foto='fuera',
       conf=dict(camara=[1.05, 1.18, -30, 40], techo=True, textos=[
           dict(html='−17 °C', clase='golpe', x=80, y=330, en=['diecisiete', 1, -0.05], modo='grande'),
           dict(html='+600 <i class="m">km/h</i>', clase='golpe', x=80, y=500, en=['seiscientos', 1, -0.05], modo='grande')]))
escena('s09', 'foto', w('Un auxiliar', mas=-0.12), foto='agarra',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='Auxiliar de vuelo', clase='etiqueta', x=80, y=330, en=['auxiliar', 1, -0.05]),
           dict(html='Nigel Ogden', clase='etiqueta', x=80, y=420, en=['Náiyel', 1, -0.05])]))
escena('s10', 'foto', w('El copiloto baja', mas=-0.12), foto='descenso',
       conf=dict(camara=[1.0, 1.12, 0, 60], techo=True, textos=[
           dict(html='MAYDAY', clase='diario', x=80, y=230, en=['baja', 1, -0.05], modo='escribe', duracion=0.5)]))
escena('s11', 'foto', w('Ógden se agota', mas=-0.12), foto='relevo',
       conf=dict(camara=[1.0, 1.12, 0, 20], techo=True))
escena('s12', 'cabina', w('La cabeza del', mas=-0.12), modo='golpea')
escena('s13', 'planta', w('Pero', mas=-0.12), modo='riesgo')
escena('s14', 'mapa', w('Veintidós', mas=-0.12), modo='desvio', **M)
escena('s15', 'foto', w('Y el capitán', mas=-0.12), foto='aterrizaje',
       conf=dict(camara=[1.0, 1.08, 0, 10], techo=True, textos=[
           dict(html='Vivo', clase='sello', x=80, y=960, en=['capitán', 3, 0.15], modo='sello')]))
escena('s16', 'foto', w('La causa', mas=0.0), foto='hangar',   # «VIVO» se queda 1,3 s
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='9 jun 1990', clase='diario', x=80, y=230, en=['día', 1, -0.05], modo='escribe', duracion=0.7),
           dict(html='Parabrisas nuevo', clase='etiqueta', x=80, y=330, en=['cambiado', 1, -0.05])]))
escena('s17', 'ficha', w('Y de noventa', mas=-0.12), fondo='cabina',
       conf=dict(FICHA, modo='revela', en=0.05, fondo_en=0.0, quita=['ochenta', 2, -0.05]))
escena('s18', 'foto', w('Por menos', mas=-0.12), foto='tornillos',
       conf=dict(camara=[1.0, 1.1, 0, 20], techo=True, textos=[
           dict(html='0,66 <i class="m">mm</i>', clase='golpe', x=80, y=330, en=['menos', 2, -0.05], modo='grande'),
           dict(html='Más finos', clase='etiqueta', x=80, y=500, en=['milímetro', 2, -0.1])]))
escena('s19', 'foto', w('Menos de cinco', mas=-0.12), foto='vuelve',
       conf=dict(camara=[1.0, 1.1, 0, 20], techo=True, textos=[
           dict(html='Tim Lancaster', clase='etiqueta', x=80, y=330, en=['Lánkaster', 2, -0.05]),
           dict(html='Vuelve a volar', clase='etiqueta', x=80, y=420, en=['volvía', 1, -0.05])]))
escena('s20', 'gancho', w('Salió', 2, mas=-0.12), foto='fuera',
       conf=dict(GANCHO, modo='vuelta', en_cifra=['Salió', 2, -0.05], en_linea=['Salió', 2, 0.1]))
DURACION = w('altura', 2, fin=True, mas=0.9)

# Subtítulos, salvo donde la pantalla ya escribe en grande lo que dice la voz.
sin_subtitulos(w('Y sobrevivió', mas=-0.1), w('Todo por', mas=-0.12))          # SOBREVIVIÓ
sin_subtitulos(w('Fuera hay', mas=-0.1), w('Un auxiliar', mas=-0.12))        # −17 °C y +600 km/h, en grande
sin_subtitulos(w('vivo', mas=-0.15), w('La causa', mas=0.0))                 # VIVO
sin_subtitulos(w('Y de noventa', mas=-0.1), w('Por menos', mas=-0.12))       # 84 tornillos, revelado en la ficha
sin_subtitulos(w('Por menos', mas=-0.1), w('Menos de cinco', mas=-0.12))     # 0,66 mm
sin_subtitulos(w('Salió', 2, mas=-0.12), DURACION)                           # vuelve el gancho

# --- Música: 16–20 LU bajo la voz (CANAL.md); se retira para la revelación y vuelve con los 0,66 mm.
musica('lecho', 0, DURACION, vol=0.085, fi=0.05, fo=0.1,   # a 0,1 quedaba a −14 LU de la voz al principio
       puntos=[(w('Y de noventa', mas=-0.4), 0.045), (w('Por menos', mas=-0.2), 0.085)])

# --- Efectos: solo los fuertes, con su golpe en pantalla (se ajustan con audio/revisar_mezcla.py).
sonido('0154', 0, vol=0.05, ini=0.0, dur=5.8, fo=1.2)                                     # el viento a 5.000 m (el bucle no empieza en silencio)
sonido('3008', w('despega', mas=-0.3), vol=0.3, ini=0.0, dur=3.0, fi=0.3, fo=1.2)        # el avión despega en el mapa
sonido('1023', w('volando', mas=-0.08), vol=0.25, ini=0.0, dur=1.4, fo=0.6)               # el parabrisas sale volando (tiembla)
sonido('0154', w('volando', mas=0.2), vol=0.05, ini=0.0, dur=13.0, fi=0.3, fo=1.5)       # el viento por el parabrisas
sonido('2453', w('golpea', mas=-0.05), vol=0.12, ini=0.0, dur=0.8, fo=0.3)                # la cabeza contra el avión (tiembla)
sonido('3008', w('aterrizan', mas=-0.4), vol=0.35, ini=0.0, dur=2.6, fi=0.3, fo=1.0)      # aterriza en el mapa
sonido('0154', w('Salió', 2, mas=-0.3), vol=0.05, ini=0.0, dur=DURACION - w('Salió', 2, mas=-0.3), fi=0.3)               # vuelve el viento del principio
