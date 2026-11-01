# Corto 5 de supervivencia · «69 días bajo tierra» (los 33 mineros de la mina San José, Atacama, Chile, 5 de agosto a
# 13 de octubre de 2010). Lo monta el kit de BusinessForMen con la marca del canal:
#   python3 canales/businessformen/kit/montar.py --canal canales/supervivencia cortos/05-los-33
# Vertical, unos 80 s, en bucle: el último plano («Sesenta y nueve días bajo tierra») es el primero (69 DÍAS · BAJO
# TIERRA). El secreto tachado: «lo que decía el papel» (segundo 7), que se lee en el 62 («Estamos bien en el refugio los
# 33»). La mina, en corte y dibujada (escenas/mina.html): el derrumbe, las sondas, la del día 17 y la cápsula. Retención:
# ../../../RETENCION.md.
# Sonido (ver ../../CANAL.md, la regla desde el corto 3): solo efectos fuertes con su golpe en pantalla y sin ambientes de
# fondo: el estruendo del derrumbe con el bloque que cae, tres golpes metálicos en la sonda y el grito de la calle. La
# música, 16–20 LU bajo la voz. Medido con audio/revisar_mezcla.py antes de renderizar.
formato(1080, 1920, voz0=0.1, cola=0.7)
subtitulos()

FICHA = dict(cab='Día 17', linea='El papel decía:', tapada='Estamos bien<br>en el refugio<br>los 33')
escena('s01', 'gancho', 0, foto='refugio', conf=dict(cifra='69', unidad='días', linea='Bajo tierra', camara=[1.1, 0, 30], modo='inicio'))
escena('s02', 'ficha', w('Pero', 1, mas=-0.12), fondo='refugio',
       conf=dict(FICHA, modo='oculta', en=['durante', 1, -0.3], escribe=[['respuesta', 1, -0.1], ['papel', 1, 0.0, 'fin']],
                 barra=['papel', 1, 0.05, 'fin'], late=['papel', 1, 0.2, 'fin']))
escena('s03', 'foto', w('Cinco', mas=-0.12), foto='desierto',
       conf=dict(camara=[1.04, 1.14, 0, 40], techo=True, textos=[
           dict(html='5 AGO 2010', clase='diario', x=80, y=236, en=['Cinco', 1, -0.05], modo='escribe', duracion=1.3),
           dict(html='Mina San José', clase='etiqueta', x=80, y=330, en=['San', 1, -0.05]),
           dict(html='Desierto de Atacama · Chile', clase='etiqueta', x=80, y=420, en=['Atacama', 1, -0.05])]))
escena('s04', 'mina', w('La montaña', mas=-0.12), modo='derrumbe')
escena('s05', 'foto', w('Hay comida', mas=-0.12), foto='atun',
       conf=dict(camara=[1.0, 1.16, 0, 40], techo=True, textos=[
           dict(html='Comida: 2 o 3 días', clase='diario', x=80, y=236, en=['comida', 1, -0.1], modo='escribe'),
           dict(html='33 hombres', clase='sello', x=80, y=960, en=['treinta', 2, -0.05], modo='sello', sale=['Urzúa', 1, -0.2]),
           dict(html='Luis Urzúa · jefe de turno', clase='etiqueta', x=80, y=330, en=['Urzúa', 1, -0.05]),
           dict(html='· 1 cucharada de atún', clase='diario', x=80, y=430, en=['cucharada', 1, -0.1], modo='escribe'),
           dict(html='· 1 sorbo de leche', clase='diario', x=80, y=500, en=['sorbo', 1, -0.1], modo='escribe'),
           dict(html='Cada 48 horas', clase='sello', x=80, y=960, en=['cuarenta', 1, -0.05], modo='sello')]))
escena('s06', 'mina', w('Arriba', 1, mas=-0.12), modo='sondas')
escena('s07', 'foto', w('Arriba', 2, mas=-0.12), foto='campamento',
       conf=dict(camara=[1.0, 1.1, 0, 30], techo=True, textos=[
           dict(html='Campamento Esperanza', clase='etiqueta', x=80, y=300, en=['Arriba', 2, 0.1]),
           dict(html='¿Vivos?', clase='diario', x=80, y=400, en=['vivos', 3, -0.1], modo='escribe')]))
