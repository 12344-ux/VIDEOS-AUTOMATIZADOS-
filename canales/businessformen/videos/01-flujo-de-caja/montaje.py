# Vídeo 1 · «Por qué quiebran empresas que ganan dinero». Lo lee canales/businessformen/kit/montar.py.
# Tramo de prueba: del gancho a «crecer hasta morir» (las cuatro primeras partes del guion) y el logo.
# Cada escena usa un recurso distinto del anterior (EDICION.md); los golpes rojos (R1) son «−120 millones» y
# «crecer hasta morir».

# --- Gancho
escena('s01', 'cifra', 0)                                        # R3: 1973 cifra a cifra; W. T. Grant; +38.000.000 $
escena('s02', 'veces', w('Sus acciones', mas=-0.25))             # R3 → R14: 20 veces; «todo va bien»; pero… 0 $
escena('s03', 'rojo', w('queman', mas=-0.12))                    # R1: −120.000.000 $
escena('s04', 'titular', w('Dos años', mas=-0.3))                # R7: el titular recreado
escena('s05', 'pregunta', w('Cómo', mas=-0.3))                   # R13: la pregunta, y silencio
# --- Lo que está en juego
escena('s06', 'diez', w('Pasa', mas=-0.3))                       # R6: 111 cierres; 4 de cada 10
escena('s07', 'ganar', w('Hoy', mas=-0.25))                      # R2: GANAR ≠ TENER; sale con cortina roja
# --- Beneficio no es caja
escena('s08', 'carpinteria', w('Imagina', mas=-0.3))             # R9 + R8: la factura sobre el taller
escena('s09', 'partida', w('Tu contabilidad', mas=-0.25))        # R4: contabilidad y banco
escena('s10', 'lunes', w('Las dos cosas', mas=-0.25))            # R2: el beneficio / la caja… el lunes
escena('s11', 'caja', w('Y los sueldos', mas=-0.25))             # R2 → R10: CAJA con dinero dentro
# --- Los ladrones de la caja
escena('s12', 'ciclo', w('El dinero de', mas=-0.3))              # R5: el ciclo de caja
escena('s13', 'debe', w('El primero', mas=-0.25))                # R12: la factura pendiente
escena('s14', 'almacen', w('El segundo', mas=-0.25))             # R9: el almacén, dinero dormido
escena('s15', 'plazos', w('El tercero', mas=-0.25))              # R11: pagas el 30, cobras el 90
escena('s16', 'cuarto', w('Y hay un cuarto', mas=-0.3))          # R13: 4… CRECER
escena('s17', 'crecer', w('Si cada pedido', mas=-0.25))          # R6 → R1: ventas arriba, caja abajo; HASTA MORIR
escena('s18', 'logo', w('morir', fin=True, mas=1.5))             # el logo
DURACION = w('morir', fin=True, mas=1.5) + 3.4

# --- Música: tres lechos y silencio en la pregunta y en el golpe final.
musica('gancho', 0, w('Cómo', mas=0.6), vol=0.3, fi=0.8, fo=0.9)
musica('explica', w('Pasa', mas=-0.2), w('El dinero de', mas=-0.3), vol=0.26, fi=1.2, fo=1.0)
musica('ladrones', w('El dinero de', mas=-0.5), w('Hasta', 2, mas=-0.08), vol=0.26, fi=1.0, fo=0.15,
       puntos=[(w('Si cada pedido'), 0.28), (w('Por eso'), 0.36), (w('Hasta', 2, mas=-0.3), 0.42)])
musica('explica', w('morir', fin=True, mas=1.4), DURACION, vol=0.5, fi=0.3, fo=0.8)

# --- Efectos
for t in (w('Mil'), w('novecientos'), w('setenta'), w('tres')):
    sonido('click-soft', t, vol=0.12)
sonido('whoosh-short', w('presenta', mas=-0.1), vol=0.1)
sonido('key-press', w('dólares', mas=0.05), vol=0.18)
sonido('click', w('veinte', mas=0.05), vol=0.16)
sonido('whoosh-short', w('Pero', mas=-0.1), vol=0.12)
sonido('impact-bass-1', w('queman', mas=-0.14), vol=0.36)
sonido('whoosh', w('Dos años', mas=-0.32), vol=0.2)
sonido('impact-bass-2', w('quiebra', mas=-0.02), vol=0.14)
sonido('key-press', w('ciento', 2), vol=0.16)
for k in range(4):
    sonido('click-soft', w('quedarse', mas=0.12 * k), vol=0.12)
sonido('whoosh-short', w('ganar', mas=-0.08), vol=0.1)
sonido('whoosh-short', w('tener', mas=-0.08), vol=0.1)
sonido('whoosh', w('Imagina', mas=-0.62), vol=0.2)
sonido('typing', w('pedido', mas=0.1), vol=0.1, dur=1.4, fo=0.3)
sonido('click', w('treinta', 2, mas=0.05), vol=0.18)
sonido('click-soft', w('apunta'), vol=0.14)
for p in ('madera', 'sueldos', 'alquiler'):
    sonido('click-soft', w(p), vol=0.12)
sonido('impact-bass-2', w('pierde', mas=0.3), vol=0.2)
sonido('click', w('lunes', mas=0.02), vol=0.18)
for t in (w('sueldos', 2), w('facturas'), w('banco', 2)):
    sonido('click-soft', t, vol=0.12)
sonido('whoosh-short', w('beneficio', 3, mas=0.3), vol=0.14)
sonido('impact-bass-2', w('caja', 3, mas=-0.06), vol=0.26)
sonido('whoosh-short', w('vueltas', mas=-0.1), vol=0.1)
for p in ('comprar', 'almacén', 'venta', 'pague'):
    sonido('click-soft', w(p), vol=0.12)
sonido('chime', w('vuelve', mas=0.02), vol=0.1)
sonido('key-press', w('ciclo', mas=0.05), vol=0.16)
sonido('impact-bass-2', w('deben', mas=-0.02), vol=0.24)
sonido('typing', w('tarda', 2), vol=0.08, dur=1.2, fo=0.3)
sonido('click', w('prestando', mas=0.02), vol=0.16)
sonido('whoosh-cinematic', w('El segundo', mas=-0.3), vol=0.14)
for k in range(3):
    sonido('pop', w('caja', 5, mas=0.15 * k), vol=0.08)
sonido('click', w('treinta', 5), vol=0.14)
sonido('click', w('noventa', 2), vol=0.14)
sonido('whoosh-short', w('sesenta', mas=-0.05), vol=0.14)
sonido('impact-bass-2', w('cuarto', mas=-0.02), vol=0.2)
sonido('impact-bass-1', w('crecer', mas=-0.04), vol=0.24)
sonido('riser', w('nuevo', mas=-0.2), vol=0.14, dur=w('Hasta', 2, mas=-0.1) - w('nuevo', mas=-0.2), fo=0.3)
sonido('impact-bass-1', w('Hasta', 2, mas=-0.1), vol=0.38)
sonido('click', w('morir', fin=True, mas=1.7), vol=0.2)
sonido('whoosh-short', w('morir', fin=True, mas=2.0), vol=0.14)
