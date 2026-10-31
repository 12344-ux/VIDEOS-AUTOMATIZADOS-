# Corto 7 · «El sueldo» (gestión de equipos): Henry Ford pagó 5 $ al día en 1914 para dejar de perder gente. Lo lee
# canales/businessformen/kit/montar.py: cortos/07-el-sueldo. Vertical, unos 45 s, en bucle (el último plano es el primero:
# PAGÓ EL DOBLE · PARA AHORRAR). La idea, para que se entienda: la puerta giratoria (entran 50.000 para 14.000 puestos) y
# las dos barras (1913 frente a 1915). Imágenes a pantalla completa (el velo ligero del kit) y, por petición del usuario
# (31-oct), solo efectos fuertes con su causa en pantalla («como el rayo») y la música más baja.
formato(1080, 1920, voz0=0.1, cola=0.45)
subtitulos()

escena('s01', 'gancho', 0, foto='cadena', conf=dict(l1='Pagó el doble', l2='para ahorrar', camara=[1.1, 0, -30], modo='inicio'))
escena('s02', 'foto', w('cinco', mas=-0.15), foto='sobre', entrada='barrido',
       conf=dict(camara=[1.0, 1.1, 0, 0], textos=[
           dict(html='5 $<small>al día</small>', clase='cifra', x=80, y=300, en=['cinco', 1, -0.05], modo='grande'),
           dict(html='Más del doble', clase='sello', x=80, y=960, en=['doble', 1, -0.05], modo='sello')]))
escena('s03', 'foto', w('Parecía', mas=-0.15), foto='puerta', entrada='subida',
       conf=dict(camara=[1.0, 1.08, 0, 20], textos=[
           dict(html='¿Una locura?', clase='titular', x=80, y=300, en=['locura', 1, -0.1]),
           dict(html='Su gente se iba', clase='sello', x=80, y=960, en=['iba', 1, -0.05], modo='sello')]))
escena('s04', 'flujo', w('El año', mas=-0.15), modo='entra', entrada='barrido')
escena('s05', 'foto', w('A cada', mas=-0.15), foto='taller', entrada='subida',
       conf=dict(camara=[1.0, 1.1, 0, 0], textos=[
           dict(html='1 · Buscarla', clase='etiqueta', x=80, y=300, en=['buscarla', 1, -0.08]),
           dict(html='2 · Enseñarle', clase='etiqueta', x=80, y=390, en=['enseñarle', 1, -0.08]),
           dict(html='Y perderla', clase='sello', x=80, y=960, en=['marchar', 1, -0.05], modo='sello')]))
escena('s06', 'flujo', w('Con los', mas=-0.15), modo='quedo', entrada='barrido')
escena('s07', 'barras', w('Al año', mas=-0.15), entrada='subida')
escena('s08', 'foto', w('El propio', mas=-0.15), foto='cadena', entrada='barrido',
       conf=dict(camara=[1.15, 1.25, -40, 0], textos=[
           dict(html='Para Ford:', clase='titular', x=80, y=300, en=['propio', 1, -0.05]),
           dict(html='Un recorte<br>de costes', clase='sello', x=80, y=880, en=['recortes', 1, -0.05], modo='sello')]))
escena('s09', 'golpe', w('Lo más', mas=-0.15), entrada='cortina',
       etq='Lo más caro de un equipo', b1='No es<br>su sueldo.', b2='Es tener que<br>sustituirlo.',
       conf={'etq': {'palabra': 'lo', 'n': 3, 'grande': True}, 'b1': {'palabra': 'no', 'y': 380, 'tam': 130},
             'b2': {'palabra': 'es', 'n': 2, 'y': 680, 'tam': 130, 'sube': -24}, 'firma': True, 'firma_t': 3.4})
escena('s10', 'gancho', w('Por eso', mas=-0.15), foto='cadena',
       conf=dict(l1='Pagó el doble', l2='para ahorrar', modo='vuelta', en_l1=['pagó', 1, -0.05], en_l2=['pagó', 1, 0.3]))
DURACION = w('doble', 2, fin=True, mas=1.3)

sin_subtitulos(w('Lo más', mas=-0.2), DURACION)                  # la lección y el gancho: escritos en grande

# --- Música: un lecho bajo (17–20 LU por debajo de la voz); se calla en el golpe.
musica('lecho', 0, DURACION, vol=0.1, fi=0.05, fo=0.3,
       puntos=[(w('Lo más', mas=-0.45), 0.1), (w('Lo más', mas=-0.2), 0.0), (w('Por eso', mas=-0.3), 0.0), (w('Por eso', mas=0.1), 0.1)])

# --- Efectos: solo los que tienen su golpe en pantalla.
sonido('0193', w('cinco', mas=-0.02), vol=0.6, ini=0.05, dur=1.0, fo=0.3)            # las monedas caen sobre el banco
sonido('3321', w('iba', fin=True, mas=0.05), vol=0.35, ini=0.05, dur=1.7, fo=0.6)   # el silbato de la fábrica: se van
sonido('impact-bass-2', w('Lo más', mas=-0.15), vol=0.08)                             # el golpe rojo
