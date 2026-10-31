# Corto 2 de supervivencia · «60 horas bajo el mar» (Harrison Okene, Nigeria, 2013). Lo monta el kit de BusinessForMen
# con la marca del canal:
#   python3 canales/businessformen/kit/montar.py --canal canales/supervivencia cortos/02-okene
# Vertical, unos 69 s, en bucle: el último plano («el cocinero que pasó sesenta horas en el fondo del mar») es el primero
# (60 HORAS · EN EL FONDO DEL MAR). El secreto tachado: «cómo lo encontraron» (segundo 8), que se lee en el 47 («lo daban
# por muerto»); el golpe, en el 52 («y la mano lo agarra»). Retención: ../../../RETENCION.md.
# Sonido (ver ../../CANAL.md): un ambiente por mundo (la superficie en tormenta y, bajo el agua, el mar apagado), los
# golpes del martillo y un solo impacto; todo medido con audio/revisar_mezcla.py antes de renderizar.
import json
import os

formato(1080, 1920, voz0=0.1, cola=0.7)
subtitulos()
M = json.load(open(os.path.join(AQUI, 'recursos', 'mapa.json')))

FICHA = dict(cab='Lo más increíble', linea='Cómo lo encontraron:', tapada='Lo daban<br>por muerto')
escena('s01', 'gancho', 0, foto='aire',
       conf=dict(cifra='60', unidad='horas', linea='En el fondo del mar', camara=[1.12, 0, -50], modo='inicio',
                 sonda=dict(en=['treinta', 1, -0.05], prof=30)))
escena('s02', 'ficha', w('Y lo más', mas=-0.12), fondo='aire',
       conf=dict(FICHA, modo='oculta', en=['increíble', 1, -0.35], escribe=[['cómo', 1, -0.05], ['encontraron', 1, 0.05, 'fin']],
                 barra=['encontraron', 1, 0.1, 'fin'], late=['encontraron', 1, 0.25, 'fin']))
escena('s03', 'mapa', w('Nigeria', mas=-0.12), nigeria=M['nigeria'], vecinos=M['vecinos'], naufragio=M['naufragio'])
escena('s04', 'foto', w('Járison', mas=-0.12), foto='remolcador',
       conf=dict(camara=[1.05, 1.15, 0, 20], techo=True, textos=[
           dict(html='Harrison Okene · 29 años', clase='etiqueta', x=80, y=300, en=['Járison', 1, 0.0]),
           dict(html='Cocinero', clase='diario', x=80, y=400, en=['cocinero', 1, -0.05]),
           dict(html='12 a bordo', clase='sello', x=80, y=960, en=['cocinero', 1, 0.3], modo='sello')]))
escena('s05', 'corte', w('Una madrugada', mas=-0.12), modo='vuelco')
escena('s06', 'corte', w('A oscuras', mas=-0.12), modo='bolsa')
escena('s07', 'puntos', w('Los otros', mas=-0.12), fondo='fondo',
       conf=dict(n=12, cols=6, tam=96, hueco=40, x=86, y=640, cifra=dict(html='12<small>a bordo</small>', x=80, y=300),
                 aparecen=[0.05, 0.55], apaga=dict(en=['once', 1, -0.05], menos=[8])))
escena('s08', 'foto', w('Lleva', mas=-0.12), foto='aire',
       conf=dict(camara=[1.18, 1.26, 0, -30], brillo=0.75, agua=dict(en=['agua', 2, -0.1], hasta=['sube', 1, 0.9, 'fin'], y=980),
                 textos=[dict(html='Inventario', clase='diario', x=80, y=236, en=0.05, modo='aparece'),
                         dict(html='· Calzoncillos', clase='diario', x=80, y=330, en=['calzoncillos', 1, -0.1], modo='escribe'),
                         dict(html='· Coca-Cola', clase='diario', x=80, y=410, en=['Coca-Cola', 1, -0.1], modo='escribe')]))
escena('s09', 'foto', w('Pasa un', mas=-0.12), foto='aire',
       conf=dict(camara=[1.3, 1.36, 0, -40], brillo=0.45,
                 cuenta=dict(etiqueta='Hora', x=80, y=300, pasos=[[1, 0.0], [24, ['día', 1, -0.05]], [48, ['otro', 1, -0.05]]])))
escena('s10', 'foto', w('Oye', mas=-0.12), foto='martillo',
       conf=dict(camara=[1.05, 1.14, 0, 0], textos=[
           dict(html='Toc', clase='golpe', x=120, y=560, en=['Golpea', 1, 0.0], modo='sello', sale=['aleja', 1, 0.0]),
           dict(html='Toc', clase='golpe', x=380, y=640, en=['Golpea', 1, 0.45], modo='sello', sale=['aleja', 1, 0.08]),
           dict(html='Toc', clase='golpe', x=640, y=720, en=['Golpea', 1, 0.9], modo='sello', sale=['aleja', 1, 0.16])]))
