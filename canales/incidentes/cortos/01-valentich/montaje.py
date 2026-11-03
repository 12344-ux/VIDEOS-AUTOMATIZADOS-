# Corto 1 del canal de incidentes · «No es un avión» (la desaparición de Frederick Valentich sobre el estrecho de Bass,
# Australia, el 21 de octubre de 1978). Lo monta el kit de BusinessForMen con la marca del canal:
#   python3 canales/businessformen/kit/montar.py --canal canales/incidentes cortos/01-valentich
# Vertical, unos 78 s, en bucle: la última frase («Solo queda su última frase») empalma con la primera («No es un avión») y
# el último plano es el primero. El secreto tachado en el expediente: «lo que se oyó después» (segundo 4), que se lee al
# 64 % («Un ruido metálico»). La radio de Melbourne, dibujada (escenas/radio.html: la hora, la onda y la transcripción,
# traducida de la oficial), y el mapa del estrecho de Bass (mapa.py y escenas/mapa.html). Valentich es una persona real:
# nunca de cara. Retención: ../../../RETENCION.md; las reglas del canal, ../../CANAL.md.
import json
import os

M = json.load(open(os.path.join(AQUI, 'recursos', 'mapa.json')))
formato(1080, 1920, voz0=0.1, cola=0.7)
subtitulos()

EXPEDIENTE = dict(cab='Expediente 001 · Valentich', linea='Lo que se oyó después:', tapada='Un ruido<br>metálico')
GANCHO = dict(etiqueta='21 oct 1978 · último mensaje', frase='«No es<br>un avión»', linea='Y desapareció')
escena('s01', 'gancho', 0, foto='luces', conf=dict(GANCHO, camara=[1.08, 0, -24], modo='inicio'))
escena('s02', 'expediente', w('Y lo que', mas=-0.12), fondo='radio',
       conf=dict(EXPEDIENTE, modo='oculta', en=0.05, escribe=[['oyó', 1, -0.15], ['después', 1, 0.0, 'fin']],
                 barra=['sigue', 1, -0.05], late=['explicación', 1, -0.05]))
escena('s03', 'mapa', w('Australia', mas=-0.12), modo='ruta', **M)
escena('s04', 'foto', w('A las', 1, mas=-0.12), foto='cabina',
       conf=dict(camara=[1.0, 1.1, 0, 30], techo=True, cuenta=dict(etiqueta='HORA', x=80, y=180, pasos=[['19:06', 0.0]]),
                 textos=[dict(html='Llama a Melbourne', clase='etiqueta', x=80, y=420, en=['llama', 1, -0.05])]))
escena('s05', 'foto', w('Hay', 1, mas=-0.12), foto='luces2',
       conf=dict(camara=[1.0, 1.12, 0, 40], techo=True, textos=[
           dict(html='Un avión grande', clase='etiqueta', x=80, y=330, en=['grande', 1, -0.05]),
           dict(html='4 luces brillantes', clase='etiqueta', x=80, y=420, en=['cuatro', 1, -0.05])]))
escena('s06', 'radio', w('Le dicen', mas=-0.12),
       conf=dict(reloj=[dict(h='19:06:14', en=0)], onda=[[0, 0.15], [['dicen', 1, 0.0], 0.7], [['zona', 1, 0.0, 'fin'], 0.2]],
                 lineas=[dict(hora='19:06:14', quien='MELBOURNE', texto='«No hay tráfico conocido»', en=['dicen', 1, 0.0])]))
escena('s07', 'foto', w('Las luces', mas=-0.12), foto='pasada',
       conf=dict(camara=[1.0, 1.14, 0, 40], techo=True, temblores=[['pasan', 1, 0.05]], destellos=[['encima', 1, 0.0]], textos=[
           dict(html='Una y otra vez', clase='etiqueta', x=80, y=330, en=['otra', 1, -0.1]),
           dict(html='«Parece que está jugando conmigo»', clase='etiqueta', x=80, y=420, en=['Parece', 1, -0.05])]))
