# Corto 4 de supervivencia · «Dado por muerto en el Everest» (Lincoln Hall, cara norte del Everest, 25–26 de mayo de
# 2006). Lo monta el kit de BusinessForMen con la marca del canal:
#   python3 canales/businessformen/kit/montar.py --canal canales/supervivencia cortos/04-lincoln-hall
# Vertical, unos 78 s, en bucle: el último plano («el hombre al que dieron por muerto en el Everest») es el primero (DADO
# POR MUERTO · EN EL EVEREST). El secreto tachado: «lo primero que dijo» (segundo 4), que se lee en el 56 («Imagino que
# les sorprende verme aquí»). El perfil de la montaña, dibujado y a escala (escenas/perfil.html). Retención:
# ../../../RETENCION.md.
# Sonido (ver ../../CANAL.md, la regla desde el corto 3): solo efectos fuertes con su golpe en pantalla y sin ambientes de
# fondo: la ráfaga de viento al caer la noche, un único golpe grave (muy bajo) con el sello HA MUERTO y los pasos en la
# nieve de los cuatro que suben, que se paran en seco al ver algo junto al precipicio. La música, 16–20 LU bajo la voz.
# Medido con audio/revisar_mezcla.py antes de renderizar.
formato(1080, 1920, voz0=0.1, cola=0.7)
subtitulos()

FICHA = dict(cab='Lo primero que dijo', linea='Al verlos llegar:', tapada='Imagino que<br>les sorprende<br>verme aquí')
escena('s01', 'gancho', 0, foto='arista',
       conf=dict(cifra='Dado por<br>muerto', tam=190, unidad='', linea='En el Everest', camara=[1.1, 0, 30], modo='inicio'))
escena('s02', 'ficha', w('Y cuando', mas=-0.12), fondo='arista',
       conf=dict(FICHA, modo='oculta', en=['cuando', 1, -0.3], escribe=[['encontraron', 1, -0.1], ['frase', 1, 0.1, 'fin']],
                 barra=['olvidado', 1, -0.2], late=['olvidado', 1, 0.1, 'fin']))
escena('s03', 'foto', w('Veinticinco', mas=-0.12), foto='cima',
       conf=dict(camara=[1.04, 1.14, 0, 40], techo=True, textos=[
           dict(html='25 MAY 2006', clase='diario', x=80, y=236, en=['Veinticinco', 1, -0.05], modo='escribe', duracion=1.4),
           dict(html='Lincoln Hall · 50 años', clase='etiqueta', x=80, y=330, en=['Líncoln', 1, 0.0]),
           dict(html='Alpinista · Australia', clase='etiqueta', x=80, y=420, en=['australiano', 1, -0.05]),
           dict(html='Cima: 8.849 m', clase='diario', x=80, y=500, en=['cima', 1, -0.05], modo='escribe')]))   # encima de la capucha
escena('s04', 'perfil', w('Allí', mas=-0.12), modo='zona')
escena('s05', 'foto', w('Al bajar', mas=-0.12), foto='delirio',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='Mal de altura', clase='etiqueta', x=80, y=300, en=['altura', 1, -0.05]),
           dict(html='Delira.', clase='diario', x=80, y=400, en=['delirar', 1, -0.05], modo='escribe'),
           dict(html='No puede seguir.', clase='diario', x=80, y=470, en=['seguir', 1, -0.15], modo='escribe'),
           dict(html='Sus sherpas', clase='etiqueta', x=80, y=960, en=['sherpas', 1, -0.05])]))
escena('s06', 'foto', w('Cae', mas=-0.12), foto='noche',
       conf=dict(camara=[1.12, 1.2, 0, -20], brillo=0.8, temblores=[['Cae', 1, 0.05]], textos=[
           dict(html='Oxígeno: se acaba', clase='diario', x=80, y=300, en=['oxígeno', 2, -0.1], modo='escribe'),
           dict(html='Señales de vida: 0', clase='diario', x=80, y=370, en=['señales', 1, -0.1], modo='escribe'),
           dict(html='Orden: dejarlo', clase='sello', x=80, y=960, en=['dejarlo', 1, -0.05], modo='sello')]))
escena('s07', 'perfil', w('En Australia', mas=-0.12), modo='noche')
escena('s08', 'foto', w('Doce', mas=-0.12), foto='amanecer',
       conf=dict(camara=[1.0, 1.12, 0, 40], techo=True, textos=[
           dict(html='12 horas después', clase='diario', x=80, y=236, en=['Doce', 1, -0.05], modo='escribe', duracion=1.2),
           dict(html='4 alpinistas', clase='etiqueta', x=80, y=330, en=['cuatro', 1, -0.05]),
           dict(html='Junto al precipicio…', clase='etiqueta', x=80, y=420, en=['precipicio', 1, -0.1])]))
