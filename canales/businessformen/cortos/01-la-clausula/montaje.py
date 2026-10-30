# Corto 1 · «La cláusula» (negociación). Lo lee canales/businessformen/kit/montar.py: cortos/01-la-clausula.
# Vertical, 48 s, en bucle: el final («IBM solo miró el precio») vuelve al gancho («IBM firmó esto») sobre el mismo
# contrato. Un recurso distinto en cada plano (EDICION.md) y un golpe rojo, el de la lección.
formato(1080, 1920, voz0=0.1, cola=0.45)
subtitulos()

escena('s01', 'contrato', 0, modo='gancho',                       # R7 + R1: IBM FIRMÓ ESTO; la firma; el sello rojo
       titulo='<span class="l">IBM firmó</span><span class="l">esto.</span>')
escena('s02', 'edad', w('Con', mas=-0.15))                       # R3: 25 años
escena('s03', 'pc', w('Mil', mas=-0.15), origen='50% 30%')       # R9 + R3: 1980; SISTEMA OPERATIVO ?
escena('s04', 'cero', w('Bil', mas=-0.15))                       # R2 → R3: LO PROMETE; 0
escena('s05', 'recibo', w('Así', mas=-0.15))                     # R8: el recibo de 75.000 $
escena('s06', 'clausula', w('en el contrato', mas=-0.3))         # R7 + R12: la cláusula subrayada con la voz
escena('s07', 'firma', w('I Be Eme', 4, mas=-0.15))              # R12 → R9: FIRMADO; EL NEGOCIO ES LA MÁQUINA
escena('s08', 'clones', w('Pero llegan', mas=-0.2))              # R5: CLONES; las pantallas en rojo
escena('s09', 'valor', w('En mil novecientos noventa', mas=-0.2))  # R3 → R6: 1993; Microsoft pasa a IBM
escena('s10', 'golpe', w('En una negociación', mas=-0.15),       # R1: la lección, con la firma BFM
       etq='En una negociación', b1='No mires solo<br>el precio.', b2='Mira lo que<br>te quedas.',
       conf={'etq': {'palabra': 'En', 'n': 3, 'grande': True}, 'b1': {'palabra': 'no', 'n': 2, 'y': 340, 'tam': 120},
             'b2': {'palabra': 'Mira', 'y': 700, 'tam': 120, 'sube': -30}, 'firma': True, 'firma_t': 3.35})
escena('s11', 'contrato', w('I Be Eme', 6, mas=-0.05), modo='cierre',  # R15: el contrato del principio
       titulo='<span class="l l1">IBM solo miró</span><span class="l l2"><span class="bloque">el precio.</span></span>')
DURACION = w('precio', 2, fin=True, mas=1.3)           # la última frase, 2 s en pantalla

# Subtítulos quemados, salvo donde la pantalla ya escribe lo que dice la voz.
sin_subtitulos(0, w('Mil', mas=-0.2))
sin_subtitulos(w('Cree', mas=-0.15), w('Pero llegan', mas=-0.25))   # EL NEGOCIO ES LA MÁQUINA
sin_subtitulos(w('En una negociación', mas=-0.2), DURACION)

# --- Música: un lecho sin entrada (el bucle no puede empezar en silencio); se calla en la lección.
musica('lecho', 0, DURACION, vol=0.28, fi=0.05, fo=0.25,
       puntos=[(w('En una negociación', mas=-0.35), 0.28), (w('En una negociación', mas=-0.1), 0.0),
               (w('I Be Eme', 6, mas=-0.3), 0.0), (w('I Be Eme', 6, mas=-0.05), 0.3)])

# --- Efectos (cada uno con su causa en pantalla)
sonido('3237', w('firmó', mas=-0.05), vol=0.8, ini=0.19, dur=0.8)            # la firma
sonido('impact-bass-1', w('peores', mas=-0.02), vol=0.32)                     # el sello
sonido('whoosh-short', w('Con', mas=-0.2), vol=0.3)
sonido('pop', w('veinticinco', mas=0.3), vol=0.35)
sonido('whoosh', w('Mil', mas=-0.2), vol=0.25)
for t in (w('Mil'), w('novecientos'), w('ochenta'), w('ochenta', mas=0.12)):
    sonido('key-press', t - 0.03, vol=0.45)
sonido('pop', w('operativo', fin=True, mas=0.05), vol=0.35)
sonido('whoosh-cinematic', w('primera', mas=-0.15), vol=0.22, dur=1.5, fo=0.4)
sonido('click', w('promete', mas=-0.08), vol=0.5)
sonido('impact-bass-2', w('ninguno', mas=-0.02), vol=0.34)
sonido('2212', w('Así', mas=-0.12), vol=0.6, dur=1.3, fo=0.2)                 # el recibo
sonido('1417', w('mil', 2, fin=True, mas=0.12), vol=0.55)                     # el total
sonido('2212', w('en el contrato', mas=-0.25), vol=0.55, dur=1.3, fo=0.2)     # vuelve el contrato
sonido('3237', w('I Be Eme', 4, mas=0.05), vol=0.75, ini=0.19, dur=0.55, fo=0.1)
sonido('click', w('firma', mas=0.22), vol=0.6)                                # el sello FIRMADO
sonido('whoosh-short', w('negocio', mas=-0.33), vol=0.3)
sonido('whoosh', w('Pero llegan', mas=-0.25), vol=0.25)
sonido('impact-bass-2', w('clones', mas=-0.02), vol=0.3)
sonido('whoosh-cinematic', w('otras', mas=-0.15), vol=0.2, dur=1.6, fo=0.5)  # la cámara entra en las copias
sonido('whoosh-short', w('compran', mas=-0.08), vol=0.28)
sonido('whoosh', w('En mil novecientos noventa', mas=-0.25), vol=0.22)
for t in (w('mil', 3), w('novecientos', 2), w('noventa'), w('tres')):
    sonido('key-press', t - 0.03, vol=0.4)
sonido('riser', w('más', mas=-2.9), vol=0.3, ini=1.2, dur=2.9, fo=0.15)      # el riser sube hasta 3,9 s
sonido('impact-bass-1', w('más', mas=0.02), vol=0.28)
sonido('impact-bass-2', w('En una negociación', mas=-0.17), vol=0.36)        # el golpe rojo
sonido('whoosh', w('I Be Eme', 6, mas=-0.25), vol=0.25)
sonido('click', w('precio', 2, mas=-0.3), vol=0.45)
