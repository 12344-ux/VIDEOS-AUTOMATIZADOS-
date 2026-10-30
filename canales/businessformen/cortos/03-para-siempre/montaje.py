# Corto 3 · «Para siempre» (marca). Lo lee canales/businessformen/kit/montar.py: cortos/03-para-siempre.
# Vertical, 53 s. Gancho con el dato (1.500 años cambiados en 14) y golpe rojo en «por un anuncio»; la lección cierra con
# el segundo golpe rojo y la firma BFM, y el bucle vuelve al anillo. El motivo: el anillo y los anillos de la rejilla.
formato(1080, 1920, voz0=0.1, cola=0.45)
subtitulos()

escena('s01', 'anillo', 0)                                       # R9: 1.500 AÑOS DE TRADICIÓN; CAMBIADOS EN 14
escena('s02', 'golpe', w('Por', mas=-0.12),                      # R1: POR UN ANUNCIO
       etq='', b1='Por un<br>anuncio.', b2='',
       conf={'etq': None, 'b1': {'palabra': 'Por', 'y': 560, 'tam': 190}, 'b2': None, 'firma': False})
escena('s03', 'japon', w('En Japón', mas=-0.2))                  # R3 + R6: 100 anillos; −5 % en 1967, 60 % en 1981
escena('s04', 'debeers', w('Detrás', mas=-0.2))                  # R2 + R11: DE BEERS; EE. UU. 1938 → JAPÓN 1967
escena('s05', 'precio', w('En mil novecientos treinta', mas=-0.05))  # R3 → R6 → R7: 1938; el precio hundido; el encargo
escena('s06', 'frase', w('En mil novecientos cuarenta', mas=-0.2))  # R9 + R2: la máquina de escribir; «A Diamond Is Forever»
escena('s07', 'sueldo', w('Después', mas=-0.05))                  # R3: 2 MESES DE SUELDO; el sello TAMPOCO ERA TRADICIÓN
escena('s08', 'significan', w('La gente', mas=-0.2))             # R2: PRODUCTOS tachado; SIGNIFICAN
escena('s09', 'golpe', w('Y quien', mas=-0.15),                  # R1: la lección, con la firma BFM
       etq='', b1='Quien decide<br>lo que significan,', b2='decide<br>el precio.',
       conf={'etq': None, 'b1': {'palabra': 'quien', 'y': 330, 'tam': 84}, 'b2': {'palabra': 'decide', 'n': 2, 'y': 600, 'tam': 150, 'sube': -24},
             'firma': True, 'firma_t': 1.6})
DURACION = w('precio', 2, fin=True, mas=1.3)            # la última frase, 2 s en pantalla

sin_subtitulos(0, w('En Japón', mas=-0.25))                       # el gancho y el golpe ya lo escriben
sin_subtitulos(w('que un compromiso', mas=-0.2), w('En mil novecientos cuarenta', mas=-0.25))  # el encargo, escrito
sin_subtitulos(w('una redactora', mas=-0.2), w('Después', mas=-0.25))                          # la frase, escrita
sin_subtitulos(w('La gente', mas=-0.25), DURACION)

# --- Música: un lecho elegante (arpa y celesta), sin entrada; se calla en los dos golpes rojos.
musica('lecho', 0, DURACION, vol=0.3, fi=0.05, fo=0.3,
       puntos=[(w('Por', mas=-0.3), 0.3), (w('Por', mas=-0.12), 0.0), (w('En Japón', mas=-0.4), 0.0), (w('En Japón', mas=-0.1), 0.3),
               (w('Y quien', mas=-0.35), 0.3), (w('Y quien', mas=-0.12), 0.0)])

# --- Efectos
sonido('impact-bass-1', w('cambiados', mas=-0.05), vol=0.22)                 # CAMBIADOS EN 14
sonido('impact-bass-2', w('Por', mas=-0.14), vol=0.36)                       # el golpe rojo
sonido('whoosh', w('En Japón', mas=-0.25), vol=0.22)
sonido('pop', w('cinco', mas=0.02), vol=0.3)
sonido('key-press', w('ochenta', mas=-0.12), vol=0.4)                        # 1967 → 1981
sonido('typing', w('sesenta', 2, mas=-0.05), vol=0.3, dur=0.8, fo=0.2)       # se encienden sesenta
sonido('whoosh-short', w('Detrás', mas=-0.22), vol=0.25)
sonido('pop', w('Estados', mas=-0.12), vol=0.3)
sonido('pop', w('Unidos', mas=0.45), vol=0.3)
sonido('whoosh', w('En mil novecientos treinta', mas=-0.25), vol=0.22)
for t in (w('mil', 4), w('novecientos', 3), w('treinta'), w('ocho')):
    sonido('key-press', t - 0.03, vol=0.4)
sonido('2212', w('contrató', mas=-0.2), vol=0.6, dur=1.2, fo=0.2)             # llega el encargo
sonido('2841', w('un', 4, mas=-0.05), vol=0.5, ini=2.0, dur=1.45, fo=0.15)   # se escribe la frase
sonido('2844', w('siempre', fin=True, mas=0.0), vol=0.4, ini=0.6, dur=0.75, fo=0.25)  # la campanilla
sonido('whoosh-short', w('Después', mas=-0.22), vol=0.25)
sonido('pop', w('dos', mas=-0.1), vol=0.35)
sonido('impact-bass-1', w('Tampoco', mas=-0.02), vol=0.28)                   # el sello
sonido('whoosh-short', w('La gente', mas=-0.22), vol=0.22)
sonido('click', w('compra', 2, mas=-0.1), vol=0.45)                          # PRODUCTOS, tachado
sonido('impact-bass-2', w('Y quien', mas=-0.17), vol=0.34)                   # el golpe rojo final
