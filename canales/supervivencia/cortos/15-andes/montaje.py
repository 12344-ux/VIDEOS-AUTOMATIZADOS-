# Corto 15 de supervivencia · «72 días en los Andes» (el vuelo 571 de la Fuerza Aérea Uruguaya, 13 de octubre – 23 de
# diciembre de 1972). Lo monta el kit de BusinessForMen con la marca del canal:
#   python3 canales/businessformen/kit/montar.py --canal canales/supervivencia cortos/15-andes
# Vertical, unos 80 s, en bucle: el último plano («Setenta y dos días en la nieve de los Andes») es el primero (72 DÍAS · EN
# LOS ANDES). El secreto tachado: lo que decía el papel (segundo 5), que se lee al 80 % («Vengo de un avión…»). Los 45 a
# bordo como puntos, que al final se apagan hasta quedar 16; el mapa del vuelo y de la caminata (mapa.py y escenas/mapa.html).
# Los supervivientes y las víctimas son personas reales: nunca de cara, y nada de cuerpos ni de lo que tuvieron que comer
# (lo dice la voz, con respeto). Retención: ../../../RETENCION.md.
import json
import os

M = json.load(open(os.path.join(AQUI, 'recursos', 'mapa.json')))
formato(1080, 1920, voz0=0.1, cola=0.7)
subtitulos()

FICHA = dict(cab='El papel', linea='Lo que escribió:', tapada='«Vengo de<br>un avión…»')
GANCHO = dict(cifra='72', unidad='días', linea='En los Andes')
VIVOS = [1, 4, 6, 9, 12, 15, 19, 21, 24, 27, 30, 33, 36, 38, 41, 44]   # 16 de 45, repartidos
escena('s01', 'gancho', 0, foto='nieve', conf=dict(GANCHO, camara=[1.1, 0, 30], modo='inicio'))
escena('s02', 'ficha', w('Los salvó', mas=-0.12), fondo='nota',
       conf=dict(FICHA, modo='oculta', en=0.05, escribe=[['salvó', 1, -0.05], ['piedra', 1, 0.0, 'fin']],
                 barra=['papel', 1, -0.1], late=['piedra', 1, -0.05]))
escena('s03', 'mapa', w('Trece', mas=-0.12), modo='ruta', **M)
escena('s04', 'puntos', w('Lleva', mas=-0.12), fondo='equipo',
       conf=dict(n=45, cols=9, tam=58, hueco=26, x=94, y=560, cifra=dict(html='45 a bordo<small>Un equipo de rugby, amigos y familiares</small>', x=80, y=300),
                 aparecen=[['cuarenta', 1, -0.1], ['rugby', 1, 0.0]]))
escena('s05', 'foto', w('Entre', mas=-0.12), foto='vuelo',
       conf=dict(camara=[1.0, 1.14, 0, 30], techo=True, temblores=[['choca', 1, 0.05]]))
escena('s06', 'foto', w('pierde', mas=-0.12), foto='choque',
       conf=dict(camara=[1.0, 1.14, 0, 40], techo=True, temblores=[['pierde', 1, 0.1]], textos=[
           dict(html='Sin alas', clase='etiqueta', x=80, y=330, en=['alas', 1, -0.05]),
           dict(html='Mueren 12', clase='etiqueta', x=80, y=420, en=['doce', 1, -0.05])]))
escena('s07', 'foto', w('Los demás', 1, mas=-0.12), foto='nieve',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='3.600 <i class="m">m</i> de altura', clase='etiqueta', x=80, y=330, en=['seiscientos', 1, -0.05]),
           dict(html='Sin abrigo', clase='etiqueta', x=80, y=420, en=['abrigo', 1, -0.05]),
           dict(html='−30 °C', clase='golpe', x=80, y=560, en=['treinta', 1, -0.05])]))
escena('s08', 'foto', w('El día once', mas=-0.12), foto='radio',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, cuenta=dict(etiqueta='DÍA', x=80, y=176, pasos=[[11, 0.0]]),
                 textos=[dict(html='Ya no los buscan', clase='sello', x=80, y=960, en=['radio', 1, 0.1], modo='sello')]))
escena('s09', 'foto', w('Sin comida', mas=-0.12), foto='noche',
       conf=dict(camara=[1.0, 1.1, 0, 30], techo=True, textos=[
           dict(html='Un pacto', clase='etiqueta', x=80, y=330, en=['pacto', 1, -0.05]),
           dict(html='La decisión más difícil', clase='etiqueta', x=80, y=420, en=['decisión', 1, -0.05])]))
