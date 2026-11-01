# Corto 8 de supervivencia · «Cortó la cuerda» (Joe Simpson y Simon Yates, Siula Grande, Andes de Perú, junio de 1985).
# Lo monta el kit de BusinessForMen con la marca del canal:
#   python3 canales/businessformen/kit/montar.py --canal canales/supervivencia cortos/08-simpson
# Vertical, unos 73 s, en bucle: el último plano («Todo empezó cuando su compañero cortó la cuerda») es el primero
# (CORTÓ LA CUERDA · CON ÉL COLGANDO). El secreto tachado: «cómo salió de la grieta» (segundo 5), que se lee en el
# 51 («Bajar más hondo»). La pared, la grieta y la salida, dibujadas (escenas/grieta.html). Retención:
# ../../../RETENCION.md.
# Sonido (ver ../../CANAL.md, la regla desde el corto 3): solo efectos fuertes con su golpe en pantalla y sin ambientes de
# fondo: la ráfaga de la ventisca (llegan la niebla y la nieve), la cuerda que se va al cortarla y el golpe de Joe en la
# repisa. La música, 16–20 LU bajo la voz. Medido con audio/revisar_mezcla.py antes de renderizar.
formato(1080, 1920, voz0=0.1, cola=0.7)
subtitulos()

FICHA = dict(cab='Cómo salió de la grieta', linea='Lo que nadie haría:', tapada='Bajar<br>más hondo')
GANCHO = dict(cifra='Cortó la<br>cuerda', tam=190, unidad='', linea='Con él colgando')
escena('s01', 'gancho', 0, foto='siula', conf=dict(GANCHO, camara=[1.1, 0, 30], modo='inicio'))
escena('s02', 'ficha', w('Para salir', mas=-0.12), fondo='siula',
       conf=dict(FICHA, modo='oculta', en=0.05, escribe=[['hizo', 1, -0.05], ['haría', 1, 0.0, 'fin']],
                 barra=['cualquiera', 1, -0.1], late=['cualquiera', 1, 0.1]))
escena('s03', 'foto', w('Junio', mas=-0.12), foto='siula',
       conf=dict(camara=[1.12, 1.2, 0, 40], techo=True, textos=[
           dict(html='JUN 1985', clase='diario', x=80, y=236, en=['Junio', 1, -0.05], modo='escribe', duracion=1.2),
           dict(html='Andes · Perú', clase='etiqueta', x=80, y=330, en=['Andes', 1, -0.05])]))
escena('s04', 'foto', w('Yóu', 1, mas=-0.12), foto='cumbre',
       conf=dict(camara=[1.04, 1.14, 0, 40], techo=True, textos=[
           dict(html='Joe Simpson', clase='etiqueta', x=80, y=300, en=['Yóu', 1, -0.05]),
           dict(html='Simon Yates', clase='etiqueta', x=80, y=390, en=['Sáimon', 1, -0.05]),
           dict(html='Siula Grande', clase='etiqueta', x=80, y=480, en=['Siula', 1, -0.05]),
           dict(html='6.344 <i class="m">m</i>', clase='sello', x=80, y=960, en=['seis', 1, -0.05], modo='sello')]))
escena('s05', 'foto', w('Al bajar', mas=-0.12), foto='pierna',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, temblores=[['cae', 1, 0.05]], textos=[
           dict(html='Pierna rota', clase='sello', x=80, y=960, en=['rompe', 1, -0.05], modo='sello')]))
escena('s06', 'grieta', w('Sáimon lo baja', mas=-0.12), modo='cuerda')
escena('s07', 'foto', w('y queda', mas=-0.12), foto='colgando',
       conf=dict(camara=[1.0, 1.1, 0, -30], textos=[
           dict(html='En el vacío', clase='etiqueta', x=80, y=300, en=['vacío', 1, -0.05])]))
escena('s08', 'foto', w('Sáimon no', mas=-0.12), foto='descenso',
       conf=dict(camara=[1.0, 1.14, 0, 40], techo=True, textos=[
           dict(html='· No lo ve', clase='diario', x=80, y=236, en=['ve', 1, -0.1], modo='escribe'),
           dict(html='· No lo oye', clase='diario', x=80, y=306, en=['oye', 1, -0.1], modo='escribe'),
           dict(html='+1 hora', clase='sello', x=80, y=960, en=['hora', 1, -0.05], modo='sello')]))
