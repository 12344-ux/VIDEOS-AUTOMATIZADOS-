# Corto 6 de supervivencia · «9 días en el Sahara» (Mauro Prosperi, Maratón de las Arenas, Marruecos, abril de 1994).
# Lo monta el kit de BusinessForMen con la marca del canal:
#   python3 canales/businessformen/kit/montar.py --canal canales/supervivencia cortos/06-prosperi
# Vertical, unos 73 s, en bucle: el último plano («Nueve días perdido en el Sahara») es el primero (9 DÍAS · EN EL
# SAHARA). El secreto tachado: «quién lo encontró» (segundo 5), que se lee en el 58 («Una niña tuareg»). El mapa, de
# Natural Earth (mapa.py y escenas/mapa.html): la carrera en Marruecos y Tinduf, en Argelia; su camino, en esquema.
# Retención: ../../../RETENCION.md.
# Sonido (ver ../../CANAL.md, la regla desde el corto 3): solo efectos fuertes con su golpe en pantalla y sin ambientes de
# fondo: la ráfaga de la tormenta de arena (la imagen tiembla), el aleteo de los murciélagos y el balido de las cabras. La
# música, 16–20 LU bajo la voz. Medido con audio/revisar_mezcla.py antes de renderizar.
import json
import os

formato(1080, 1920, voz0=0.1, cola=0.7)
subtitulos()
M = json.load(open(os.path.join(AQUI, 'recursos', 'mapa.json')))

FICHA = dict(cab='Quién lo encontró', linea='El noveno día:', tapada='Una niña<br>tuareg')
escena('s01', 'gancho', 0, foto='dunas', conf=dict(cifra='9', tam=400, unidad='días', linea='En el Sahara', camara=[1.1, 0, 30], modo='inicio'))
escena('s02', 'ficha', w('Y quien', mas=-0.12), fondo='dunas',
       conf=dict(FICHA, modo='oculta', en=['quien', 1, -0.1], escribe=[['encontró', 1, -0.1], ['persona', 1, 0.1, 'fin']],
                 barra=['esperaba', 1, -0.2], late=['esperaba', 1, 0.1, 'fin']))
escena('s03', 'mapa', w('Abril', mas=-0.12), modo='carrera', **M)
escena('s04', 'foto', w('Mauro', mas=-0.12), foto='carrera',
       conf=dict(camara=[1.04, 1.14, 0, 40], techo=True, textos=[
           dict(html='Mauro Prosperi', clase='etiqueta', x=80, y=300, en=['Mauro', 1, -0.05], sale=['Cuarenta', 1, -0.2]),
           dict(html='Policía · Italia', clase='etiqueta', x=80, y=390, en=['policía', 1, -0.05], sale=['Cuarenta', 1, -0.2]),
           dict(html='38 años', clase='etiqueta', x=80, y=480, en=['treinta', 1, -0.05], sale=['Cuarenta', 1, -0.2]),
           dict(html='46 °C', clase='grande', y=560, centro=True, en=['Cuarenta', 1, -0.05], modo='grande')]))
escena('s05', 'foto', w('Y de repente', mas=-0.12), foto='tormenta',
       conf=dict(camara=[1.0, 1.16, 0, 30], temblores=[['tormenta', 1, 0.1]], textos=[
           dict(html='8 horas', clase='diario', x=80, y=236, en=['ocho', 2, -0.05], modo='escribe'),
           dict(html='Solo', clase='grande', y=620, centro=True, en=['solo', 1, -0.05], modo='grande')]))
escena('s06', 'foto', w('Las reglas', mas=-0.12), foto='carrera',
       conf=dict(camara=[1.14, 1.24, -40, 60], techo=True, textos=[
           dict(html='La regla:', clase='diario', x=80, y=236, en=['reglas', 1, -0.05], modo='escribe'),
           dict(html='Quédate quieto', clase='sello', x=80, y=960, en=['quédate', 1, -0.05], modo='sello')]))
escena('s07', 'foto', w('Y él', mas=-0.12), foto='santuario',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='Santuario abandonado', clase='etiqueta', x=80, y=300, en=['santuario', 1, -0.05])]))
escena('s08', 'foto', w('Come', mas=-0.12), foto='murcielagos', conf=dict(camara=[1.0, 1.18, 0, 40]))
escena('s09', 'foto', w('Pasa un', mas=-0.12), foto='santuario',
       conf=dict(camara=[1.2, 1.04, 0, 0], techo=True, textos=[
           dict(html='· Un helicóptero', clase='diario', x=80, y=236, en=['helicóptero', 1, -0.1], modo='escribe'),
           dict(html='· Un avión', clase='diario', x=80, y=306, en=['avión', 1, -0.1], modo='escribe'),
           dict(html='· Un fuego', clase='diario', x=80, y=376, en=['fuego', 1, -0.1], modo='escribe'),
           dict(html='No lo ven', clase='sello', x=80, y=960, en=['Tampoco', 1, -0.05], modo='sello')]))
