# Corto 11 de supervivencia · «La cueva» (los doce niños de los Jabalíes Salvajes y su entrenador, cueva de Tham Luang,
# norte de Tailandia, del 23 de junio al 10 de julio de 2018). Lo monta el kit de BusinessForMen con la marca del canal:
#   python3 canales/businessformen/kit/montar.py --canal canales/supervivencia cortos/11-tham-luang
# Vertical, unos 82 s, en bucle: el último plano («Dieciocho días en una cueva») es el primero (18 DÍAS · EN UNA CUEVA). El
# secreto tachado: «cómo los sacaron» (segundo 5), que se lee al 75 % («Sacarlos dormidos»). La cueva, en corte y dibujada
# (escenas/cueva.html): se inunda, huyen hasta la roca, el camino de salida y el rescate uno a uno. Los niños eran menores:
# siempre de espaldas y de lejos. Retención: ../../../RETENCION.md.
# Sonido (ver ../../CANAL.md, la regla desde el corto 3): solo efectos fuertes con su golpe en pantalla y sin ambientes de
# fondo: el trueno de la tormenta (con su destello), el agua que entra al inundarse, los buzos que salen del agua y la
# lluvia que vuelve. La música, 16–20 LU bajo la voz. Medido con audio/revisar_mezcla.py antes de renderizar.
formato(1080, 1920, voz0=0.1, cola=0.7)
subtitulos()

FICHA = dict(cab='Cómo los sacaron', linea='El plan:', tapada='Sacarlos<br>dormidos')
GANCHO = dict(cifra='18', unidad='días', linea='En una cueva')
escena('s01', 'gancho', 0, foto='roca', conf=dict(GANCHO, camara=[1.1, 0, 30], modo='inicio'))   # «Dieciocho» n=1 aquí
escena('s02', 'ficha', w('Pero', 1, mas=-0.12), fondo='roca',
       conf=dict(FICHA, modo='oculta', en=0.05, escribe=[['plan', 1, -0.05], ['locura', 1, 0.0, 'fin']],
                 barra=['locura', 1, -0.1], late=['locura', 1, -0.05]))
escena('s03', 'foto', w('Veintitrés', mas=-0.12), foto='entrada',
       conf=dict(camara=[1.04, 1.14, 0, 40], techo=True, textos=[
           dict(html='23 JUN 2018', clase='diario', x=80, y=236, en=['Veintitrés', 1, -0.05], modo='escribe', duracion=1.3),
           dict(html='Norte de Tailandia', clase='etiqueta', x=80, y=330, en=['Norte', 1, -0.05]),
           dict(html='Cueva de Tham Luang', clase='etiqueta', x=80, y=420, en=['Tam', 1, -0.05])]))
escena('s04', 'puntos', w('Los niños tienen', mas=-0.12), fondo='entrada',
       conf=dict(n=12, cols=6, tam=64, hueco=30, x=144, y=640, cifra=dict(html='12 niños<small>de 11 a 16 años</small>', x=80, y=300),
                 aparecen=[['niños', 2, -0.1], ['dieciséis', 1, 0.0]],
                 sello=dict(html='Sin comida', en=['comida', 1, -0.05], x=80, y=960)))
escena('s05', 'cueva', w('Afuera', 1, mas=-0.12), modo='inunda')
escena('s06', 'foto', w('En la entrada', mas=-0.12), foto='bicicletas',
       conf=dict(camara=[1.0, 1.12, 0, 30], lluvia=True, destellos=[0.05]))
escena('s07', 'cueva', w('Huyen', mas=-0.12), modo='adentro')
escena('s08', 'foto', w('Beben', mas=-0.12), foto='gotas',
       conf=dict(camara=[1.0, 1.14, 0, -20], techo=True,
                 cuenta=dict(etiqueta='DÍA', x=80, y=176, pasos=[[2, 0.0], [3, ['gotea', 1, -0.05]]])))
escena('s09', 'foto', w('Su entrenador', 2, mas=-0.12), foto='meditar',
       conf=dict(camara=[1.0, 1.1, 0, 30], techo=True,
                 cuenta=dict(etiqueta='DÍA', x=80, y=176, pasos=[[4, 0.0], [5, ['enseña', 1, -0.05]]]),
                 textos=[dict(html='Ekkapol · 25 años', clase='etiqueta', x=80, y=520, en=['Ekapol', 1, -0.05]),
                         dict(html='Exmonje budista', clase='etiqueta', x=80, y=610, en=['monje', 1, -0.05])]))
escena('s10', 'foto', w('Afuera', 2, mas=-0.12), foto='rescatistas',
       conf=dict(camara=[1.0, 1.12, 0, 40], techo=True,
                 cuenta=dict(etiqueta='DÍA', x=80, y=176, pasos=[[6, 0.0], [7, ['buscan', 1, 0.0]], [8, ['Pasan', 1, -0.05]], [9, ['nueve', 1, -0.05]]]),
                 textos=[dict(html='Más de 10.000', clase='golpe', x=80, y=540, en=['miles', 1, -0.1]),
                         dict(html='¿Vivos?', clase='sello', x=80, y=960, en=['vivos', 2, -0.05], modo='sello')]))