escena('s11', 'foto', w('Hasta que', mas=-0.12), foto='linterna',
       conf=dict(camara=[1.0, 1.1, 0, 0], brillo=0.85, haz=dict(en=['linterna', 1, -0.3]),
                 textos=[dict(html='Buzos', clase='etiqueta', x=80, y=300, en=['buzos', 1, -0.05])]))
escena('s12', 'ficha', w('Pero', 2, mas=-0.12), fondo='linterna',
       conf=dict(FICHA, modo='revela', en=0.05, fondo_en=0.0, quita=['cuerpos', 1, 0.0]))
escena('s13', 'foto', w('Uno', mas=-0.12), foto='mano',
       conf=dict(camara=[1.0, 1.22, 0, 0], destellos=[['agarra', 1, -0.02]], temblores=[['agarra', 1, 0.0]],
                 textos=[dict(html='Está vivo', clase='sello', x=80, y=960, en=['vivo', 1, -0.05], modo='sello')]))
escena('s14', 'corte', w('Pero', 3, mas=-0.12), modo='camara')
escena('s15', 'puntos', w('De doce', mas=-0.12), fondo='fondo',
       conf=dict(n=12, cols=6, tam=96, hueco=40, x=86, y=640, cifra=dict(html='12<small>a bordo</small>', x=80, y=300),
                 aparecen=[0.0, 0.3], apaga=dict(en=['uno', 2, -0.1], menos=[8]), sello=dict(html='Volvió uno', en=['uno', 2, 0.05], x=80, y=980)))
escena('s16', 'gancho', w('cocinero', 2, mas=-0.25), foto='aire',
       conf=dict(cifra='60', unidad='horas', linea='En el fondo del mar', modo='vuelta', en_cifra=['sesenta', 2, -0.05],
                 en_linea=['sesenta', 2, 0.35]))
DURACION = w('mar', 3, fin=True, mas=0.9)

# Subtítulos, salvo donde la pantalla ya escribe en grande lo que dice la voz.
sin_subtitulos(0, w('A treinta', mas=-0.12))                             # 60 HORAS · EN EL FONDO DEL MAR
sin_subtitulos(w('Está vivo', mas=-0.12), w('Pero', 3, mas=-0.12))       # ESTÁ VIVO
sin_subtitulos(w('volvió', mas=-0.12), DURACION)                         # VOLVIÓ UNO, y vuelve el gancho

# --- Música: violines agudos y piano (pieza 2: 10 % bajo 150 Hz), siempre por debajo de la voz; se retira para el
# golpe de la mano y vuelve con el rescate.
musica('lecho', 0, DURACION, vol=0.16, fi=0.05, fo=0.3,
       puntos=[(w('Y el barco', mas=-0.2), 0.16), (w('vuelca', mas=0.2), 0.2), (w('A oscuras', mas=-0.2), 0.14),
               (w('Uno ve', mas=-0.2), 0.14), (w('agarra', mas=-0.3), 0.04), (w('vivo', mas=0.1), 0.2),
               (w('Pero', 3, mas=0.2), 0.15), (w('cocinero', 2, mas=0.0), 0.16)])

# --- Sonido: ambientes de fondo bajos y continuos, y golpes solo donde algo golpea en pantalla.
sonido('bajoagua', 0, vol=0.4, ini=0.0, dur=w('Nigeria', mas=0.4), fi=0.0, fo=0.8)                  # bajo el agua (el bucle no empieza en silencio)
sonido('2570', w('Nigeria', mas=-0.3), vol=0.09, ini=0.5, dur=w('hunde', mas=0.3) - w('Nigeria', mas=-0.3), fi=0.6, fo=1.2)  # el mar en la superficie
sonido('0154', w('Una madrugada', mas=-0.3), vol=0.05, ini=4.0, dur=w('hunde', mas=0.3) - w('Una madrugada', mas=-0.3), fi=0.8, fo=1.0)  # el viento
sonido('gemido', w('vuelca', mas=-0.25), vol=0.12, ini=0.5, dur=2.4, fi=0.1, fo=0.7)                # el casco cruje al volcar
sonido('1521', w('vuelca', mas=0.25), vol=0.1, ini=0.0, dur=2.2, fo=0.8)                            # el barco golpea el agua
sonido('bajoagua', w('hunde', mas=-0.2), vol=0.17, ini=12.0, dur=w('Pero', 3, mas=0.6) - w('hunde', mas=-0.2), fi=1.2, fo=1.0)  # ya bajo el agua
for k, ini in enumerate((1.15, 2.2, 4.25)):                                                          # TOC · TOC · TOC
    sonido('golpecasco', w('Golpea', mas=0.45 * k), vol=0.42, ini=ini, dur=0.7, fo=0.25)
sonido('impact-bass-1', w('agarra', fin=True, mas=0.05), vol=0.02)                                   # la mano (en la pausa)
sonido('bajoagua', w('cocinero', 2, mas=-0.5), vol=0.4, ini=40.0, dur=DURACION - w('cocinero', 2, mas=-0.5), fi=0.8, fo=0.0)  # vuelve el principio
