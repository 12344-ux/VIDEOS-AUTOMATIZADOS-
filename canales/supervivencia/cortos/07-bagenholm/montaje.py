# Corto 7 de supervivencia · «80 minutos bajo el hielo» (Anna Bågenholm, Narvik y Tromsø, Noruega, 20 de mayo de 1999).
# Lo monta el kit de BusinessForMen con la marca del canal:
#   python3 canales/businessformen/kit/montar.py --canal canales/supervivencia cortos/07-bagenholm
# Vertical, unos 67 s, en bucle: el último plano («Ochenta minutos bajo el hielo») es el primero (80 MIN · BAJO EL
# HIELO). El secreto tachado: «la regla del médico» (segundo 4), que se lee en el 43 («Caliente y muerta»). El hielo, el
# termómetro y el monitor, dibujados (escenas/hielo.html). Retención: ../../../RETENCION.md.
# Sonido (ver ../../CANAL.md, la regla desde el corto 3): solo efectos fuertes con su golpe en pantalla y sin ambientes de
# fondo: el hielo que se rompe (la imagen tiembla) y un pitido del monitor en cada latido que vuelve. La música, 16–20 LU
# bajo la voz. Medido con audio/revisar_mezcla.py antes de renderizar.
formato(1080, 1920, voz0=0.1, cola=0.7)
subtitulos()

FICHA = dict(cab='La regla del médico', linea='Muerta solo si está:', tapada='Caliente<br>y muerta')
escena('s01', 'gancho', 0, foto='rio', conf=dict(cifra='80', tam=360, unidad='min', linea='Bajo el hielo', camara=[1.1, 0, 30], modo='inicio'))
escena('s02', 'ficha', w('Todo', mas=-0.12), fondo='rio',
       conf=dict(FICHA, modo='oculta', en=0.05, escribe=[['por', 1, -0.05], ['regla', 1, 0.0, 'fin']],
                 barra=['médico', 1, -0.05], late=['médico', 1, 0.1]))
escena('s03', 'foto', w('Mayo', mas=-0.12), foto='esqui',
       conf=dict(camara=[1.04, 1.14, 0, 40], techo=True, textos=[
           dict(html='MAY 1999', clase='diario', x=80, y=236, en=['Mayo', 1, -0.05], modo='escribe', duracion=1.2, sale=['Ana', 1, -0.2]),
           dict(html='Norte de Noruega', clase='etiqueta', x=80, y=330, en=['Norte', 1, -0.05], sale=['Ana', 1, -0.2]),
           dict(html='Anna Bågenholm', clase='etiqueta', x=80, y=300, en=['Ana', 1, -0.05]),
           dict(html='Médica · 29 años', clase='etiqueta', x=80, y=390, en=['médica', 1, -0.05])]))
escena('s04', 'foto', w('Pierde', mas=-0.12), foto='rio', conf=dict(camara=[1.06, 1.2, 0, 50], temblores=[['cae', 1, 0.05]]))
escena('s05', 'hielo', w('El hielo', 2, mas=-0.3), modo='hielo')     # la 1.ª, «bajo el hielo»
escena('s06', 'foto', w('Encuentra', mas=-0.12), foto='bajo_hielo',
       conf=dict(camara=[1.0, 1.12, 0, 0], textos=[
           dict(html='Una bolsa de aire', clase='etiqueta', x=80, y=300, en=['bolsa', 1, -0.05]),
           dict(html='Aguanta', clase='sello', x=80, y=960, en=['aguanta', 1, -0.05], modo='sello')]))
escena('s07', 'hielo', w('A los', 1, mas=-0.12), modo='hielo')
escena('s08', 'foto', w('La sacan', mas=-0.12), foto='rescate',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='Minuto 80', clase='diario', x=80, y=236, en=['ochenta', 2, -0.05], modo='escribe'),
           dict(html='No respira', clase='diario', x=80, y=306, en=['respira', 1, -0.1], modo='escribe')]))
