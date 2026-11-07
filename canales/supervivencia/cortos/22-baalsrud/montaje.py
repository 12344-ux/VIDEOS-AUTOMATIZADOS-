# Corto 22 de supervivencia · «El duodécimo hombre» (Jan Baalsrud, el comando noruego que escapó de los nazis en el norte de
# Noruega, de marzo a junio de 1943). Lo monta el kit de BusinessForMen con la marca del canal:
#   python3 canales/businessformen/kit/montar.py --canal canales/supervivencia cortos/22-baalsrud
# Vertical, unos 78 s, en bucle: el último plano («Se cortó nueve dedos de los pies con una navaja, para no morir») es el
# primero (9 DEDOS · SE LOS CORTÓ ÉL MISMO). El secreto tachado: cómo cruzó la frontera (segundo 6), que se lee al 74 % (en
# un trineo de renos, con pastores samis). El mapa (mapa.py y escenas/mapa.html) sale dos veces: el pesquero desde las
# Shetland y la huida hasta Suecia; los doce, como puntos (comun/puntos.html), y los 27 días en la camilla, con un contador.
# Jan Baalsrud y quienes lo ayudaron son personas reales: nunca de cara. Retención: ../../../RETENCION.md.
import json
import os

M = json.load(open(os.path.join(AQUI, 'recursos', 'mapa.json')))
formato(1080, 1920, voz0=0.1, cola=0.7)
subtitulos()

FICHA = dict(cab='La frontera', linea='Lo llevaron:', tapada='En un trineo<br>de renos')
GANCHO = dict(cifra='9', unidad='dedos', linea='Se los cortó él mismo')
escena('s01', 'gancho', 0, foto='nieve', conf=dict(GANCHO, camara=[1.1, 0, 30], modo='inicio'))
escena('s01b', 'foto', w('Y aun así', mas=-0.12), foto='nieve',   # el mismo plano, más cerca: el sello
       conf=dict(camara=[1.3, 1.36, 0, -40], techo=True, textos=[
           dict(html='Escapó', clase='sello', x=80, y=960, en=['escapó', 1, -0.1], modo='sello')]))
escena('s02', 'ficha', w('Para cruzar', mas=-0.12), fondo='renos',
       conf=dict(FICHA, modo='oculta', en=0.05, escribe=[['lo', 1, -0.05], ['llevaron', 1, 0.0, 'fin']],
                 barra=['forma', 1, -0.05], late=['imaginaría', 1, -0.05]))
escena('s03', 'foto', w('Noruega', 1, mas=-0.12), foto='ocupacion',
       conf=dict(camara=[1.0, 1.1, 0, 20], techo=True, textos=[
           dict(html='Marzo 1943', clase='diario', x=80, y=230, en=['marzo', 1, -0.05], modo='escribe', duracion=0.6),
           dict(html='Noruega ocupada', clase='etiqueta', x=80, y=330, en=['ocupado', 1, -0.1])]))
escena('s04', 'mapa', w('Doce noruegos', mas=-0.12), modo='mision', **M)
escena('s05', 'foto', w('Pero alguien', mas=-0.12), foto='pesquero',
       conf=dict(camara=[1.0, 1.06, 0, 10], techo=True))
escena('s06', 'foto', w('Un barco alemán', mas=-0.12), foto='ataque',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, temblores=[['vuelan', 1, 0.0]], destellos=[['vuelan', 1, 0.0]]))
escena('s07', 'foto', w('Yan Bálsrud', mas=-0.12), foto='nado',
       conf=dict(camara=[1.0, 1.1, 0, 20], techo=True, textos=[
           dict(html='Jan Baalsrud', clase='etiqueta', x=80, y=330, en=['Yan', 1, -0.05])]))
escena('s08', 'puntos', w('De los doce', mas=-0.12), fondo='ataque',
       conf=dict(n=12, cols=6, tam=96, hueco=34, x=80, y=520, aparecen=[0.0, 0.3],
                 cifra=dict(html='12 <small>en el pesquero</small>', x=80, y=230),
                 apaga=dict(en=['solo', 1, -0.05], menos=[0], ritmo=0.06),
                 sello=dict(html='Solo él', en=['escapa', 1, -0.05], x=80, y=860)))
escena('s09', 'foto', w('Empieza', mas=-0.12), foto='caceria',
       conf=dict(camara=[1.0, 1.1, 0, 20], techo=True))
escena('s10', 'foto', w('Una avalancha', mas=-0.12), foto='avalancha',
       conf=dict(camara=[1.0, 1.14, 0, 40], techo=True, temblores=[['entierra', 1, 0.0]]))
escena('s11', 'foto', w('La nieve lo deja', mas=-0.12), foto='ventisca',
       conf=dict(camara=[1.0, 1.1, 0, 20], techo=True, textos=[
           dict(html='Ceguera de nieve', clase='etiqueta', x=80, y=330, en=['ciego', 1, -0.05]),
           dict(html='Pies congelados', clase='etiqueta', x=80, y=420, en=['congelan', 1, -0.05])]))
