# Corto 8 · «La fórmula» (marca): en 1985 Coca-Cola cambió su fórmula, ganó las catas a ciegas y tuvo que volver atrás en
# 79 días. Lo lee canales/businessformen/kit/montar.py: cortos/08-la-formula. Vertical, unos 44 s, en bucle (GANÓ 200.000
# CATAS · Y FUE UN DESASTRE). La idea, para que se entienda: los dos vasos de la cata (gana la nueva) y los 79 días, uno a
# uno. Imágenes a pantalla completa; solo efectos fuertes con su causa en pantalla y la música baja (31-oct).
formato(1080, 1920, voz0=0.1, cola=0.45)
subtitulos()

escena('s01', 'gancho', 0, foto='lata', conf=dict(l1='Ganó 200.000<br>catas', l2='y fue un desastre', camara=[1.12, 0, -20], modo='inicio'))
escena('s02', 'catas', w('La nueva', mas=-0.15), entrada='barrido')
escena('s03', 'foto', w('Pepsi', mas=-0.15), foto='cata', entrada='subida',
       conf=dict(camara=[1.0, 1.1, 0, 0], textos=[
           dict(html='Pepsi gana clientes', clase='etiqueta', x=80, y=300, en=['Pepsi', 1, -0.05]),
           dict(html='Gana lo más dulce', clase='sello', x=80, y=960, en=['dulce', 1, -0.05], modo='sello')]))
escena('s04', 'foto', w('Así que', mas=-0.15), foto='lata', entrada='barrido',
       conf=dict(camara=[1.2, 1.32, 0, 30], textos=[
           dict(html='Una más dulce', clase='titular', x=80, y=300, en=['dulce', 2, -0.1]),
           dict(html='✓ Ganaba', clase='sello', x=80, y=960, en=['ganaba', 1, -0.05], modo='sello')]))
escena('s05', 'foto', w('La lanzó', mas=-0.15), foto='telefonos', entrada='subida',
       conf=dict(camara=[1.0, 1.1, 0, 0], textos=[
           dict(html='Abril de 1985', clase='etiqueta', x=80, y=300, en=['abril', 1, -0.05]),
           dict(html='5.000', clase='cifra', x=80, y=420, en=['cinco', 2, -0.05], modo='grande'),
           dict(html='llamadas de queja al día', clase='nota', x=86, y=640, en=['llamadas', 1, -0.05])]))
escena('s06', 'foto', w('La gente no', mas=-0.15), foto='estante', entrada='barrido',
       conf=dict(camara=[1.0, 1.08, 0, 0], textos=[
           dict(html='No querían<br>una mejor.', clase='titular', x=80, y=300, en=['quería', 1, -0.05]),
           dict(html='Querían la suya', clase='sello', x=80, y=960, en=['suya', 1, -0.08], modo='sello')]))
escena('s07', 'calendario', w('Setenta', mas=-0.15), entrada='subida')
escena('s08', 'golpe', w('Tus clientes', mas=-0.15), entrada='cortina',
       etq='Tus clientes', b1='No compran solo<br>lo que vendes.', b2='Compran lo que<br>significa<br>para ellos.',
       conf={'etq': {'palabra': 'tus', 'grande': True}, 'b1': {'palabra': 'no', 'n': 2, 'y': 360, 'tam': 86},
             'b2': {'palabra': 'compran', 'n': 2, 'y': 640, 'tam': 86, 'sube': -24}, 'firma': True, 'firma_t': 3.9})
escena('s09', 'gancho', w('Por eso', mas=-0.15), foto='lata',
       conf=dict(l1='Ganó 200.000<br>catas', l2='y fue un desastre', modo='vuelta', en_l1=['ganó', 1, -0.05], en_l2=['ganó', 1, 0.4]))
DURACION = w('perdió', fin=True, mas=1.3)

sin_subtitulos(w('Tus clientes', mas=-0.2), DURACION)            # la lección y el gancho: escritos en grande

musica('lecho', 0, DURACION, vol=0.09, fi=0.05, fo=0.3,
       puntos=[(w('Tus clientes', mas=-0.45), 0.1), (w('Tus clientes', mas=-0.2), 0.0), (w('Por eso', mas=-0.3), 0.0), (w('Por eso', mas=0.1), 0.1)])

sonido('0253', w('llamadas', mas=-0.1), vol=0.22, ini=0.0, dur=1.4, fo=0.2)           # suenan los teléfonos
sonido('0253', w('llamadas', mas=0.55), vol=0.15, ini=0.3, dur=1.1, fo=0.3)
sonido('1932', w('siempre', fin=True, mas=-0.1), vol=0.4, ini=0.25, dur=0.9, fo=0.3)   # se abre la de siempre, en la pausa
