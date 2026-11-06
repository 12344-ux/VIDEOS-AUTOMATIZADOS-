# Corto 17 de supervivencia · «133 días solo en una balsa» (Poon Lim, Atlántico Sur, 1942–1943). Lo monta el kit de
# BusinessForMen con la marca del canal:
#   python3 canales/businessformen/kit/montar.py --canal canales/supervivencia cortos/17-poon-lim
# Vertical, unos 78 s, en bucle: el último plano («Ciento treinta y tres días solo en una balsa») es el primero (133 DÍAS ·
# SOLO EN UNA BALSA). El secreto tachado: lo que bebió cuando se quedó sin agua (segundo 6), que se lee al 74 % («Sangre de
# tiburón»). El mapa del Atlántico ecuatorial (mapa.py y escenas/mapa.html) y la balsa vista desde arriba
# (escenas/balsa.html). Poon Lim es una persona real: nunca de cara; nada de sangre en imagen (el tiburón, en silueta).
# Retención: ../../../RETENCION.md.
import json
import os

M = json.load(open(os.path.join(AQUI, 'recursos', 'mapa.json')))
formato(1080, 1920, voz0=0.1, cola=0.7)
subtitulos()

FICHA = dict(cab='Sin agua', linea='Lo que bebió:', tapada='Sangre de<br>tiburón')
GANCHO = dict(cifra='133', unidad='días', linea='Solo en una balsa')
escena('s01', 'gancho', 0, foto='balsa', conf=dict(GANCHO, camara=[1.1, 0, 30], modo='inicio'))
escena('s02', 'foto', w('Y', 2, mas=-0.12), foto='tiburon',
       conf=dict(camara=[1.0, 1.16, 0, 30], techo=True, textos=[
           dict(html='No sabía nadar', clase='sello', x=80, y=960, en=['no', 1, -0.05], modo='sello')]))
escena('s03', 'ficha', w('Cuando', mas=0.0), fondo='lucha',
       conf=dict(FICHA, modo='oculta', en=0.05, escribe=[['Cuando', 1, 0.1], ['bebió', 1, 0.0, 'fin']],
                 barra=['algo', 1, -0.05], late=['imaginaría', 1, -0.05]))
escena('s04', 'mapa', w('Atlántico', mas=-0.12), modo='hundido', **M)
escena('s05', 'foto', w('viaja', mas=-0.12), foto='carguero',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='Carguero británico', clase='etiqueta', x=80, y=330, en=['carguero', 1, -0.05])]))
escena('s06', 'foto', w('Un', 3, mas=-0.12), foto='torpedo',
       conf=dict(camara=[1.0, 1.14, 0, 20], techo=True, destellos=[['torpedea', 1, 0.0]], temblores=[['torpedea', 1, 0.05]],
                 textos=[dict(html='Submarino alemán', clase='etiqueta', x=80, y=330, en=['submarino', 1, -0.05]),
                         dict(html='2 minutos', clase='sello', x=80, y=960, en=['minutos', 1, -0.05], modo='sello')]))
escena('s07', 'puntos', w('De', 2, mas=-0.12), fondo='torpedo',
       conf=dict(n=54, cols=9, tam=56, hueco=20, x=80, y=460, aparecen=[['cincuenta', 1, -0.05], ['bordo', 1, 0.2]],
                 cifra=dict(html='54 <small>a bordo del Benlomond</small>', x=80, y=220), apaga=dict(en=['solo', 2, -0.05], menos=[40], ritmo=0.012),
                 sello=dict(html='1 de 54', en=['salva', 1, -0.05], x=80, y=1020)))
escena('s08', 'balsa', w('Tras', mas=0.2), modo='inventario', fondo='luna')   # la foto no se ve en este modo
escena('s09', 'foto', w('Se', 5, mas=-0.12), foto='anzuelo',
       conf=dict(camara=[1.0, 1.14, 0, 20], techo=True, textos=[
           dict(html='Sin comida', clase='etiqueta', x=80, y=330, en=['comida', 1, -0.05]),
           dict(html='Linterna y clavo: anzuelos', clase='etiqueta', x=80, y=420, en=['pieza', 1, -0.05])]))
escena('s10', 'foto', w('Pesca', 1, mas=-0.12), foto='gaviota',
       conf=dict(camara=[1.0, 1.1, 0, 20], techo=True, textos=[
           dict(html='Pesca', clase='etiqueta', x=80, y=330, en=['Pesca', 1, -0.05]),
           dict(html='Caza gaviotas', clase='etiqueta', x=80, y=420, en=['gaviotas', 1, -0.05])]))
escena('s11', 'foto', w('bebe', 1, mas=-0.12), foto='lluvia',
       conf=dict(camara=[1.04, 1.12, 0, 20], techo=True, lluvia=True, textos=[
           dict(html='Agua de lluvia', clase='etiqueta', x=80, y=330, en=['bebe', 1, -0.05])]))
escena('s12', 'foto', w('Un', 5, mas=-0.12), foto='pasa',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='Lo ve', clase='etiqueta', x=80, y=330, en=['ve', 1, -0.05]),
           dict(html='Sigue de largo', clase='etiqueta', x=80, y=420, en=['sigue', 1, -0.1])]))
escena('s13', 'foto', w('avión', mas=-0.1), foto='avion',
       conf=dict(camara=[1.0, 1.14, 0, 30], techo=True, destellos=[['tormenta', 1, 0.0]], textos=[
           dict(html='Le lanza una boya', clase='etiqueta', x=80, y=330, en=['boya', 1, -0.05]),
           dict(html='Lo pierde', clase='etiqueta', x=80, y=420, en=['pierde', 1, -0.05])]))