escena('s08', 'radio', w('Le preguntan', mas=-0.12),
       conf=dict(reloj=[dict(h='19:06:44', en=0), dict(h='19:09:27', en=['responde', 1, 0.1])],
                 onda=[[0, 0.15], [['preguntan', 1, 0.0], 0.6], [['responde', 1, 0.0], 0.2], [['no', 3, -0.05], 0.9]],
                 lineas=[dict(hora='19:06:44', quien='MELBOURNE', texto='«¿Qué tipo de avión es?»', en=['preguntan', 1, 0.0]),
                         dict(hora='19:09:27', quien='VH-DSJ', texto='«No es un avión»', en=['responde', 1, 0.0], grande=True)]))
escena('s09', 'foto', w('Es largo', mas=-0.12), foto='objeto',
       conf=dict(camara=[1.0, 1.14, 0, 40], techo=True, apagones=[[['Desaparece', 1, -0.05], ['vuelve', 1, -0.05]]], textos=[
           dict(html='Largo', clase='etiqueta', x=80, y=330, en=['largo', 1, -0.05]),
           dict(html='Metálico', clase='etiqueta', x=80, y=420, en=['metálico', 1, -0.05]),
           dict(html='Luz verde', clase='etiqueta', x=80, y=510, en=['verde', 1, -0.05]),
           dict(html='Encima de él', clase='sello', x=80, y=960, en=['encima', 2, -0.05], modo='sello', sale=['Desaparece', 1, -0.1])]))
escena('s10', 'foto', w('Entonces', mas=-0.12), foto='motor',
       conf=dict(camara=[1.0, 1.12, 0, 20], techo=True, temblores=[['fallar', 1, 0.0], ['fallar', 1, 0.35]],
                 cuenta=dict(etiqueta='HORA', x=80, y=180, pasos=[['19:11', 0.0]]),
                 textos=[dict(html='El motor falla', clase='etiqueta', x=80, y=420, en=['motor', 1, -0.05])]))
escena('s11', 'radio', w('A las', 2, mas=-0.12),
       conf=dict(reloj=[dict(h='19:12:28', en=0)], onda=[[0, 0.15], [['llama', 2, 0.0], 0.7], [['vez', 2, 0.0, 'fin'], 0.2]],
                 lineas=[dict(hora='19:12:28', quien='VH-DSJ', texto='«Delta Sierra Juliet… Melbourne…»', en=['llama', 2, 0.0])],
                 abierto=dict(en=['diecisiete', 1, -0.1], hasta=['abierto', 1, 1.25, 'fin'], segundos=17, desde=28)))
escena('s12', 'expediente', w('Un ruido', mas=-0.12), fondo='radio',
       conf=dict(EXPEDIENTE, modo='revela', en=0.05, fondo_en=0.0, quita=['ruido', 1, -0.05]))
escena('s13', 'radio', w('Y silencio', mas=-0.12), conf=dict(reloj=[dict(h='19:12:45', en=0)], onda=[[0, 0.0]], silencio=dict(en=0.0)))
escena('s14', 'foto', w('Lo buscan', mas=-0.12), foto='busqueda',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True,
                 cuenta=dict(etiqueta='DÍAS', x=80, y=180, pasos=[[1, 0.0], [2, ['buscan', 1, 0.25]], [3, ['cuatro', 2, -0.1]], [4, ['días', 1, -0.05]]]),
                 textos=[dict(html='Nada', clase='sello', x=80, y=960, en=['nada', 1, -0.05], modo='sello')]))
escena('s15', 'mapa', w('Cinco', mas=-0.12), modo='pieza', **M)
escena('s16', 'foto', w('Nunca', mas=-0.12), foto='pieza',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='Isla Flinders · 1983', clase='etiqueta', x=80, y=330, en=0.1),
           dict(html='¿Era la suya?', clase='golpe', x=80, y=520, en=['demostró', 1, -0.05])]))
escena('s17', 'expediente', w('El informe', mas=-0.12), fondo='busqueda',
       conf=dict(cab='Informe oficial · 1982', linea='Causa de la desaparición:', sello='No determinada', modo='informe', en=0.05,
                 fondo_en=0.0, escribe=[['informe', 1, 0.0], ['dice', 2, 0.0, 'fin']], en_sello=['no', 5, -0.05]))
