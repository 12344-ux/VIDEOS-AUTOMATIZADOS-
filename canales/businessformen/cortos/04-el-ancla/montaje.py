# Corto 4 · «El ancla» (precios y negociación). Lo lee canales/businessformen/kit/montar.py: cortos/04-el-ancla.
# Vertical, 52 s, en bucle. La idea, para que se entienda: el primer número que ves es la regla con la que mides el
# siguiente. El 999 se queda siempre a la vista (tachado, en la regla) para que el 499 se lea contra él.
# Edición: 2.5D en el auditorio (público delante, pantalla detrás, a distinta velocidad), el precio dentro de la
# pantalla, transiciones con causa (se entra por la pantalla; la cortina roja de la marca; barridos) y un golpe rojo.
formato(1080, 1920, voz0=0.1, cola=0.45)
subtitulos()

PANTALLA = dict(px=69, py=458, pw=960, ph=622, pt=290, origen='50% 40%')  # la pantalla del auditorio, medida en la imagen
escena('s01', 'escenario', 0, modo='gancho', precio='999 $', **PANTALLA)            # R9 2.5D: UN PRECIO QUE NUNCA EXISTIÓ
escena('s02', 'precio', w('esto', mas=-0.15), entrada={'tipo': 'iris', 'x': 540, 'y': 770})  # R3: 999 → 499; el ancla tachada
escena('s03', 'escenario', w('La sala', mas=-0.3), modo='aplauso', precio='499 $', entrada='cortina', **PANTALLA)  # ¿CARO? → GANGA
escena('s04', 'ancla', w('Se llama', mas=-0.25), entrada='barrido')                 # R2 + R5: ANCLAJE; la regla
escena('s05', 'azar', w('Funciona', mas=-0.15))                                      # R2: HASTA CON UN NÚMERO AL AZAR
escena('s06', 'ruleta', w('En un experimento', mas=-0.2), entrada='subida')         # R5: la ruleta para en 10 y en 65
escena('s07', 'resultados', w('Con el diez', mas=-0.2), entrada='barrido')         # R6: 25 % y 45 %, a escala
escena('s08', 'consejo', w('Así que', mas=-0.25), entrada='cortina')               # R5: las dos reglas
escena('s09', 'golpe', w('El primer número manda', mas=-0.2),                       # R1: la lección, con la firma BFM
       etq='', b1='El primer<br>número manda.', b2='',
       conf={'etq': None, 'b1': {'palabra': 'El', 'n': 9, 'y': 520, 'tam': 150}, 'b2': None, 'firma': True, 'firma_t': 0.45})
DURACION = w('manda', fin=True, mas=1.3)

sin_subtitulos(0, w('Antes', mas=-0.2))                          # el gancho ya lo escribe
sin_subtitulos(w('esto', mas=-0.2), w('La sala', mas=-0.35))     # 999 → 499, en grande
sin_subtitulos(w('Funciona', mas=-0.2), w('En un experimento', mas=-0.25))
sin_subtitulos(w('Con el diez', mas=-0.25), DURACION)            # resultados, reglas y golpe: ya escritos

# --- Música: un lecho sin entrada; se calla en el golpe.
musica('lecho', 0, DURACION, vol=0.27, fi=0.05, fo=0.3,
       puntos=[(w('El primer número manda', mas=-0.45), 0.27), (w('El primer número manda', mas=-0.2), 0.0)])

# --- Efectos
sonido('whoosh-cinematic', w('Antes', mas=-0.1), vol=0.18, dur=2.5, fi=0.4, fo=0.8)   # la cámara avanza
sonido('whoosh-short', w('esto', mas=-0.2), vol=0.32)                                  # se entra por la pantalla
sonido('impact-bass-1', w('novecientos', mas=-0.05), vol=0.24)
sonido('whoosh', w('cayó', mas=-0.3), vol=0.25)                                        # el 999 sube y se tacha
sonido('pop', w('cuatrocientos', mas=0.2), vol=0.38)                                   # cae el 499
sonido('2363', w('La sala', mas=-0.35), vol=0.42, ini=0.4, dur=3.4, fo=1.2)            # la sala aplaude
sonido('click', w('parecía', 2, mas=-0.1), vol=0.4)                                    # ¿CARO?, tachado
sonido('whoosh-short', w('Se llama', mas=-0.3), vol=0.25)
sonido('impact-bass-2', w('Se llama', mas=0.25), vol=0.22)                             # cae el ancla
sonido('pop', w('medir', mas=-0.05), vol=0.3)
for t in [w('Funciona', mas=-0.1) + 0.12 * k for k in range(0, 18, 3)]:
    sonido('key-press', t, vol=0.18)                                                   # las cifras que cambian
sonido('whoosh-short', w('En un experimento', mas=-0.25), vol=0.25)
# La ruleta: un trinquete que se frena (clics cada vez más separados) hasta el 10, y otro giro corto hasta el 65.
t0, t1 = w('En un experimento', mas=0.3), w('diez')
for k in range(16):
    sonido('click-soft', t0 + (t1 - t0) * (1 - (1 - k / 15) ** 0.5) ** 1.6, vol=0.28)
sonido('pop', w('diez', mas=0.02), vol=0.3)
for k in range(6):
    sonido('click-soft', w('o', mas=-0.05) + 0.11 * k ** 1.25, vol=0.26)
sonido('pop', w('sesenta', mas=0.2), vol=0.3)
sonido('whoosh-short', w('Con el diez', mas=-0.25), vol=0.25)
sonido('whoosh-short', w('Así que', mas=-0.3), vol=0.25)
sonido('impact-bass-2', w('El primer número manda', mas=-0.22), vol=0.34, dur=2.3, fo=0.4)  # el golpe rojo
