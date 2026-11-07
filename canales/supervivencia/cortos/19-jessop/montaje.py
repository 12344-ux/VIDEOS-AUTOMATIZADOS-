# Corto 19 de supervivencia · «Insumergible» (Violet Jessop, la camarera nacida en Argentina que iba en los tres gemelos de la
# White Star: el Olympic en su choque de 1911, el Titanic en 1912 y el Britannic en 1916). Lo monta el kit de BusinessForMen
# con la marca del canal:
#   python3 canales/businessformen/kit/montar.py --canal canales/supervivencia cortos/19-jessop
# Vertical, unos 78 s, en bucle: el último plano («Sobrevivió al Titanic. Y a sus dos barcos gemelos») es el primero
# (3 BARCOS · SOBREVIVIÓ A LOS TRES). El secreto tachado: lo único que se llevó del Britannic (segundo 3), que se lee al 86 %
# (su cepillo de dientes: en el Titanic lo había echado de menos). Los tres gemelos, dibujados (escenas/gemelos.html), salen
# cuatro veces: el Olympic, el paso al Titanic, el paso al Britannic y los tres al final, con Violet en cada uno. Violet
# Jessop es una persona real: nunca de cara. Retención: ../../../RETENCION.md.
formato(1080, 1920, voz0=0.1, cola=0.7)
subtitulos()

FICHA = dict(cab='Britannic, 1916', linea='Lo que se llevó:', tapada='Su cepillo<br>de dientes', tam=140)
GANCHO = dict(cifra='3', unidad='barcos', linea='Sobrevivió a los tres')
escena('s01', 'gancho', 0, foto='titanic', conf=dict(GANCHO, camara=[1.1, 0, 30], modo='inicio'))
escena('s02', 'ficha', w('Y cuando', mas=-0.12), fondo='britannic',
       conf=dict(FICHA, modo='oculta', en=0.05, escribe=[['lo', 1, 0.1], ['llevó', 1, 0.0, 'fin']],
                 barra=['fue', 1, -0.05], late=['pequeño', 1, -0.05]))
escena('s03', 'foto', w('Váiolet', 1, mas=-0.12), foto='pampa',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='1887', clase='diario', x=80, y=230, en=['mil', 1, -0.05], modo='escribe', duracion=0.6),
           dict(html='Violet Jessop', clase='etiqueta', x=80, y=330, en=['Váiolet', 1, -0.05]),
           dict(html='Argentina', clase='etiqueta', x=80, y=420, en=['Argentina', 1, -0.05])]))
escena('s04', 'foto', w('Con', 1, mas=-0.12), foto='camarera',
       conf=dict(camara=[1.0, 1.1, 0, 20], techo=True, textos=[
           dict(html='21 años', clase='etiqueta', x=80, y=330, en=['veintiún', 1, -0.05]),
           dict(html='Camarera', clase='etiqueta', x=80, y=420, en=['camarera', 1, -0.05])]))
escena('s05', 'gemelos', w('En', 3, mas=-0.12), modo='olympic')
escena('s06', 'foto', w('Choca', 1, mas=-0.12), foto='choque',
       conf=dict(camara=[1.0, 1.1, 0, 30], techo=True, temblores=[['Choca', 1, 0.0]], textos=[
           dict(html='20 sep 1911', clase='etiqueta', x=80, y=330, en=['Choca', 1, -0.05]),
           dict(html='HMS Hawke', clase='etiqueta', x=80, y=420, en=['buque', 1, -0.05]),
           dict(html='Ilesa', clase='sello', x=80, y=960, en=['ilesa', 1, -0.05], modo='sello')]))
escena('s07', 'gemelos', w('Al año siguiente', mas=-0.12), modo='titanic')
escena('s08', 'foto', w('Catorce', mas=-0.12), foto='iceberg',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, temblores=[['iceberg', 1, 0.0]], textos=[
           dict(html='14 abr 1912', clase='diario', x=80, y=230, en=['Catorce', 1, -0.05], modo='escribe', duracion=0.7),
           dict(html='Atlántico Norte', clase='etiqueta', x=80, y=330, en=['iceberg', 1, -0.05])]))
escena('s09', 'foto', w('La suben', mas=-0.12), foto='bote',
       conf=dict(camara=[1.0, 1.12, 0, 40], techo=True, textos=[
           dict(html='Bote 16', clase='etiqueta', x=80, y=330, en=['dieciséis', 1, -0.05])]))
escena('s10', 'foto', w('Pasa', mas=-0.12), foto='noche',
       conf=dict(camara=[1.0, 1.1, 0, 20], techo=True))
escena('s11', 'foto', w('Al amanecer', mas=-0.12), foto='carpathia',
       conf=dict(camara=[1.0, 1.1, 0, 20], techo=True, textos=[
           dict(html='Carpathia', clase='etiqueta', x=80, y=330, en=['Carpatia', 1, -0.05])]))
