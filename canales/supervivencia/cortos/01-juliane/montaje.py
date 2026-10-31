# Corto 1 de supervivencia · «La chica que cayó del cielo» (Juliane Koepcke, Perú, 1971). Lo monta el kit de
# BusinessForMen con la marca del canal:
#   python3 canales/businessformen/kit/montar.py --canal canales/supervivencia cortos/01-juliane
# Vertical, unos 69 s, en bucle: el último plano («la chica que cayó del cielo») es el primero (la caída, CAYÓ 3.000
# METROS). El final va delante; la historia, en presente y contada por días (el contador cruza el vídeo); la regla del
# padre se tacha en el segundo 29 y no se lee hasta el 42 (bucle abierto de 13 s). Retención: ../../../RETENCION.md.
import json
import os

formato(1080, 1920, voz0=0.1, cola=0.7)
subtitulos()
M = json.load(open(os.path.join(AQUI, 'recursos', 'mapa.json')))

escena('s01', 'caida', 0)
escena('s02', 'ruta', w('Perú', mas=-0.12), peru=M['peru'], vecinos=M['vecinos'], lima=M['lima'], pucallpa=M['pucallpa'])
escena('s03', 'tormenta', w('El avión', mas=-0.12))
escena('s04', 'foto', w('Yuliane', 2, mas=-0.12), foto='asiento', modo='sola')
escena('s05', 'inventario', w('Tiene', mas=-0.12))
escena('s06', 'regla', w('Pero su padre', mas=-0.12), modo='oculta')
escena('s07', 'foto', w('Oye', mas=-0.12), foto='sola', modo='aviones')
DIAS = w('Pasan', mas=0.45)                                              # «No la ven» se queda 1,2 s
escena('s08', 'dias', DIAS)
escena('s09', 'regla', w('La regla', mas=-0.12), modo='revela')
escena('s10', 'foto', w('Encuentra', mas=-0.12), foto='caminando', modo='arroyo')
escena('s11', 'foto', w('Después', mas=-0.12), foto='refugio', modo='refugio')
escena('s12', 'gasolina', w('Recuerda', mas=-0.12))
escena('s13', 'foto', w('Al día siguiente', mas=-0.12), foto='lenadores', modo='rescate')
escena('s14', 'final', w('En el avión', mas=-0.12))
DURACION = w('cielo', fin=True, mas=0.95)

# Subtítulos, salvo donde la pantalla ya escribe lo que dice la voz.
sin_subtitulos(0, w('Perú', mas=-0.12))                                  # 17 AÑOS · CAYÓ 3.000 METROS · Y SOBREVIVIÓ
sin_subtitulos(w('Sola', mas=-0.12), w('Tiene', mas=-0.12))              # SOLA.
sin_subtitulos(w('No', 2, mas=-0.12), w('Pasan', mas=-0.12))             # NO LA VEN
sin_subtitulos(w('Sobrevivió', 2, mas=-0.12), DURACION)                  # SOBREVIVIÓ UNA, y vuelve el gancho

# --- Música: crece con la historia (pieza 2: de −25 a −17 dB en 30 s); se retira en la regla revelada y en el final.
musica('lecho', 0, DURACION, vol=0.26, fi=0.05, fo=0.3,
       puntos=[(w('Y el avión', mas=0.3), 0.22), (w('Yuliane', 2, mas=-0.1), 0.14), (w('Pero su padre', mas=-0.1), 0.22),
               (w('busca', mas=-0.5), 0.22), (w('busca', mas=-0.1), 0.05), (w('Encuentra', mas=-0.2), 0.24),
               (w('Sobrevivió', 2, mas=-0.3), 0.24), (w('Sobrevivió', 2, mas=0.1), 0.1), (w('la chica', mas=0.0), 0.26)])

# --- Ambiente y efectos (cada uno con su causa en pantalla). Revisado el 31-oct con audio/revisar_mezcla.py: los efectos
# sonaban +1,4 LU por encima de la voz (el trueno y los golpes graves, hasta 15 LU más que ella) y había 39 en 70 s.
# Ahora: sin sonidos de interfaz (pop, click, riser, whoosh), un solo golpe grave y cada efecto, al menos 8 LU bajo la voz.
sonido('0154', 0, vol=0.04, ini=3.0, dur=5.4, fi=0.0, fo=0.8)                     # viento de la caída (el bucle no empieza en silencio)
sonido('impact-bass-1', w('sobrevivió', mas=0.0), vol=0.03)
for t in (w('veinticuatro'), w('diciembre'), w('mil', 2), w('novecientos'), w('setenta')):
    sonido('key-press', t - 0.02, vol=0.38)                                         # la fecha a máquina
sonido('3008', w('vuela', mas=-0.3), vol=0.14, ini=1.5, dur=3.4, fi=0.4, fo=0.8)   # el avión cruza el mapa
sonido('0740', w('tormenta', mas=-0.5), vol=0.13, ini=6.0, dur=4.6, fi=0.3, fo=0.6)  # lluvia y truenos
sonido('3115', w('rayo', mas=-0.05), vol=0.08, ini=0.0, dur=2.4, fo=0.6)             # el rayo
sonido('1470', w('Yuliane', 2, mas=-0.3), vol=0.06, ini=10.0, dur=8.2, fi=0.6, fo=1.0)   # la selva de noche (insectos)
sonido('3008', w('aviones', mas=-0.6), vol=0.25, ini=0.5, dur=2.6, fi=0.3, fo=0.8)   # los aviones que la buscan
sonido('1354', w('agua', mas=-0.2), vol=0.3, ini=4.0, dur=8.0, fi=0.5, fo=1.2)       # el arroyo
sonido('1299', w('sigue', mas=-0.1), vol=0.45, ini=0.4, dur=1.6, fo=0.3)            # pasos entre ramas
sonido('0246', w('bidón', mas=-0.05), vol=0.55, ini=0.2, dur=1.0, fo=0.3)           # la lata de gasolina
sonido('2713', w('Al día siguiente', mas=-0.3), vol=0.2, ini=20.0, dur=3.6, fi=0.4, fo=0.8)   # río y pájaros
sonido('0154', w('la chica', mas=-0.3), vol=0.04, ini=3.0, dur=1.9, fi=0.6, fo=0.0)   # vuelve el viento de la caída
