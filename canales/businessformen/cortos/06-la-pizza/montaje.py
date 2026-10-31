# Corto 6 · «La pizza» (marketing y honestidad). Lo lee canales/businessformen/kit/montar.py: cortos/06-la-pizza.
# Vertical, 43 s, en bucle. La idea, para que se entienda: admitir el fallo en público, y arreglarlo, le hizo vender más.
# Edición: 2.5D en la pizza y en la masa, las críticas dentro de la pantalla de la sala de directivos, transiciones con
# causa (barridos, la cortina roja de la marca, una subida) y un golpe rojo para la pregunta final, con la firma BFM.
formato(1080, 1920, voz0=0.1, cola=0.45)
subtitulos()

PANTALLA = dict(px=60, py=300, pw=960, ph=520, pt=100)   # la parte de arriba de la pantalla de la sala, medida en la imagen
escena('s01', 'pizza', 0)                                                           # R9 2.5D: LO DIJO EN LA TELE
escena('s02', 'quejas', w('Era Dóminos', mas=-0.2), entrada='barrido')              # R8: «sabe a cartón», «a kétchup»
escena('s03', 'anuncio', w('En vez', mas=-0.2), entrada='cortina', **PANTALLA)      # R9 + R8: las críticas en la pantalla
escena('s04', 'receta', w('Después', mas=-0.2), entrada='subida')                  # R9 2.5D + R5: masa, salsa, queso
escena('s05', 'ventas', w('En los tres', mas=-0.2), entrada='barrido')             # R6 + R3: +14,3 %
escena('s06', 'gano', w('No ganó', mas=-0.2))                                       # R2: esconder, tachado; admitirlo y arreglarlo
escena('s07', 'golpe', w('Si tu producto', mas=-0.2),                               # R1: la pregunta, con la firma BFM
       etq='Si tu producto tiene un problema,', b1='Tus clientes<br>ya lo saben.', b2='¿Lo sabes tú?',
       conf={'etq': {'palabra': 'si', 'grande': True}, 'b1': {'palabra': 'tus', 'y': 380, 'tam': 130},
             'b2': {'palabra': 'lo', 'n': 4, 'y': 700, 'tam': 150, 'sube': -24}, 'firma': True, 'firma_t': 3.6})
DURACION = w('tú', fin=True, mas=1.45)

sin_subtitulos(0, w('Era Dóminos', mas=-0.25))                    # el gancho ya lo escribe
sin_subtitulos(w('Sus clientes', mas=-0.2), w('En vez', mas=-0.25))
sin_subtitulos(w('Después', mas=-0.25), DURACION)               # la receta, el dato, la lección y la pregunta: escritos

# --- Música: lecho sin entrada; se calla en el golpe.
musica('lecho', 0, DURACION, vol=0.27, fi=0.05, fo=0.3,
       puntos=[(w('Si tu producto', mas=-0.45), 0.27), (w('Si tu producto', mas=-0.2), 0.0)])

# --- Efectos
sonido('1786', w('mala', mas=0.35), vol=0.35)                                         # la tele que se apaga, tras «mala»
sonido('whoosh-short', w('Era Dóminos', mas=-0.22), vol=0.28)
sonido('pop', w('masa', mas=-0.2), vol=0.3)
sonido('pop', w('salsa', mas=-0.2), vol=0.3)
sonido('whoosh', w('En vez', mas=-0.25), vol=0.22)
sonido('click', w('anuncio', mas=-0.08), vol=0.4)
sonido('whoosh-short', w('Después', mas=-0.22), vol=0.25)
for k in ('masa', 'salsa'):
    sonido('click-soft', w(k, 2, mas=-0.08), vol=0.4)
sonido('click-soft', w('queso', mas=-0.08), vol=0.4)
sonido('whoosh-short', w('En los tres', mas=-0.22), vol=0.25)
sonido('riser', w('ciento', mas=-2.8), vol=0.26, ini=1.2, dur=2.8, fo=0.15)          # sube hasta el +14,3 %
sonido('impact-bass-1', w('ciento', mas=0.0), vol=0.26)
sonido('click', w('fallo', fin=True, mas=0.05), vol=0.45)                             # ESCONDER, tachado
sonido('impact-bass-2', w('Si tu producto', mas=-0.22), vol=0.34)                     # el golpe rojo
