# Corto 9 · «La cámara» (estrategia): Kodak construyó la primera cámara digital en 1975, la dejó en el laboratorio para
# proteger el carrete y quebró en 2012. Lo lee canales/businessformen/kit/montar.py: cortos/09-la-camara. Vertical, unos
# 44 s, en bucle (KODAK INVENTÓ ESTO · EN 1975, sobre el prototipo). La idea, para que se entienda: la ficha de 1975 (una
# foto de 10.000 píxeles que tarda 23 s) y las dos curvas que se cruzan. Imágenes a pantalla completa; solo efectos
# fuertes con su causa en pantalla y la música baja (31-oct).
formato(1080, 1920, voz0=0.1, cola=0.45)
subtitulos()

escena('s01', 'gancho', 0, foto='prototipo',
       conf=dict(l1='Kodak inventó<br>esto', l2='en 1975', tam1=104, camara=[1.12, 0, -20], modo='inicio', destello=['digital', 1, 0.05, 'fin']))
escena('s02', 'pixeles', w('Pesaba', mas=-0.15), entrada='barrido')
escena('s03', 'foto', w('Kódak la', mas=-0.15), foto='laboratorio', entrada='subida',
       conf=dict(camara=[1.0, 1.08, 0, 0], textos=[dict(html='Proyecto de laboratorio', clase='etiqueta', x=80, y=300, en=['laboratorio', 1, -0.1])]))
escena('s04', 'foto', w('Por qué', mas=-0.15), foto='carretes', entrada='barrido',
       conf=dict(camara=[1.0, 1.1, 0, 0], textos=[
           dict(html='Cada carrete: $', clase='etiqueta', x=80, y=300, en=['carrete', 1, -0.08]),
           dict(html='Cada revelado: $', clase='etiqueta', x=80, y=390, en=['revelado', 1, -0.08])]))
escena('s05', 'foto', w('Una cámara', mas=-0.15), foto='prototipo', entrada='subida',
       conf=dict(camara=[1.2, 1.3, 0, 20], brillo=0.75, textos=[
           dict(html='Sin carrete', clase='titular', x=80, y=300, en=['sin', 1, -0.05]),
           dict(html='Una amenaza', clase='sello', x=80, y=960, en=['amenaza', 1, -0.05], modo='sello')]))
escena('s06', 'curvas', w('Años', mas=-0.15), entrada='barrido')
escena('s07', 'foto', w('Y en dos', mas=-0.15), foto='fabrica', entrada='subida',
       conf=dict(camara=[1.0, 1.08, 0, 0], textos=[dict(html='Quiebra · 2012', clase='sello', x=80, y=960, en=['quiebra', 1, 0.12, 'fin'], modo='sello')]))
escena('s08', 'foto', w('Había', mas=-0.15), foto='prototipo', entrada='barrido',
       conf=dict(camara=[1.0, 1.06, 0, 0], textos=[
           dict(html='Inventó<br>el futuro', clase='titular', x=80, y=300, en=['inventado', 1, -0.05]),
           dict(html='Y lo dejó pasar', clase='sello', x=80, y=960, en=['pasar', 1, -0.05], modo='sello')]))
escena('s09', 'golpe', w('Si no', mas=-0.45), entrada='cortina',
       etq='Si no cambias tu negocio,', b1='Otro lo<br>cambiará', b2='por ti.',
       conf={'etq': {'palabra': 'si', 'grande': True}, 'b1': {'palabra': 'otro', 'y': 380, 'tam': 130},
             'b2': {'palabra': 'por', 'n': 2, 'y': 680, 'tam': 150, 'sube': -24}, 'firma': True, 'firma_t': 2.8})
escena('s10', 'gancho', w('Y todo', mas=-0.15), foto='prototipo',
       conf=dict(l1='Kodak inventó<br>esto', l2='en 1975', tam1=104, modo='vuelta', en_l1=['todo', 1, -0.05], en_l2=['todo', 1, 0.3]))
DURACION = w('esto', fin=True, mas=1.4)

sin_subtitulos(w('Si no', mas=-0.45), DURACION)                   # la lección y el gancho: escritos en grande

musica('lecho', 0, DURACION, vol=0.1, fi=0.05, fo=0.3,
       puntos=[(w('Si no', mas=-0.45), 0.1), (w('Si no', mas=-0.2), 0.0), (w('Y todo', mas=-0.3), 0.0), (w('Y todo', mas=0.1), 0.1)])

sonido('2821', w('digital', fin=True, mas=0.0), vol=0.6, ini=0.0, dur=0.4)           # el disparo (con el destello)
sonido('2819', w('carrete', mas=-0.25), vol=0.5, ini=0.0, dur=0.9)                    # el arrastre del carrete
sonido('1501', w('quiebra', fin=True, mas=0.05), vol=0.33, ini=0.05, dur=0.8, fo=0.3)  # el portazo, con el sello (en la pausa)
sonido('impact-bass-2', w('Si no', mas=-0.45), vol=0.02)                              # el golpe rojo, con la cortina (en la pausa)
