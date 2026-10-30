# Corto 2 · «La cuerda» (organización interna). Lo lee canales/businessformen/kit/montar.py: cortos/02-la-cuerda.
# Vertical, 48 s, en bucle: el final («el problema nunca fue la gente») vuelve al gancho («la peor fábrica de EE. UU.»)
# sobre la misma imagen. Un recurso distinto en cada plano y un golpe rojo, el de la lección. La cuerda es el motivo.
formato(1080, 1920, voz0=0.1, cola=0.45)
subtitulos()

escena('s01', 'fabrica', 0, modo='gancho',                        # R9: LA PEOR FÁBRICA DE EE. UU.
       titulo='<span class="l"><span class="bloque">La peor</span></span><span class="l">fábrica</span><span class="l">de EE. UU.</span>')
escena('s02', 'ausencias', w('Uno', mas=-0.18))                  # R3 + R5: 1 DE CADA 5; NO SE PRESENTABA
escena('s03', 'puerta', w('Y hubo', mas=-0.15))                  # R12: botellas dentro de las puertas
escena('s04', 'persiana', w('En mil', mas=-0.2), modo='cierra')  # R11: 1982; la persiana baja; CERRADA
escena('s05', 'persiana', w('Dos años', mas=-0.25), modo='abre') # R14: la persiana sube; TOYOTA AL MANDO
escena('s06', 'mismos', w('Y con los mismos', mas=-0.15))        # R15: vuelven las cinco figuras; +85 %
escena('s07', 'calidad', w('A los tres', mas=-0.05))              # R9 + R6: la fábrica limpia; CASI PERFECTA
escena('s08', 'pregunta', w('Qué cambió', mas=-0.25))            # R13: ¿QUÉ CAMBIÓ?; baja una cuerda
escena('s09', 'tirar', w('Cualquier', mas=-0.2))                 # R9: la cuerda de verdad; LÍNEA PARADA
escena('s10', 'ayuda', w('Y nadie', mas=-0.15))                  # R5: GRITOS tachado; LE AYUDABAN
escena('s11', 'copia', w('Yéneral Mótors', 2, mas=-0.2))         # R5 + R2: las cuerdas copiadas; LAS CORTARON
escena('s12', 'golpe', w('Puedes', mas=-0.3),                    # R1: la lección, con la firma BFM
       etq='', b1='Puedes copiar<br>una herramienta.', b2='No puedes copiar<br>la confianza.',
       conf={'etq': None, 'b1': {'palabra': 'Puedes', 'y': 330, 'tam': 86}, 'b2': {'palabra': 'No', 'n': 2, 'y': 640, 'tam': 86, 'sube': -24},
             'firma': True, 'firma_t': 3.2})
escena('s13', 'fabrica', w('El problema', mas=-0.2), modo='cierre',  # R15: la fábrica del principio
       titulo='<span class="l l1">El problema</span><span class="l l2">nunca fue</span><span class="l l3"><span class="bloque">la gente.</span></span>')
DURACION = w('gente', fin=True, mas=1.3)               # la última frase, 2 s en pantalla

sin_subtitulos(0, w('Y hubo', mas=-0.2))                          # el gancho y 1 DE CADA 5 ya lo escriben
sin_subtitulos(w('Y con los mismos', mas=-0.2), w('A los tres', mas=-0.25))
sin_subtitulos(w('Qué cambió', mas=-0.3), w('que viera', mas=-0.1))     # y CUALQUIER OPERARIO
sin_subtitulos(w('Y nadie', mas=-0.2), w('Puso', mas=-0.1))             # y GENERAL MOTORS QUISO COPIARLO
sin_subtitulos(w('pero a quien', mas=-0.2), DURACION)

# --- Música: tensa hasta la pregunta; silencio en «¿Qué cambió?»; otra, más luminosa, desde la cuerda.
musica('tension', 0, w('Qué cambió', mas=0.1), vol=0.27, fi=0.05, fo=0.35)
musica('cuerda', w('Una', 2, mas=-0.2), DURACION, vol=0.26, fi=0.5, fo=0.25,
       puntos=[(w('Puedes', mas=-0.5), 0.26), (w('Puedes', mas=-0.3), 0.08), (w('El problema', mas=-0.4), 0.08), (w('El problema', mas=-0.15), 0.28)])

# --- Efectos
sonido('impact-bass-1', w('peor', mas=-0.02), vol=0.22)                       # LA PEOR, quieta desde el fotograma 0
sonido('whoosh-short', w('Uno', mas=-0.22), vol=0.3)
sonido('pop', w('no', mas=0.05), vol=0.35)                                    # NO SE PRESENTABA
sonido('whoosh-short', w('Y hubo', mas=-0.18), vol=0.25)
sonido('1526', w('puertas', mas=-0.05), vol=0.45, dur=0.5, fo=0.1)            # la puerta del coche
sonido('1335', w('sonaran', mas=-0.05), vol=0.5, ini=0.15, dur=0.45, fo=0.1)  # las botellas que suenan
sonido('1335', w('sonaran', mas=0.12), vol=0.35, ini=0.15, dur=0.45, fo=0.1)
for t in (w('mil'), w('novecientos'), w('ochenta'), w('dos')):
    sonido('key-press', t - 0.03, vol=0.4)
sonido('2474', w('cerró', mas=-0.55), vol=0.9, ini=16.3, dur=1.7, fo=0.2)     # la persiana que baja
sonido('impact-bass-2', w('cerró', mas=0.3), vol=0.28)                         # CERRADA
sonido('2474', w('reabrieron', mas=-0.35), vol=0.4, ini=2.0, dur=1.1, fi=0.1, fo=0.3)
sonido('pop', w('mismos', mas=-0.1), vol=0.3)
sonido('whoosh', w('A los tres', mas=-0.25), vol=0.22)
sonido('whoosh-short', w('Qué cambió', mas=-0.28), vol=0.25)
sonido('1818', w('Una', 2, mas=-0.15), vol=0.55, dur=1.0, fo=0.3)              # baja la cuerda
sonido('1818', w('tirar', mas=-0.05), vol=0.7, dur=0.9, fo=0.3)                 # el tirón
sonido('1269', w('parar', mas=-0.02), vol=0.35, dur=1.4, fo=0.4)               # LÍNEA PARADA
sonido('click', w('gritaba', mas=-0.05), vol=0.45)
sonido('whoosh-short', w('ayudaban', mas=-0.3), vol=0.25)
sonido('whoosh', w('Yéneral Mótors', 2, mas=-0.22), vol=0.22)
sonido('typing', w('cuerdas', mas=-0.2), vol=0.25, dur=0.8, fo=0.2)
sonido('1818', w('tiraba', mas=-0.05), vol=0.55, dur=0.7, fo=0.2)
sonido('1247', w('cortaron', mas=-0.12), vol=0.55, ini=1.3, dur=1.2, fo=0.3)   # las cortan
sonido('impact-bass-2', w('Puedes', mas=-0.32), vol=0.34)                      # el golpe rojo
sonido('whoosh', w('El problema', mas=-0.25), vol=0.22)