escena('s11', 'foto', w('El día diez', mas=-0.12), foto='buzos',
       conf=dict(camara=[1.0, 1.16, 0, 0], techo=True,
                 cuenta=dict(etiqueta='DÍA', x=80, y=176, pasos=[[10, 0.0]]),
                 textos=[dict(html='Buzos británicos', clase='etiqueta', x=80, y=520, en=['británicos', 1, -0.05]),
                         dict(html='«¿Cuántos son?»', clase='diario', x=80, y=610, en=['Cuántos', 1, -0.1], modo='escribe', duracion=0.9),
                         dict(html='13', clase='grande', x=80, y=700, en=['Trece', 1, -0.05], modo='grande')]))
escena('s12', 'foto', w('Están vivos', 2, mas=-0.12), foto='tunel',
       conf=dict(camara=[1.0, 1.14, 0, 20], techo=True, textos=[
           dict(html='Imposible', clase='sello', x=80, y=960, en=['imposible', 1, -0.05], modo='sello', sale=['Hay', 1, -0.2]),
           dict(html='Túneles inundados', clase='etiqueta', x=80, y=330, en=['túneles', 2, -0.05]),
           dict(html='A oscuras', clase='etiqueta', x=80, y=420, en=['oscuras', 1, -0.05]),
           dict(html='No saben bucear', clase='etiqueta', x=80, y=510, en=['bucear', 2, -0.05])]))
escena('s13', 'cueva', w('El oxígeno', mas=-0.12), modo='salida')
escena('s14', 'foto', w('Un exbuzo', mas=-0.12), foto='tanques',
       conf=dict(camara=[1.0, 1.08, 0, 20], techo=True, brillo=0.8, textos=[
           dict(html='6 JUL 2018', clase='diario', x=80, y=236, en=['exbuzo', 1, -0.05], modo='escribe', duracion=1.0),
           dict(html='Saman Kunan', clase='etiqueta', x=80, y=330, en=['Saman', 1, -0.05]),
           dict(html='Exbuzo de la Armada', clase='etiqueta', x=80, y=420, en=['Armada', 1, -0.05])]))
escena('s15', 'ficha', w('Entonces', mas=-0.12), fondo='dormido',
       conf=dict(FICHA, modo='revela', en=0.05, fondo_en=0.0, quita=['Sacarlos', 3, -0.05]))
escena('s16', 'foto', w('Un anestesista', mas=-0.12), foto='dormido',
       conf=dict(camara=[1.0, 1.12, 0, 30], techo=True, textos=[
           dict(html='Anestesista australiano', clase='etiqueta', x=80, y=330, en=['anestesista', 1, -0.05]),
           dict(html='Uno a uno', clase='etiqueta', x=80, y=420, en=['uno', 2, -0.05])]))
escena('s17', 'cueva', w('Y los buzos', mas=-0.12), modo='rescate')
escena('s18', 'puntos', w('Trece de trece', mas=-0.12), fondo='salida',
       conf=dict(n=13, cols=7, tam=64, hueco=30, x=120, y=640, cifra=dict(html='13<small>de 13</small>', x=80, y=300),
                 aparecen=[0.0, 0.4], sello=dict(html='Todos vivos', en=['trece', 4, 0.1, 'fin'], x=80, y=960)))
escena('s19', 'gancho', w('Dieciocho', 3, mas=-0.12), foto='roca',          # la 2.ª es la fecha («dos mil dieciocho»)
       conf=dict(GANCHO, modo='vuelta', en_cifra=['dieciocho', 3, -0.05], en_linea=['cueva', 6, 0.0]))
DURACION = w('cueva', 6, fin=True, mas=0.9)

# Subtítulos, salvo donde la pantalla ya escribe en grande lo que dice la voz.
sin_subtitulos(w('Cuántos', mas=-0.1), w('Están vivos', 2, mas=-0.12))      # «¿CUÁNTOS SON?» · 13
sin_subtitulos(w('Sacarlos dormidos', mas=-0.1), w('Un anestesista', mas=-0.12))   # el plan, revelado en la ficha
sin_subtitulos(w('Trece de trece', mas=-0.1), w('Dieciocho', 3, mas=-0.12))  # 13 DE 13 · TODOS VIVOS
sin_subtitulos(w('Dieciocho', 3, mas=-0.12), DURACION)                         # vuelve el gancho

# --- Música: 16–20 LU bajo la voz (CANAL.md); se retira para el plan revelado y vuelve con el rescate.
musica('lecho', 0, DURACION, vol=0.09, fi=0.05, fo=0.1,
       puntos=[(w('Entonces', mas=-0.3), 0.09), (w('Sacarlos dormidos', mas=-0.2), 0.05), (w('Un anestesista', mas=-0.1), 0.09)])

# --- Efectos: solo los fuertes, con su golpe en pantalla (se ajustan con audio/revisar_mezcla.py).
sonido('3132', w('inunda', mas=-0.15), vol=0.2, ini=2.0, dur=2.2, fi=0.3, fo=0.9)             # el agua entra y llena el sifón
sonido('3113', w('En la entrada', mas=-0.2), vol=0.18, ini=1.0, dur=2.6, fo=1.2)               # el trueno, con su destello
sonido('1529', w('salen', 2, mas=0.05), vol=0.18, ini=0.0, dur=1.2, fo=0.4)                    # los buzos salen del agua
sonido('3114', w('lluvias', mas=-0.5), vol=0.15, ini=0.75, dur=2.4, fo=1.2)                       # vuelve la tormenta, lejos
