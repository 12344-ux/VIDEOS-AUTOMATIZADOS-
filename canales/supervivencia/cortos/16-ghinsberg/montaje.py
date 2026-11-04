# Corto 16 de supervivencia · «Tres semanas solo en el Amazonas» (Yossi Ghinsberg en la selva del río Tuichi, Bolivia,
# 1981; la película «Jungle»). Lo monta el kit de BusinessForMen con la marca del canal:
#   python3 canales/businessformen/kit/montar.py --canal canales/supervivencia cortos/16-ghinsberg
# Vertical, unos 80 s, en bucle: el último plano («Tres semanas solo en el Amazonas») es el primero (3 SEMANAS · SOLO EN EL
# AMAZONAS). El secreto tachado: lo que usó contra el jaguar (segundo 6), que se lee al 64 % («Un spray y un mechero», según
# su relato). El mapa de Bolivia y del río Tuichi, en esquema (mapa.py y escenas/mapa.html). Ghinsberg, Kevin Gale y los
# demás son personas reales: nunca de cara. Retención: ../../../RETENCION.md.
import json
import os

M = json.load(open(os.path.join(AQUI, 'recursos', 'mapa.json')))
formato(1080, 1920, voz0=0.1, cola=0.7)
subtitulos()

FICHA = dict(cab='Contra el jaguar', linea='Lo que usó:', tapada='Un spray<br>y un mechero')
GANCHO = dict(cifra='3', unidad='semanas', linea='Solo en el Amazonas')
escena('s01', 'gancho', 0, foto='selva', conf=dict(GANCHO, camara=[1.1, 0, 30], modo='inicio'))
escena('s02', 'foto', w('Y una noche', mas=-0.12), foto='noche',
       conf=dict(camara=[1.0, 1.16, 0, 20], techo=True, textos=[
           dict(html='Un jaguar', clase='etiqueta', x=80, y=330, en=['jaguar', 1, -0.05])]))
escena('s03', 'ficha', w('Lo que hizo', mas=-0.12), fondo='noche',
       conf=dict(FICHA, modo='oculta', en=0.05, escribe=[['hizo', 1, -0.05], ['espantarlo', 1, 0.0, 'fin']],
                 barra=['parece', 1, -0.1], late=['película', 1, -0.05]))
escena('s04', 'mapa', w('Bolivia', mas=-0.12), modo='zona', **M)
escena('s05', 'foto', w('Un guía', mas=-0.12), foto='grupo',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='3 desconocidos', clase='etiqueta', x=80, y=330, en=0.1),
           dict(html='Promete oro', clase='etiqueta', x=80, y=420, en=['oro', 1, -0.05])]))
escena('s06', 'foto', w('El grupo', mas=-0.12), foto='balsa',
       conf=dict(camara=[1.0, 1.14, 0, 40], techo=True, textos=[
           dict(html='Yossi y Kevin', clase='etiqueta', x=80, y=330, en=['Kevin', 1, -0.05]),
           dict(html='Río Tuichi', clase='etiqueta', x=80, y=420, en=['Tuichi', 1, -0.05])]))
escena('s07', 'foto', w('Kevin llega', mas=-0.12), foto='cascada',
       conf=dict(camara=[1.0, 1.16, 0, 40], techo=True, temblores=[['cascada', 1, 0.05]],
                 textos=[dict(html='Solo', clase='sello', x=80, y=960, en=['solo', 2, -0.05], modo='sello')]))
escena('s08', 'foto', w('Durante', mas=-0.12), foto='solo',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, cuenta=dict(etiqueta='DÍA', x=80, y=176, pasos=[[1, 0.0], [2, ['busca', 1, 0.0]], [3, ['arriba', 1, 0.0]], [4, ['No', 1, 0.0]]]),
                 textos=[dict(html='Busca a Kevin', clase='etiqueta', x=80, y=520, en=['busca', 1, -0.05])]))
escena('s09', 'foto', w('Come', mas=-0.12), foto='frutas',
       conf=dict(camara=[1.0, 1.14, 0, 20], techo=True, textos=[
           dict(html='Frutas silvestres', clase='etiqueta', x=80, y=330, en=['frutas', 1, -0.05])]))