escena('s18', 'foto', w('Era un', mas=-0.12), foto='cuarto',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='Apasionado de los ovnis', clase='etiqueta', x=80, y=330, en=['apasionado', 1, -0.05])]))
escena('s19', 'foto', w('Se desorientó', mas=-0.12), foto='mar',
       conf=dict(camara=[1.0, 1.1, 0, 30], techo=True, textos=[
           dict(html='1 · ¿Se desorientó?', clase='etiqueta', x=80, y=330, en=['desorientó', 1, -0.1]),
           dict(html='2 · ¿Lo fingió todo?', clase='etiqueta', x=80, y=420, en=['fingió', 1, -0.1]),
           dict(html='3 · ¿Vio algo de verdad?', clase='etiqueta', x=80, y=510, en=['vio', 1, -0.1]),
           dict(html='Nadie lo sabe', clase='sello', x=80, y=960, en=['Nadie', 2, -0.05], modo='sello')]))
escena('s20', 'gancho', w('Solo queda', mas=-0.12), foto='luces',
       conf=dict(GANCHO, modo='vuelta', en_etiqueta=0.1, en_frase=['Solo', 2, 0.0], en_linea=['queda', 1, 0.0]))
DURACION = w('frase', fin=True, mas=0.9)

# Subtítulos, salvo donde la pantalla ya escribe en grande lo que dice la voz.
sin_subtitulos(0, w('Fue', mas=-0.12))                                  # el gancho: «NO ES UN AVIÓN»
sin_subtitulos(w('Parece', mas=-0.1), w('Le preguntan', mas=-0.12))      # «PARECE QUE ESTÁ JUGANDO CONMIGO»
sin_subtitulos(w('Le preguntan', mas=-0.12), w('Es largo', mas=-0.12))   # la radio: «¿QUÉ TIPO DE AVIÓN ES?» «NO ES UN AVIÓN»
sin_subtitulos(w('Un ruido', mas=-0.12), w('Lo buscan', mas=-0.12))      # el expediente revelado y SIN SEÑAL
sin_subtitulos(w('El informe', mas=-0.12), w('Era un', mas=-0.12))        # INFORME OFICIAL · NO DETERMINADA
sin_subtitulos(w('Se desorientó', mas=-0.12), DURACION)                  # las tres preguntas y vuelve el gancho

# --- Música: 16–20 LU bajo la voz (CANAL.md); se retira para el ruido y el silencio y vuelve con la búsqueda.
musica('lecho', 0, DURACION, vol=0.135, fi=0.05, fo=0.1,
       puntos=[(w('Después', 2, mas=-0.3), 0.135), (w('Un ruido', mas=-0.2), 0.05), (w('Lo buscan', mas=-0.3), 0.135)])

# --- Efectos (BigSoundBank, CC0): la radio que se abre, las luces que pasan por encima y, en la pausa tras «micrófono
# abierto», la interferencia y un roce metálico (evocan el ruido; no es la grabación). Se ajustan con revisar_mezcla.py.
sonido('0313', w('Le dicen', mas=-0.25), vol=0.19, ini=0.0, dur=1.1, fo=0.4)                       # la radio se abre
sonido('3006', w('pasan', mas=-1.6), vol=0.24, ini=0.0, dur=5.5, fi=0.4, fo=1.6)                   # las luces pasan por encima
T_PAUSA = w('abierto', fin=True)
sonido('0310', w('diecisiete', mas=-0.1), vol=0.05, ini=1.5, dur=T_PAUSA + 1.35 - w('diecisiete', mas=-0.1), fi=0.3, fo=0.05,
       puntos=[(T_PAUSA + 0.05, 0.05), (T_PAUSA + 0.35, 0.55), (T_PAUSA + 1.2, 0.55), (T_PAUSA + 1.3, 0.0)])  # el micrófono abierto
sonido('0303', T_PAUSA + 0.45, vol=0.25, ini=0.0, dur=0.85, fo=0.25)                                # el roce metálico