escena('s09', 'grieta', w('La nieve', mas=-0.12), modo='cuerda')
escena('s10', 'grieta', w('Yóu cae', 3, mas=-0.12), modo='grieta')
escena('s11', 'ficha', w('Así que', mas=-0.12), fondo='grieta',
       conf=dict(FICHA, modo='revela', en=0.05, fondo_en=0.0, quita=['baja', 2, -0.1]))
escena('s12', 'grieta', w('grieta', 3, fin=True, mas=-0.15), modo='salida')
escena('s13', 'foto', w('Le quedan', mas=-0.12), foto='glaciar',
       conf=dict(camara=[1.0, 1.14, 0, 40], techo=True, textos=[
           dict(html='8 <i class="m">km</i> hasta el campamento', clase='etiqueta', x=80, y=300, en=['ocho', 1, -0.05]),
           dict(html='· Sin comida', clase='diario', x=80, y=400, en=['comida', 1, -0.1], modo='escribe'),
           dict(html='· Casi sin agua', clase='diario', x=80, y=470, en=['agua', 1, -0.1], modo='escribe'),
           dict(html='· Con la pierna rota', clase='diario', x=80, y=540, en=['pierna', 3, -0.1], modo='escribe'),
           dict(html='3 días', clase='sello', x=80, y=960, en=['tres', 1, -0.05], modo='sello')]))
escena('s14', 'foto', w('Llega', mas=-0.12), foto='campamento',
       conf=dict(camara=[1.0, 1.1, 0, 30], textos=[
           dict(html='El campamento', clase='etiqueta', x=80, y=300, en=['campamento', 2, -0.05]),
           dict(html='A tiempo', clase='sello', x=80, y=960, en=['horas', 1, -0.05], modo='sello')]))   # unas horas antes de que se marchen
escena('s15', 'foto', w('Lo contó', mas=-0.12), foto='cumbre',
       conf=dict(camara=[1.14, 1.22, 0, 40], techo=True, textos=[
           dict(html='Su libro · 1988', clase='etiqueta', x=80, y=300, en=['libro', 1, -0.05]),
           dict(html='«Tocando<br>el vacío»', clase='golpe', x=80, y=560, en=['Tocando', 1, -0.1])]))
escena('s16', 'gancho', w('Todo empezó', mas=-0.12), foto='siula',
       conf=dict(GANCHO, modo='vuelta', en_cifra=['cortó', 2, -0.05], en_linea=['cuerda', 4, 0.0]))
DURACION = w('cuerda', 4, fin=True, mas=0.9)

# Subtítulos, salvo donde la pantalla ya escribe en grande lo que dice la voz.
sin_subtitulos(w('de una hora', mas=-0.1), w('La nieve', mas=-0.12))           # +1 HORA
sin_subtitulos(w('tres', mas=-0.1), w('Llega', mas=-0.12))                     # 3 DÍAS
sin_subtitulos(w('Más de seis', mas=-0.1), w('Al bajar', mas=-0.12))           # 6.344 M (con «más de 6.300» a la vez, dos cifras)
sin_subtitulos(w('Baja', 2, mas=-0.12), w('grieta', 3, fin=True, mas=-0.15))   # cómo salió, revelado en la ficha
sin_subtitulos(w('Tocando', mas=-0.12), w('Todo empezó', mas=-0.12))           # «TOCANDO EL VACÍO»
sin_subtitulos(w('Todo empezó', mas=-0.12), DURACION)                           # vuelve el gancho

# --- Música: 16–20 LU bajo la voz (CANAL.md); se retira para el corte de la cuerda y para la salida revelada.
musica('lecho', 0, DURACION, vol=0.1, fi=0.05, fo=0.1,
       puntos=[(w('La nieve', mas=-0.3), 0.1), (w('corta', mas=-0.2), 0.06), (w('Yóu cae', 3, mas=0.6), 0.1),
               (w('Así que', mas=-0.3), 0.1), (w('Baja', 2, mas=-0.2), 0.06), (w('Y encuentra', mas=0.0), 0.1)])

# --- Efectos: solo los fuertes, con su golpe en pantalla.
sonido('0154', w('visibilidad', mas=-0.45), vol=0.08, ini=3.6, dur=2.6, fi=0.25, fo=1.2)  # la ráfaga (llega la ventisca)
sonido('1818', w('corta', mas=-0.15), vol=0.07, ini=0.0, dur=1.25, fo=0.2)                  # la cuerda que se va
sonido('2453', w('sesenta', mas=0.2 - 0.46), vol=0.2, ini=0.0, dur=1.0, fo=0.3)          # el golpe en la repisa