escena('s12', 'foto', w('Unos campesinos', mas=-0.12), foto='camilla',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True))
escena('s13', 'foto', w('Allí lo dejan', mas=-0.12), foto='muro',
       conf=dict(camara=[1.0, 1.12, 0, 20], techo=True,
                 cuenta=dict(etiqueta='DÍAS', x=80, y=176, pasos=[[0, 0.0], [9, ['dejan', 1, 0.0]], [18, ['muro', 1, 0.0]], [27, ['veintisiete', 1, 0.0]]])))
escena('s14', 'foto', w('Los pies se le', mas=-0.12), foto='navaja',
       conf=dict(camara=[1.0, 1.12, 0, 20], techo=True, textos=[
           dict(html='9 dedos', clase='golpe', x=80, y=330, en=['nueve', 2, -0.05], modo='grande')]))
escena('s15', 'ficha', w('Y cómo llegó', mas=-0.12), fondo='renos',
       conf=dict(FICHA, modo='revela', en=0.05, fondo_en=0.0, quita=['trineo', 1, -0.05]))
escena('s16', 'foto', w('con unos pastores', mas=-0.3), foto='renos',   # el trineo de renos, revelado, se queda 1,5 s en la ficha
       conf=dict(camara=[1.18, 1.26, 0, 0], origen='50% 100%', techo=True, textos=[   # más cerca y desde abajo: el trineo, sobre el subtítulo
           dict(html='Pastores samis', clase='etiqueta', x=80, y=330, en=['pastores', 1, -0.05])]))
escena('s17', 'mapa', w('Después de unos', mas=-0.12), modo='huida', **M)
escena('s18', 'foto', w('Pasa siete', mas=-0.12), foto='hospital',
       conf=dict(camara=[1.0, 1.1, 0, 20], techo=True, textos=[
           dict(html='7 meses', clase='etiqueta', x=80, y=330, en=['siete', 1, -0.05])]))
escena('s19', 'foto', w('Murió', mas=-0.12), foto='tumba',
       conf=dict(camara=[1.0, 1.1, 0, 20], techo=True, textos=[
           dict(html='1917–1988', clase='diario', x=80, y=230, en=['mil', 2, -0.05], modo='escribe', duracion=0.7),
           dict(html='Manndalen', clase='etiqueta', x=80, y=330, en=['cenizas', 1, -0.05])]))
escena('s20', 'gancho', w('Se cortó', 2, mas=-0.12), foto='nieve',
       conf=dict(GANCHO, modo='vuelta', en_cifra=['cortó', 2, -0.05], en_linea=['cortó', 2, 0.1]))
DURACION = w('morir', 2, fin=True, mas=0.9)

# Subtítulos, salvo donde la pantalla ya escribe en grande lo que dice la voz.
sin_subtitulos(w('aun así', mas=-0.1), w('Para cruzar', mas=-0.12))           # ESCAPÓ
sin_subtitulos(w('nueve', 2, mas=-0.1), w('Y cómo llegó', mas=-0.12))         # 9 DEDOS, en grande
sin_subtitulos(w('Y cómo llegó', mas=-0.1), w('con unos pastores', mas=-0.3))  # el trineo de renos, revelado en la ficha
sin_subtitulos(w('Se cortó', 2, mas=-0.12), DURACION)                         # vuelve el gancho

# --- Música: 16–20 LU bajo la voz (CANAL.md); se retira para la revelación y vuelve con los pastores.
musica('lecho', 0, DURACION, vol=0.085, fi=0.05, fo=0.1,   # a 0,1 quedaba a −14 LU de la voz al final
       puntos=[(w('Y cómo llegó', mas=-0.4), 0.045), (w('con unos pastores', mas=-0.2), 0.075), (DURACION - 0.1, 0.075)])

# --- Efectos: solo los fuertes, con su golpe en pantalla (se ajustan con audio/revisar_mezcla.py).
sonido('0154', 0, vol=0.05, ini=0.0, dur=5.6, fo=1.2)                                     # el viento de la montaña (el bucle no empieza en silencio)
sonido('1023', w('vuelan', mas=-0.05), vol=0.4, ini=0.0, dur=1.8, fo=0.8)                 # vuelan el pesquero (destello y temblor)
sonido('2570', w('avalancha', mas=-0.1), vol=0.2, ini=0.0, dur=2.6, fi=0.1, fo=1.0)      # el alud (tiembla)
sonido('0154', w('La nieve lo deja', mas=-0.3), vol=0.04, ini=0.0, dur=3.2, fi=0.3, fo=1.0)  # la ventisca
sonido('0154', w('Se cortó', 2, mas=-0.3), vol=0.05, ini=0.0, dur=DURACION - w('Se cortó', 2, mas=-0.3), fi=0.3)  # vuelve el viento del principio