escena('s10', 'foto', w('Una crecida', mas=-0.12), foto='pantano',
       conf=dict(camara=[1.0, 1.14, 0, 30], techo=True, textos=[
           dict(html='Una crecida', clase='etiqueta', x=80, y=330, en=['crecida', 1, -0.05]),
           dict(html='2 veces en un pantano', clase='etiqueta', x=80, y=420, en=['pantano', 1, -0.05]),
           dict(html='Hongos en los pies', clase='etiqueta', x=80, y=510, en=['pies', 1, -0.05])]))
escena('s11', 'foto', w('Y empieza', mas=-0.12), foto='solo',
       conf=dict(camara=[1.06, 1.0, 0, -20], techo=True, brillo=0.85, textos=[
           dict(html='Alucina', clase='etiqueta', x=80, y=330, en=['mujer', 1, -0.05])]))
escena('s12', 'foto', w('Una noche', 2, mas=-0.12), foto='noche',
       conf=dict(camara=[1.0, 1.18, 0, 0], origen='50% 55%', techo=True, textos=[
           dict(html='El jaguar', clase='etiqueta', x=80, y=330, en=['jaguar', 2, -0.05])]))
escena('s13', 'ficha', w('Enciende', mas=-0.12), fondo='fuego',
       conf=dict(FICHA, modo='revela', en=0.05, fondo_en=0.0, quita=['spray', 1, -0.05]))
escena('s14', 'foto', w('lanzallamas', mas=-0.12), foto='fuego',
       conf=dict(camara=[1.0, 1.12, 0, 20], techo=True, destellos=[['lanzallamas', 1, 0.05]],
                 textos=[dict(html='Se va', clase='sello', x=80, y=960, en=['va', 1, -0.05], modo='sello')]))
escena('s15', 'foto', w('Mientras', mas=-0.12), foto='barca',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='Kevin, a salvo', clase='etiqueta', x=80, y=330, en=['pueblo', 1, -0.05]),
           dict(html='Tico Tudela, cazador', clase='etiqueta', x=80, y=420, en=['Tico', 1, -0.05])]))
escena('s16', 'mapa', w('Al tercer', mas=-0.12), modo='busqueda', **M)
escena('s17', 'foto', w('Tres semanas después', mas=-0.12), foto='orilla',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='Vivo', clase='sello', x=80, y=960, en=0.15, modo='sello')]))
escena('s18', 'foto', w('De los otros', mas=-0.12), foto='grupo',
       conf=dict(camara=[1.08, 1.0, 0, 0], techo=True, brillo=0.6, textos=[
           dict(html='Los otros dos, nunca', clase='etiqueta', x=80, y=330, en=['nunca', 1, -0.05])]))
escena('s19', 'foto', w('Su historia', mas=-0.12), foto='balsa',
       conf=dict(camara=[1.0, 1.1, 0, 30], techo=True, textos=[
           dict(html='«Jungle» · 2017', clase='golpe', x=80, y=330, en=['película', 2, -0.05])]))
escena('s20', 'gancho', w('Tres semanas solo', mas=-0.12), foto='selva',
       conf=dict(GANCHO, modo='vuelta', en_cifra=['Tres', 4, -0.05], en_linea=['Tres', 4, 0.1]))
DURACION = w('Amazonas', 2, fin=True, mas=0.9)

# Subtítulos, salvo donde la pantalla ya escribe en grande lo que dice la voz.
sin_subtitulos(w('Enciende', mas=-0.1), w('lanzallamas', mas=-0.12))     # el spray y el mechero, revelados en la ficha
sin_subtitulos(w('Tres semanas solo', mas=-0.12), DURACION)               # vuelve el gancho

# --- Música: 16–20 LU bajo la voz (CANAL.md); se retira para el jaguar y vuelve con la búsqueda.
musica('lecho', 0, DURACION, vol=0.1, fi=0.05, fo=0.1,
       puntos=[(w('Una noche', 2, mas=-0.3), 0.1), (w('Enciende', mas=-0.2), 0.05), (w('Mientras', mas=-0.2), 0.1)])

# --- Efectos: solo los fuertes, con su golpe en pantalla (se ajustan con audio/revisar_mezcla.py).
sonido('1521', w('cascada', mas=-0.1), vol=0.11, ini=0.0, dur=2.0, fo=0.8)              # cae por la cascada
sonido('1341', w('lanzallamas', mas=-0.05), vol=0.18, ini=0.0, dur=1.8, fo=0.8)         # el lanzallamas (destello)
sonido('3132', w('río', 1, mas=-0.3), vol=0.2, ini=0.0, dur=3.0, fi=0.4, fo=1.0)          # el río
