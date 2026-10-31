# Corto 3 de supervivencia · «438 días a la deriva» (José Salvador Alvarenga, de México a las islas Marshall,
# 2012–2014). Lo monta el kit de BusinessForMen con la marca del canal:
#   python3 canales/businessformen/kit/montar.py --canal canales/supervivencia cortos/03-alvarenga
# Vertical, unos 67 s, en bucle: el último plano («Cuatrocientos treinta y ocho días. Todo, por salir a pescar») es el
# primero (438 DÍAS · A LA DERIVA). El secreto tachado: «muchos no le creyeron» (segundo 11), que se lee en el 62 («su
# historia encaja»). La deriva y la simulación, en esquema. Retención: ../../../RETENCION.md.
# Sonido (ver ../../CANAL.md): el agua contra la barca de fondo, la tormenta, la lluvia, el viento de la noche y la
# rompiente del arrecife; ningún sonido de interfaz. Medido con audio/revisar_mezcla.py antes de renderizar.
import json
import os

formato(1080, 1920, voz0=0.1, cola=0.7)
subtitulos()
M = json.load(open(os.path.join(AQUI, 'recursos', 'mapa.json')))
C, P = M['cerca'], M['pacifico']
# El mapa lleva todos sus parámetros en todos los modos (la plantilla los usa en el código de cada uno).
VACIO = dict(tierra='', marshall='', rejilla='', deriva='M0,0', trazas=[], chiapas=[0, 0], ebon=[0, 0], km=0)
PAC = dict(tierra=P['tierra'], marshall=P['marshall'], rejilla=P['rejilla'], deriva=P['deriva'], trazas=P['trazas'],
           chiapas=P['chiapas'], ebon=P['ebon'], km=P['km'], tierra_c='', salvador='', salida='M0,0', chiapas_c=[0, 0], salvador_c=[0, 0])
CER = dict(VACIO, tierra_c=C['tierra'], salvador=C['salvador'], salida=C['salida'], chiapas_c=C['chiapas'], salvador_c=C['salvador_c'])

FICHA = dict(cab='¿Mentía?', linea='Lo que dijo la ciencia:', tapada='Su historia<br>encaja')
escena('s01', 'gancho', 0, foto='barca', conf=dict(cifra='438', unidad='días', linea='A la deriva', camara=[1.1, 0, 30], modo='inicio'))
escena('s02', 'mapa', w('Al otro', mas=-0.12), modo='pacifico', **PAC)
escena('s03', 'ficha', w('Y cuando', mas=-0.12), fondo='barca',
       conf=dict(FICHA, modo='oculta', en=['contó', 1, -0.3], escribe=[['contó', 1, 0.0], ['hecho', 1, 0.0, 'fin']],
                 barra=['creyeron', 1, 0.05, 'fin'], late=['creyeron', 1, 0.2, 'fin']))
escena('s04', 'mapa', w('Noviembre', mas=-0.12), modo='cerca', **CER)
escena('s05', 'foto', w('Una tormenta', mas=-0.12), foto='tormenta',
       conf=dict(camara=[1.05, 1.16, 0, 20], lluvia=True, destellos=[['tormenta', 1, 0.1], ['rompe', 1, 0.0]], temblores=[['rompe', 1, 0.05]],
                 textos=[dict(html='Sin motor', clase='sello', x=80, y=960, en=['rompe', 1, 0.0], modo='sello')]))
escena('s06', 'mapa', w('Sin motor', mas=-0.12), modo='deriva', **PAC)
escena('s07', 'foto', w('No tienen', mas=-0.12), foto='barca',
       conf=dict(camara=[1.25, 1.32, 0, 0], brillo=0.6, textos=[
           dict(html='Comida: 0', clase='diario', x=80, y=300, en=['comida', 1, -0.1], modo='escribe'),
           dict(html='Agua: 0', clase='diario', x=80, y=380, en=['agua', 1, -0.1], modo='escribe')]))
escena('s08', 'foto', w('José pesca', mas=-0.12), foto='pesca',
       conf=dict(camara=[1.0, 1.1, 0, 0], textos=[dict(html='Con las manos', clase='etiqueta', x=80, y=300, en=0.1)]))
escena('s09', 'foto', w('Atrapa', mas=-0.12), foto='tortuga',
       conf=dict(camara=[1.0, 1.1, 0, 0], textos=[dict(html='Aves', clase='etiqueta', x=80, y=300, en=['aves', 1, -0.1]),
                                                   dict(html='Tortugas', clase='etiqueta', x=80, y=390, en=['tortugas', 1, -0.1])]))
escena('s10', 'foto', w('Bebe', mas=-0.12), foto='lluvia',
       conf=dict(camara=[1.0, 1.1, 0, 0], lluvia=True, textos=[dict(html='Agua de lluvia', clase='etiqueta', x=80, y=300, en=['lluvia', 1, -0.1])]))
escena('s11', 'puntos', w('Ezequiel', 2, mas=-0.12), fondo='noche',
       conf=dict(n=2, cols=2, tam=120, hueco=200, x=310, y=820, nombres=[dict(i=0, texto='José'), dict(i=1, texto='Ezequiel')],
                 aparecen=[0.0, 0.25], apaga=dict(en=['muere', 1, -0.05], menos=[0]),
                 sello=dict(html='4 meses', en=['cuatro', 1, -0.05], x=80, y=300)))