escena('s09', 'foto', w('Un hombre', mas=-0.12), foto='sentado',
       conf=dict(camara=[1.0, 1.2, 0, 60], techo=True, destellos=[['vivo', 2, -0.02]], textos=[
           dict(html='Sin guantes', clase='etiqueta', x=80, y=300, en=['guantes', 1, -0.05]),
           dict(html='Sin gorro', clase='etiqueta', x=80, y=390, en=['gorro', 1, -0.05]),
           dict(html='Con el traje abierto', clase='etiqueta', x=80, y=480, en=['abierto', 1, -0.1]),
           dict(html='Vivo', clase='sello', x=80, y=960, en=['vivo', 2, -0.02], modo='sello')]))
escena('s10', 'ficha', w('Y les', mas=-0.12), fondo='sentado',
       conf=dict(FICHA, modo='revela', en=0.05, fondo_en=0.0, quita=['Imagino', 1, -0.05]))
escena('s11', 'foto', w('Iban', mas=-0.12), foto='renuncia',
       conf=dict(camara=[1.0, 1.1, 0, 30], techo=True, textos=[
           dict(html='Iban a la cima', clase='etiqueta', x=80, y=300, en=['Iban', 1, 0.0]),
           dict(html='Renuncian', clase='sello', x=80, y=960, en=['Renuncian', 1, -0.05], modo='sello', sale=['guía', 1, -0.1]),
           dict(html='Dan Mazur, su guía', clase='etiqueta', x=80, y=390, en=['Mázur', 1, -0.05]),
           dict(html='«La cumbre<br>sigue ahí»', clase='golpe', x=80, y=560, en=['cumbre', 1, -0.1], sale=['Líncoln', 2, -0.1]),
           dict(html='«Solo tiene<br><b>una vida</b>»', clase='golpe', x=80, y=560, en=['Líncoln', 2, -0.05])]))
escena('s12', 'perfil', w('Doce', 2, mas=-0.12), modo='bajada')
escena('s13', 'foto', w('La congelación', mas=-0.12), foto='bajada',
       conf=dict(camara=[1.0, 1.1, 0, 30], techo=True, textos=[
           dict(html='Congelación', clase='etiqueta', x=80, y=300, en=['congelación', 1, -0.05]),
           dict(html='Las puntas de los dedos', clase='diario', x=80, y=390, en=['puntas', 1, -0.1], modo='escribe'),
           dict(html='Vuelve a casa', clase='sello', x=80, y=960, en=['casa', 1, -0.05], modo='sello')]))
escena('s14', 'gancho', w('El hombre', mas=-0.25), foto='arista',
       conf=dict(cifra='Dado por<br>muerto', tam=190, unidad='', linea='En el Everest', modo='vuelta',
                 en_cifra=['muerto', 3, -0.05], en_linea=['Everest', 3, 0.0]))
DURACION = w('Everest', 3, fin=True, mas=0.9)

# Subtítulos, salvo donde la pantalla ya escribe en grande lo que dice la voz.
sin_subtitulos(0, w('A la mañana', mas=-0.12))                          # DADO POR MUERTO · EN EL EVEREST (fotograma 0, limpio)
sin_subtitulos(w('ha muerto', mas=-0.1), w('Pasa', mas=-0.12))         # HA MUERTO
sin_subtitulos(w('Está', mas=-0.1), w('Y les', mas=-0.12))              # VIVO
sin_subtitulos(w('Imagino', mas=-0.12), w('Iban', mas=-0.12))           # la frase, revelada en la ficha
sin_subtitulos(w('cumbre', mas=-0.12), w('Doce', 2, mas=-0.12))        # «La cumbre sigue ahí» · «Solo tiene una vida»
sin_subtitulos(w('Pero vuelve', mas=-0.1), w('El hombre', mas=-0.25))  # VUELVE A CASA
sin_subtitulos(w('El hombre', mas=-0.25), DURACION)                     # vuelve el gancho

# --- Música: 16–20 LU bajo la voz (CANAL.md); se retira para «Está vivo» y para la frase, y vuelve después.
musica('lecho', 0, DURACION, vol=0.1, fi=0.05, fo=0.1,
       puntos=[(w('Un hombre', mas=-0.3), 0.1), (w('Está', mas=-0.3), 0.06), (w('Imagino', fin=True, mas=0.3), 0.06),
               (w('Iban', mas=0.2), 0.1)])

# --- Efectos: solo los fuertes, con su golpe en pantalla.
sonido('0154', w('Cae', mas=-0.5), vol=0.08, ini=3.6, dur=2.6, fi=0.25, fo=1.2)                # la ráfaga al caer la noche
sonido('impact-bass-1', w('muerto', 2, mas=-0.05), vol=0.03)                                  # el sello HA MUERTO
sonido('3363', w('Doce', mas=-0.1), vol=0.3, ini=0.0, dur=w('precipicio', fin=True) - w('Doce', mas=-0.1), fi=0.15, fo=0.05)  # los pasos que se paran