escena('s09', 'foto', w('Su corazón', 2, mas=-0.12), foto='monitor',
       conf=dict(camara=[1.0, 1.1, 0, 0], textos=[
           dict(html='Sin pulso', clase='sello', x=80, y=960, en=['late', 1, -0.05], modo='sello')]))
escena('s10', 'foto', w('Un helicóptero', mas=-0.12), foto='helicoptero',
       conf=dict(camara=[1.0, 1.12, 0, -30], textos=[
           dict(html='Hospital de Tromsø', clase='etiqueta', x=80, y=300, en=['hospital', 1, -0.05])]))
escena('s11', 'hielo', w('Su temperatura', mas=-0.12), modo='temperatura')
escena('s12', 'ficha', w('Pero', mas=-0.12), fondo='quirofano',
       conf=dict(FICHA, modo='revela', en=0.05, fondo_en=0.0, quita=['caliente', 1, -0.1]))
escena('s13', 'foto', w('Más de cien', mas=-0.12), foto='quirofano',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='+100 médicos y enfermeros', clase='etiqueta', x=80, y=300, en=['cien', 1, -0.05]),
           dict(html='9 horas', clase='sello', x=80, y=960, en=['nueve', 2, -0.05], modo='sello')]))   # la 1.ª, «noventa y nueve»
escena('s14', 'hielo', w('Una máquina', mas=-0.12), modo='latido')
escena('s15', 'foto', w('Despierta', mas=-0.12), foto='hospital',
       conf=dict(camara=[1.0, 1.14, 0, 40], techo=True, textos=[
           dict(html='10 días después', clase='diario', x=80, y=236, en=['Despierta', 1, -0.05], modo='escribe', sale=['Años', 1, -0.25]),
           dict(html='Paralizada', clase='etiqueta', x=80, y=330, en=['paralizada', 1, -0.05], sale=['Años', 1, -0.25]),
           dict(html='Del cuello para abajo', clase='etiqueta', x=80, y=420, en=['cuello', 1, -0.05], sale=['Años', 1, -0.25]),
           dict(html='Se recupera', clase='sello', x=80, y=960, en=['recupera', 1, -0.05], modo='sello'),
           dict(html='Años después', clase='diario', x=80, y=236, en=['Años', 1, -0.05], modo='escribe'),
           dict(html='Radióloga', clase='etiqueta', x=80, y=330, en=['radióloga', 1, -0.05]),
           dict(html='En el hospital que la salvó', clase='etiqueta', x=80, y=420, en=['hospital', 2, -0.05])]))
escena('s16', 'gancho', w('Ochenta', 3, mas=-0.12), foto='rio',
       conf=dict(cifra='80', tam=360, unidad='min', linea='Bajo el hielo', modo='vuelta', en_cifra=['ochenta', 3, -0.05],
                 en_linea=['hielo', 3, 0.0]))
DURACION = w('hielo', 3, fin=True, mas=0.9)

# Subtítulos, salvo donde la pantalla ya escribe en grande lo que dice la voz.
sin_subtitulos(w('caliente', mas=-0.12), w('Más de cien', mas=-0.12))     # la regla, revelada en la ficha
sin_subtitulos(w('Ochenta', 3, mas=-0.12), DURACION)                        # vuelve el gancho

# --- Música: 16–20 LU bajo la voz (CANAL.md); se retira para la regla revelada y vuelve con el equipo.
musica('lecho', 0, DURACION, vol=0.1, fi=0.05, fo=0.1,
       puntos=[(w('Pero', mas=-0.3), 0.1), (w('caliente', mas=-0.3), 0.06), (w('Más de cien', mas=-0.1), 0.1)])

# --- Efectos: solo los fuertes, con su golpe en pantalla.
sonido('2206', w('rompe', mas=-0.5), vol=0.2, ini=0.0, dur=1.3, fo=0.3)                 # el hielo se rompe (y tiembla)
for k in range(2):                                                                       # un pitido en cada latido:
    sonido('1310', w('latir', mas=0.05 + 0.8 * k), vol=0.03, ini=1.38, dur=0.3, fo=0.05)  # la punta, en «latir» + 0,07 + 0,8·k