escena('s12', 'foto', w('Una mujer', mas=-0.12), foto='cubierta',
       conf=dict(camara=[1.0, 1.12, -20, 30], techo=True))
escena('s13', 'foto', w('Cuatro años después', mas=-0.12), foto='enfermera',
       conf=dict(camara=[1.0, 1.1, 0, 20], techo=True, textos=[
           dict(html='1916', clase='diario', x=80, y=230, en=['Cuatro', 1, -0.05], modo='escribe', duracion=0.6),
           dict(html='Enfermera', clase='etiqueta', x=80, y=330, en=['enfermera', 1, -0.05])]))
escena('s14', 'gemelos', w('Y va en el tercer', mas=-0.12), modo='britannic')
escena('s15', 'foto', w('En el mar Egeo', mas=-0.12), foto='britannic',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, temblores=[['mina', 1, 0.0]], textos=[
           dict(html='21 nov 1916', clase='diario', x=80, y=230, en=['Egeo', 1, -0.1], modo='escribe', duracion=0.7),
           dict(html='55 minutos', clase='golpe', x=80, y=330, en=['cincuenta', 1, -0.05], modo='grande')]))
escena('s16', 'foto', w('Su bote', mas=-0.12), foto='helices',
       conf=dict(camara=[1.0, 1.14, 0, 40], techo=True))
escena('s17', 'foto', w('Váiolet salta', mas=-0.12), foto='agua',
       conf=dict(camara=[1.0, 1.12, 0, -30], techo=True, temblores=[['golpea', 1, 0.0]], textos=[
           dict(html='Sobrevive', clase='sello', x=80, y=960, en=['Sobrevive', 1, -0.1], modo='sello')]))
escena('s18', 'foto', w('Años', 3, mas=-0.12), foto='craneo',
       conf=dict(camara=[1.0, 1.12, 0, 20], techo=True, textos=[
           dict(html='Años después', clase='etiqueta', x=80, y=330, en=['Años', 3, -0.05]),
           dict(html='Cráneo roto', clase='etiqueta', x=80, y=420, en=['cráneo', 1, -0.05])]))
escena('s19', 'ficha', w('Y lo que se llevó', mas=-0.12), fondo='britannic',
       conf=dict(FICHA, modo='revela', en=0.05, fondo_en=0.0, quita=['cepillo', 1, -0.05]))
escena('s20', 'foto', w('En el Titánic', mas=-0.12), foto='cepillo',   # el cepillo, revelado, se queda 1,3 s en la ficha
       conf=dict(camara=[1.0, 1.1, 0, 20], techo=True))
escena('s21', 'gemelos', w('Volvió', mas=-0.12), modo='tres')
escena('s22', 'gancho', w('Sobrevivió', 2, mas=-0.12), foto='titanic',
       conf=dict(GANCHO, modo='vuelta', en_cifra=['Sobrevivió', 2, -0.05], en_linea=['Sobrevivió', 2, 0.1]))
DURACION = w('gemelos', 2, fin=True, mas=0.9)

# Subtítulos, salvo donde la pantalla ya escribe en grande lo que dice la voz.
sin_subtitulos(w('cincuenta', mas=-0.1), w('Su bote', mas=-0.12))          # 55 MINUTOS, en grande
sin_subtitulos(w('Sobrevive', mas=-0.15), w('Años', 3, mas=-0.12))         # SOBREVIVE
sin_subtitulos(w('Y lo que se llevó', mas=-0.1), w('En el Titánic', mas=-0.12))  # el cepillo, revelado en la ficha
sin_subtitulos(w('Sobrevivió', 2, mas=-0.12), DURACION)                    # vuelve el gancho

# --- Música: 16–20 LU bajo la voz (CANAL.md); se retira para la revelación y vuelve con el cepillo.
musica('lecho', 0, DURACION, vol=0.1, fi=0.05, fo=0.1,
       puntos=[(w('Y lo que se llevó', mas=-0.4), 0.05), (w('En el Titánic', mas=-0.2), 0.1)])

# --- Efectos: solo los fuertes, con su golpe en pantalla (se ajustan con audio/revisar_mezcla.py).
sonido('1023', w('Choca', 1, mas=-0.05), vol=0.25, ini=0.0, dur=1.6, fo=0.6)         # el Hawke contra el Olympic (tiembla)
sonido('0303', w('iceberg', mas=-0.1), vol=0.15, ini=0.0, dur=2.0, fi=0.05, fo=0.8)  # el iceberg raspa el casco (tiembla)
sonido('0226', w('Carpatia', mas=-0.3), vol=0.08, ini=0.0, dur=2.6, fi=0.2, fo=1.0)  # la sirena del Carpathia al amanecer
sonido('1023', w('mina', mas=-0.05), vol=0.25, ini=0.0, dur=1.8, fo=0.8)          # la mina (tiembla)
sonido('1521', w('salta', mas=0.05), vol=0.1, ini=0.0, dur=1.5, fo=0.6)           # Violet cae al agua