escena('s10', 'foto', w('El día diecisiete', mas=-0.12), foto='alud',
       conf=dict(camara=[1.0, 1.14, 0, 30], techo=True, temblores=[['alud', 1, 0.1], ['alud', 1, 0.5]],
                 cuenta=dict(etiqueta='DÍA', x=80, y=176, pasos=[[17, 0.0]]),
                 textos=[dict(html='Mueren 8 más', clase='etiqueta', x=80, y=520, en=['Mueren', 2, -0.05])]))
escena('s11', 'foto', w('En diciembre', mas=-0.12), foto='caminata',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='Nando Parrado · Roberto Canessa', clase='etiqueta', x=80, y=330, en=['Nando', 1, -0.05])]))
escena('s12', 'mapa', w('Caminan', mas=-0.12), modo='caminata', **M)
escena('s13', 'foto', w('Al otro lado', mas=-0.12), foto='rio',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='Sergio Catalán, arriero', clase='etiqueta', x=80, y=330, en=['arriero', 1, -0.05]),
           dict(html='El río no deja oír', clase='etiqueta', x=80, y=420, en=['ruido', 1, -0.05])]))
escena('s14', 'foto', w('Él les lanza', mas=-0.12), foto='nota',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='Un papel y un lápiz', clase='etiqueta', x=80, y=330, en=['papel', 2, -0.05])]))
escena('s15', 'ficha', w('Y Parrado', mas=-0.12), fondo='nota',
       conf=dict(FICHA, modo='revela', en=0.05, fondo_en=0.0, quita=['Vengo', 1, -0.05]))
escena('s16', 'foto', w('Al día siguiente', mas=-0.12), foto='helicoptero',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='22 DIC 1972', clase='diario', x=80, y=236, en=['helicópteros', 1, -0.3], modo='escribe', duracion=0.9),
           dict(html='Rescatan a 14', clase='etiqueta', x=80, y=330, en=['catorce', 1, -0.05])]))
escena('s17', 'puntos', w('Dieciséis de', mas=-0.12), fondo='equipo',
       conf=dict(n=45, cols=9, tam=58, hueco=26, x=94, y=560, cifra=dict(html='16 de 45<small>volvieron a casa</small>', x=80, y=300),
                 aparecen=[0.0, 0.25], apaga=dict(en=0.3, menos=VIVOS)))
escena('s18', 'gancho', w('Setenta y dos días', 2, mas=-0.12), foto='nieve',
       conf=dict(GANCHO, modo='vuelta', en_cifra=['Setenta', 3, -0.05], en_linea=['Setenta', 3, 0.1]))   # la 2.ª, «mil novecientos setenta»
DURACION = w('Andes', 2, fin=True, mas=0.9)

# Subtítulos, salvo donde la pantalla ya escribe en grande lo que dice la voz.
sin_subtitulos(w('Y Parrado', mas=-0.1), w('Al día siguiente', mas=-0.12))   # el papel, revelado en la ficha
sin_subtitulos(w('Dieciséis de', mas=-0.12), DURACION)                        # 16 DE 45 y vuelve el gancho

# --- Música: 16–20 LU bajo la voz (CANAL.md); se retira para el papel y vuelve con los helicópteros.
musica('lecho', 0, DURACION, vol=0.1, fi=0.05, fo=0.1,
       puntos=[(w('Él les lanza', mas=-0.3), 0.1), (w('Y Parrado', mas=-0.2), 0.05), (w('Al día siguiente', mas=-0.1), 0.1)])

# --- Efectos: solo los fuertes, con su golpe en pantalla (se ajustan con audio/revisar_mezcla.py).
sonido('1023', w('choca', mas=-0.05), vol=0.3, ini=0.0, dur=2.4, fo=1.0)               # el choque (tiembla)
sonido('2570', w('alud', mas=-0.3), vol=0.15, ini=293.2, dur=2.6, fi=0.1, fo=1.0)       # el alud
sonido('3132', w('Al otro lado', mas=-0.2), vol=0.15, ini=0.0, dur=4.0, fi=0.4, fo=1.0) # el río
sonido('0264', w('helicópteros', mas=-0.6), vol=0.07, ini=0.0, dur=3.0, fi=0.4, fo=1.2) # los helicópteros