escena('s08', 'mina', w('Hasta que', mas=-0.12), modo='dia17')
escena('s09', 'foto', w('Cuando', mas=-0.12), foto='sonda',
       conf=dict(camara=[1.0, 1.18, 0, 0], textos=[
           dict(html='22 AGO 2010 · día 17', clase='diario', x=80, y=236, en=['Cuando', 1, 0.0], modo='escribe', duracion=1.2)]))
escena('s10', 'ficha', w('Estamos', mas=-0.12), fondo='sonda',
       conf=dict(FICHA, modo='revela', en=0.05, fondo_en=0.0, quita=['Estamos', 1, -0.05]))
escena('s11', 'foto', w('Chile', 2, mas=-0.12), foto='fiesta',
       conf=dict(camara=[1.0, 1.1, 0, 30], techo=True, textos=[
           dict(html='Chile, a la calle', clase='etiqueta', x=80, y=300, en=['calle', 1, -0.1])]))
escena('s12', 'mina', w('Cincuenta', 1, mas=-0.12), modo='rescate')
escena('s13', 'foto', w('Unos', mas=-0.12), foto='capsula',
       conf=dict(camara=[1.0, 1.12, 0, 0], techo=True, textos=[
           dict(html='1.000 millones', clase='golpe', x=80, y=560, en=['millones', 1, -0.15]),
           dict(html='Lo ven en directo', clase='etiqueta', x=80, y=700, en=['directo', 1, -0.1])]))
escena('s14', 'puntos', w('Treinta', 4, mas=-0.12), fondo='capsula',
       conf=dict(n=33, cols=11, tam=52, hueco=22, x=144, y=700, cifra=dict(html='33<small>de 33</small>', x=80, y=300),
                 aparecen=[0.0, 0.45], apaga=dict(en=['treinta', 5, -0.05], menos=list(range(33))),
                 sello=dict(html='Todos vivos', en=['tres', 6, 0.1, 'fin'], x=80, y=980)))
escena('s15', 'gancho', w('Sesenta', 2, mas=-0.12), foto='refugio',
       conf=dict(cifra='69', unidad='días', linea='Bajo tierra', modo='vuelta', en_cifra=['sesenta', 2, -0.05],
                 en_linea=['tierra', 2, 0.0]))
DURACION = w('tierra', 2, fin=True, mas=0.9)

# Subtítulos, salvo donde la pantalla ya escribe en grande lo que dice la voz.
sin_subtitulos(0, w('Sesenta', 1, mas=-0.12))                              # 69 DÍAS · BAJO TIERRA (el fotograma 0, limpio)
sin_subtitulos(w('Estamos', mas=-0.12), w('Chile', 2, mas=-0.12))       # la nota, revelada en la ficha
sin_subtitulos(w('Unos', mas=-0.12), DURACION)                          # 1.000 MILLONES · 33 DE 33 · vuelve el gancho

# --- Música: 16–20 LU bajo la voz (CANAL.md); se retira para la nota y vuelve con la calle.
musica('lecho', 0, DURACION, vol=0.1, fi=0.05, fo=0.1,
       puntos=[(w('Cuando', mas=-0.3), 0.1), (w('Estamos', mas=-0.3), 0.04), (w('Chile', 2, mas=-0.1), 0.1)])

# --- Efectos: solo los fuertes, con su golpe en pantalla.
sonido('1023', w('derrumba', mas=0.05), vol=0.35, ini=0.0, dur=4.4, fo=1.6)                   # el derrumbe (cae el bloque)
for k, ini in enumerate((0.05, 1.25, 2.35)):                                                 # tres golpes en la sonda
    sonido('3589', w('golpean', mas=0.45 * k), vol=0.08, ini=ini, dur=0.7, fo=0.3)
sonido('0236', w('Chile', 2, mas=-0.15), vol=0.08, ini=0.0, dur=3.0, fi=0.05, fo=1.2)         # el grito de la calle