escena('s10', 'foto', w('Con un trozo', mas=-0.12), foto='carbon',
       conf=dict(camara=[1.0, 1.12, 0, 0], textos=[
           dict(html='Una despedida', clase='etiqueta', x=80, y=300, en=['despedida', 1, -0.05])]))
escena('s11', 'foto', w('Y entonces', mas=-0.12), foto='dunas',
       conf=dict(camara=[1.0, 1.15, 0, -50], techo=True, textos=[
           dict(html='Rompe la regla', clase='sello', x=80, y=960, en=['rompe', 1, -0.05], modo='sello', sale=['brújula', 1, -0.15]),
           dict(html='Brújula y mapa', clase='etiqueta', x=80, y=300, en=['brújula', 1, -0.05]),
           dict(html='Al amanecer', clase='diario', x=80, y=390, en=['amanecer', 1, -0.1], modo='escribe'),
           dict(html='Al anochecer', clase='diario', x=80, y=460, en=['anochecer', 1, -0.1], modo='escribe')]))
escena('s12', 'foto', w('El octavo', mas=-0.12), foto='oasis',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='Día 8', clase='diario', x=80, y=236, en=['octavo', 1, -0.05], modo='escribe'),
           dict(html='Un charco de agua', clase='etiqueta', x=80, y=330, en=['charco', 1, -0.05])]))
escena('s13', 'foto', w('Y el noveno', mas=-0.12), foto='rebano',
       conf=dict(camara=[1.0, 1.08, 0, 20], techo=True, textos=[
           dict(html='Día 9', clase='diario', x=80, y=236, en=['noveno', 1, -0.05], modo='escribe')]))
escena('s14', 'ficha', w('Lo encuentra', mas=-0.12), fondo='rebano',
       conf=dict(FICHA, modo='revela', en=0.05, fondo_en=0.0, quita=['niña', 1, -0.1]))
escena('s15', 'mapa', w('Su familia', 2, mas=-0.12), modo='argelia', **M)
escena('s16', 'foto', w('Había', mas=-0.12), foto='oasis',
       conf=dict(camara=[1.12, 1.2, 0, 30], techo=True, textos=[
           dict(html='−15 <i class="m">kg</i>', clase='sello', x=80, y=960, en=['quince', 1, -0.05], modo='sello')]))
escena('s17', 'gancho', w('Nueve', 2, mas=-0.12), foto='dunas',
       conf=dict(cifra='9', tam=400, unidad='días', linea='En el Sahara', modo='vuelta', en_cifra=['nueve', 2, -0.05],
                 en_linea=['sahara', 2, 0.0]))
DURACION = w('Sahara', 2, fin=True, mas=0.9)

# Subtítulos, salvo donde la pantalla ya escribe en grande lo que dice la voz.
sin_subtitulos(w('Cuarenta', mas=-0.1), w('Y de repente', mas=-0.12))      # 46 °C
sin_subtitulos(w('solo', 1, mas=-0.1), w('No ve', mas=-0.12))                  # SOLO
sin_subtitulos(w('quédate', mas=-0.1), w('Y él', mas=-0.12))                   # QUÉDATE QUIETO
sin_subtitulos(w('la regla', mas=-0.1), w('camina', mas=-0.12))               # ROMPE LA REGLA
sin_subtitulos(w('Lo encuentra', mas=-0.12), w('Su familia', 2, mas=-0.12))   # quién lo encontró, revelado en la ficha
sin_subtitulos(w('A doscientos', mas=-0.1), w('Había', mas=-0.12))         # 291 KM · FUERA DE LA CARRERA
sin_subtitulos(w('quince', mas=-0.1), DURACION)                             # −15 KG · vuelve el gancho

# --- Música: 16–20 LU bajo la voz (CANAL.md); se retira para la ficha revelada y vuelve con la familia.
musica('lecho', 0, DURACION, vol=0.085, fi=0.05, fo=0.1,
       puntos=[(w('Y el noveno', mas=-0.3), 0.085), (w('Lo encuentra', mas=-0.2), 0.055), (w('Su familia', 2, mas=-0.1), 0.085)])

# --- Efectos: solo los fuertes, con su golpe en pantalla.
sonido('0154', w('tormenta', mas=-0.5), vol=0.08, ini=3.6, dur=3.0, fi=0.25, fo=1.4)        # la ráfaga (la imagen tiembla)
sonido('2891', w('murciélagos', mas=-0.45), vol=0.1, ini=0.0, dur=2.0, fi=0.05, fo=0.6)     # el aleteo
sonido('0279', w('cabras', fin=True, mas=-0.35), vol=0.05, ini=0.2, dur=0.8, fo=0.25)         # el balido