escena('s14', 'balsa', w('Deja', 1, mas=-0.12), modo='lunas', fondo='luna')
escena('s15', 'foto', w('Pero', 2, mas=-0.12), foto='balsa',
       conf=dict(camara=[1.18, 1.06, 0, -30], origen='50% 70%', techo=True, brillo=1.05, textos=[
           dict(html='Sin lluvia, sin agua', clase='etiqueta', x=80, y=330, en=['deja', 2, -0.05])]))
escena('s16', 'foto', w('Con', 4, mas=-0.12), foto='tiburon',
       conf=dict(camara=[1.08, 1.0, 0, -20], techo=True, textos=[
           dict(html='Cebo: restos de gaviota', clase='etiqueta', x=80, y=330, en=['restos', 1, -0.05]),
           dict(html='Un tiburón', clase='etiqueta', x=80, y=420, en=['tiburón', 1, -0.05])]))
escena('s17', 'foto', w('El', 2, mas=-0.12), foto='lucha',
       conf=dict(camara=[1.0, 1.12, 0, 20], techo=True, temblores=[['ataca', 1, 0.0], ['golpes', 1, 0.05]], textos=[
           dict(html='Lo ataca', clase='etiqueta', x=80, y=330, en=['ataca', 1, -0.05]),
           dict(html='A golpes con la jarra', clase='etiqueta', x=80, y=420, en=['mata', 1, -0.1])]))
escena('s18', 'ficha', w('Y', 12, mas=-0.12), fondo='lucha',
       conf=dict(FICHA, modo='revela', en=0.05, fondo_en=0.0, quita=['sangre', 1, -0.05]))
escena('s19', 'foto', w('Y', 13, mas=-0.12), foto='color',
       conf=dict(camara=[1.0, 1.1, 0, 20], techo=True, textos=[
           dict(html='Cambia de color', clase='etiqueta', x=80, y=330, en=['mar', 1, -0.1])]))
escena('s20', 'mapa', w('Hay', mas=-0.12), modo='deriva', **M)
escena('s21', 'foto', w('Ha', 1, mas=-0.12), foto='pescadores',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='−9 <i class="m">kg</i>', clase='etiqueta', x=80, y=330, en=['kilos', 1, -0.05]),
           dict(html='Vivo', clase='sello', x=80, y=960, en=['vivo', 1, -0.05], modo='sello')]))
escena('s22', 'foto', w('Nadie', 2, mas=-0.12), foto='luna',
       conf=dict(camara=[1.0, 1.14, 0, 40], techo=True, textos=[
           dict(html='Récord en una balsa', clase='etiqueta', x=80, y=330, en=['balsa', 3, -0.05]),
           # La frase cae sobre la luna llena (2,45:1 sin caja): va en una caja oscura, como los rótulos.
           dict(html='<span style="display: inline-block; background: rgba(11, 10, 9, 0.82); padding: 0.18em 0.35em 0.12em; border-left: 6px solid #ff5e1a">«Espero que nadie tenga<br>que batir este récord»</span>',
                clase='diario', x=80, y=450, en=['espero', 1, -0.1], modo='aparece')]))
escena('s23', 'gancho', w('Ciento', 2, mas=-0.12), foto='balsa',
       conf=dict(GANCHO, modo='vuelta', en_cifra=['Ciento', 2, -0.05], en_linea=['Ciento', 2, 0.1]))
DURACION = w('balsa', 4, fin=True, mas=0.9)

# Subtítulos, salvo donde la pantalla ya escribe en grande lo que dice la voz.
sin_subtitulos(w('Y', 2, mas=-0.1), w('Cuando', mas=-0.12))           # NO SABÍA NADAR
sin_subtitulos(w('Se', 2, mas=-0.1), w('De', 2, mas=-0.12))            # 2 MINUTOS
sin_subtitulos(w('Y', 12, mas=-0.1), w('Y', 13, mas=-0.12))            # la sangre de tiburón, revelada en la ficha
sin_subtitulos(w('Pero', 3, mas=-0.1), w('Nadie', 2, mas=-0.12))       # VIVO
sin_subtitulos(w('espero', mas=-0.15), w('Ciento', 2, mas=-0.12))      # la frase, en pantalla
sin_subtitulos(w('Ciento', 2, mas=-0.12), DURACION)                     # vuelve el gancho

# --- Música: 16–20 LU bajo la voz (CANAL.md); se retira para la revelación y vuelve con el mar que cambia de color.
musica('lecho', 0, DURACION, vol=0.1, fi=0.05, fo=0.1,
       puntos=[(w('El', 2, mas=-0.3), 0.1), (w('Y', 12, mas=-0.25), 0.05), (w('Y', 13, mas=-0.2), 0.1)])

# --- Efectos: solo los fuertes, con su golpe en pantalla (se ajustan con audio/revisar_mezcla.py).
sonido('1023', w('torpedea', mas=-0.05), vol=0.2, ini=0.0, dur=2.6, fo=1.0)      # el torpedo, con el destello
sonido('3008', w('avión', mas=-0.3), vol=0.25, ini=0.0, dur=2.4, fi=0.5, fo=0.8)  # el avión que pasa
sonido('3113', w('tormenta', mas=-0.05), vol=0.15, ini=0.0, dur=2.4, fo=1.0)     # el trueno, con su destello
sonido('2453', w('golpes', mas=-0.02), vol=0.15, ini=0.0, dur=0.8, fo=0.3)       # el golpe con la jarra