escena('s12', 'foto', w('Y José', mas=-0.12), foto='noche',
       conf=dict(camara=[1.0, 1.06, 0, 0], textos=[dict(html='Solo.', clase='grande', y=520, centro=True, en=['solo', 1, -0.05], modo='grande')]))
escena('s13', 'mapa', w('Pasan', mas=-0.12), modo='meses', **PAC)
escena('s14', 'foto', w('Hasta que', mas=-0.12), foto='atolon',
       conf=dict(camara=[1.0, 1.12, 0, -20], techo=True, textos=[
           dict(html='30 ENE 2014', clase='diario', x=80, y=236, en=['treinta', 2, -0.05], modo='escribe', duracion=1.6),
           dict(html='Atolón de Ebon', clase='etiqueta', x=80, y=330, en=['atolón', 1, -0.05]),
           dict(html='Islas Marshall', clase='etiqueta', x=80, y=420, en=['Marshall', 1, -0.05])]))
escena('s15', 'mapa', w('A más', mas=-0.12), modo='llegada', **PAC)
escena('s16', 'mapa', w('Unos', mas=-0.12), modo='ciencia', **PAC)
escena('s17', 'ficha', w('Y su', mas=-0.12), fondo='atolon', conf=dict(FICHA, modo='revela', en=0.0, quita=['encaja', 1, 0.0]))
escena('s18', 'gancho', w('Cuatrocientos', 2, mas=-0.12), foto='barca',
       conf=dict(cifra='438', unidad='días', linea='A la deriva', modo='vuelta', en_cifra=['cuatrocientos', 2, -0.05],
                 en_linea=['días', 2, 0.1, 'fin']))
DURACION = w('pescar', 2, fin=True, mas=0.9)

# Subtítulos, salvo donde la pantalla ya escribe en grande lo que dice la voz.
sin_subtitulos(0, w('y no volvió', mas=-0.12))                          # 438 DÍAS · A LA DERIVA (el fotograma 0, limpio)
sin_subtitulos(w('Y José', mas=-0.12), w('Pasan', mas=-0.12))           # SOLO.
sin_subtitulos(w('Y su', mas=-0.12), DURACION)                          # SU HISTORIA ENCAJA, y vuelve el gancho

# --- Música: piano y cuerdas agudas (pieza 2: 0 % bajo 150 Hz), por debajo de la voz; sube con la tormenta y con la
# llegada, y se retira para «se queda solo» y para el «encaja».
musica('lecho', 0, DURACION, vol=0.24, fi=0.05, fo=0.3,
       puntos=[(w('Una tormenta', mas=-0.2), 0.24), (w('rompe', mas=0.2), 0.3), (w('No tienen', mas=-0.2), 0.22),
               (w('Y José', mas=-0.3), 0.1), (w('Pasan', mas=0.0), 0.24), (w('Hasta que', mas=0.0), 0.3),
               (w('Unos', mas=0.0), 0.22), (w('encaja', mas=-0.4), 0.08), (w('encaja', mas=0.4), 0.26)])

# --- Sonido: ambientes reales, bajos y continuos; nada de sonidos de interfaz.
sonido('1448', 0, vol=0.06, ini=30.0, dur=w('Una tormenta', mas=0.4), fi=0.0, fo=0.8)                      # el agua contra la barca
sonido('2570', w('Una tormenta', mas=-0.3), vol=0.12, ini=55.0, dur=w('Sin motor', mas=0.6) - w('Una tormenta', mas=-0.3), fi=0.4, fo=0.8)  # el mar de la tormenta
sonido('0154', w('Una tormenta', mas=-0.3), vol=0.04, ini=8.0, dur=w('Sin motor', mas=0.6) - w('Una tormenta', mas=-0.3), fi=0.4, fo=0.8)   # el viento
sonido('3113', w('tormenta', mas=0.05), vol=0.2, ini=2.0, dur=2.6, fo=0.8)                                  # el trueno (con el destello)
sonido('1448', w('Sin motor', mas=-0.2), vol=0.08, ini=90.0, dur=w('Ezequiel', 2, mas=0.4) - w('Sin motor', mas=-0.2), fi=0.8, fo=0.8)  # a la deriva
sonido('1529', w('pesca', mas=0.15), vol=0.2, ini=0.0, dur=1.2, fo=0.4)                                     # la mano en el agua
sonido('0740', w('Bebe', mas=-0.3), vol=0.4, ini=22.0, dur=w('Ezequiel', 2, mas=0.5) - w('Bebe', mas=-0.3), fi=0.5, fo=1.0)  # la lluvia
sonido('0147', w('Y José', mas=-0.3), vol=0.32, ini=60.0, dur=w('Pasan', mas=0.6) - w('Y José', mas=-0.3), fi=0.5, fo=0.8)    # el viento de la noche
sonido('2570', w('Hasta que', mas=-0.2), vol=0.14, ini=120.0, dur=w('A más', mas=0.6) - w('Hasta que', mas=-0.2), fi=0.6, fo=1.0)  # la rompiente del arrecife
sonido('1448', w('Cuatrocientos', 2, mas=-0.4), vol=0.06, ini=30.0, dur=DURACION - w('Cuatrocientos', 2, mas=-0.4), fi=0.6, fo=0.0)  # vuelve el principio
