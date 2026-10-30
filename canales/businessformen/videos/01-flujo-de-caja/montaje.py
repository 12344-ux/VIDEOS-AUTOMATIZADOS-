# Vídeo 1 · «Por qué quiebran empresas que ganan dinero». Lo lee canales/businessformen/kit/montar.py.
# Cada escena usa un recurso distinto del anterior (EDICION.md); los tres golpes rojos (R1) son «−120 millones»,
# «crecer hasta morir» y «la caja es realidad». Motivos que vuelven: el mapa de Grant (se enciende y se apaga), el ciclo
# de caja (se explica y luego se acorta) y las barras de «crecer» (en la regla 4).
import json
import os

MAPA = json.load(open(os.path.join(AQUI, 'recursos', 'mapa.json')))

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
# --- La historia de W. T. Grant
escena('s19', 'mapa', w('Volvamos', mas=-0.3), **MAPA)           # R11: 1973 → el mapa; mil tiendas desde Lynn
escena('s20', 'tienda', w('A finales', mas=-0.2))                # R9: la tienda de los 60; + TIENDAS, + CRÉDITO
escena('s21', 'clientes', w('En mil novecientos sesenta y ocho', mas=-0.25))  # R3: 324.359.000 $ a plazos
escena('s22', 'lineas', w('En sus cuentas', mas=-0.3))           # R6: beneficio plano, caja hundida; lo atrapado
escena('s23', 'deposito', w('Para tapar', mas=-0.35))            # R5: el depósito con agujero, deuda y dividendos
escena('s24', 'quiebra', w('En octubre', mas=-0.3))              # R3: +1.000 M$ de deuda; el sello QUIEBRA
escena('s25', 'apagon', w('En la primavera', mas=-0.3), **MAPA)  # R15: el mapa se apaga hacia Lynn
escena('s26', 'estudio', w('Años después', 2, mas=-0.3))         # R7 → R11: el estudio; diez años antes
# --- Carillion
escena('s27', 'salto', w('Podrías', mas=-0.3))                   # R14: 1975 gira hasta 2018
escena('s28', 'grua', w('cayó', mas=-0.12))                      # R9: la grúa; hospitales, colegios, cárceles
escena('s29', 'dividendos', w('Entre dos mil doce', mas=-0.3))   # R6: 376 M£ en dividendos; 217 M£ en rojo
escena('s30', 'proveedores', w('Y obligó', mas=-0.3))            # R11: 120 días; el problema pasa a los demás
escena('s31', 'liquidacion', w('El quince', mas=-0.3))           # R2 → R6: 29 M£ frente a 7.000 M£, a escala
escena('s32', 'codicia', w('Un informe', mas=-0.3))              # R2: imprudencia, arrogancia, CODICIA; silencio
# --- Amazon, al revés
escena('s33', 'alreves', w('Ahora', mas=-0.3))                   # R14 → R6: AL REVÉS; sus pérdidas
escena('s34', 'amazon', w('Cobra a sus', mas=-0.3))              # R5: cobra antes, paga después; CICLO NEGATIVO
escena('s35', 'carta', w('Por eso', 2, mas=-0.3))                # R7: la carta de 2004; BENEFICIO tachado
# --- Las cuatro reglas
escena('s36', 'reglas', w('Qué haces', mas=-0.3))                # R13: la pregunta; cuatro cuadros
escena('s37', 'regla1', w('Una mira', mas=-0.3))                 # R2 + R11: cada semana; el beneficio, una vez
escena('s38', 'regla2', w('Dos prevé', mas=-0.3))                # R8: la tabla de 13 semanas; S9 en rojo
escena('s39', 'regla3', w('Tres acorta', mas=-0.3))              # R15: el ciclo encoge; el proveedor asfixiado
escena('s40', 'regla4', w('Y cuatro', mas=-0.3))                 # R6 → R2 → R12: cuánta caja; la pared
# --- Cierre
escena('s41', 'cierre', w('Dóbliu', 3, mas=-0.3))                # R9: la tienda vacía; LE FALTABA CAJA
escena('s42', 'dicho', w('Hay un viejo', mas=-0.3))              # R2 → R1: LA CAJA ES REALIDAD
escena('s43', 'suscribete', w('Si te ha servido', mas=-0.3))     # la llamada, con la marca
LOGO = w('entiende', fin=True, mas=0.6)
escena('s44', 'logo', LOGO)                                      # el logo
DURACION = LOGO + 3.4

# --- Música: un lecho por tramo; silencio en la pregunta, en los golpes rojos y tras «codicia».
musica('gancho', 0, w('Cómo', mas=0.6), vol=0.3, fi=0.8, fo=0.9)
musica('explica', w('Pasa', mas=-0.2), w('El dinero de', mas=-0.3), vol=0.26, fi=1.2, fo=1.0)
musica('ladrones', w('El dinero de', mas=-0.5), w('Hasta', 2, mas=-0.08), vol=0.26, fi=1.0, fo=0.15,
       puntos=[(w('Si cada pedido'), 0.28), (w('Por eso'), 0.36), (w('Hasta', 2, mas=-0.3), 0.42)])
musica('historia', w('Volvamos', mas=-0.4), w('Podrías', mas=1.6), vol=0.26, fi=1.4, fo=1.6,
       puntos=[(w('En octubre'), 0.3), (w('quiebra', 4), 0.32), (w('Años después', 2), 0.24)])
musica('carillion', w('dos mil dieciocho', mas=-0.25), w('codicia', fin=True, mas=0.1), vol=0.26, fi=0.6, fo=0.25,
       puntos=[(w('Un informe'), 0.3)])
musica('amazon', w('Ahora', mas=-0.1), w('Qué haces', mas=-0.3), vol=0.25, fi=0.5, fo=0.8)
musica('explica', w('Cuatro', 3, mas=-0.25), w('Dóbliu', 3, mas=-0.2), vol=0.24, fi=0.8, fo=1.2)
musica('cierre', w('Dóbliu', 3, mas=-0.6), w('Y', 37, mas=-0.12), vol=0.3, fi=1.2, fo=0.12)
musica('explica', w('Si te ha servido', mas=-0.6), DURACION, vol=0.45, fi=0.4, fo=0.8)

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
# La historia de W. T. Grant
sonido('whoosh-cinematic', w('Volvamos', mas=-0.45), vol=0.16)
sonido('whoosh', w('Grant', mas=-0.45), vol=0.1)
sonido('click-soft', w('fundada', mas=0.1), vol=0.12)
sonido('typing', w('seis', mas=0.1), vol=0.07, dur=w('tiendas', 2, fin=True) - w('seis') + 0.1, fo=0.4)
sonido('chime', w('tiendas', 2, fin=True, mas=0.15), vol=0.08)
sonido('whoosh-short', w('A finales', mas=-0.3), vol=0.12)
sonido('click', w('abrió'), vol=0.14)
sonido('whoosh-short', w('venta', 2, mas=-0.2), vol=0.1)
sonido('click', w('crédito'), vol=0.14)
sonido('key-press', w('clientes'), vol=0.14)
sonido('typing', w('trescientos', mas=-0.1), vol=0.06, dur=1.4, fo=0.3)
sonido('impact-bass-2', w('dólares', 2, fin=True), vol=0.16)
sonido('click-soft', w('cuentas', 2), vol=0.12)
sonido('whoosh-short', w('Pero', 3, mas=-0.1), vol=0.12)
sonido('impact-bass-1', w('año', 3, fin=True, mas=-0.05), vol=0.26)
sonido('click-soft', w('clientes', 2, mas=-0.2), vol=0.12)
sonido('click-soft', w('almacenes', 2, mas=-0.2), vol=0.12)
sonido('click', w('agujero', mas=-0.1), vol=0.14)
sonido('whoosh-short', w('pidió', mas=-0.15), vol=0.1)
sonido('whoosh-short', w('pagando', mas=-0.05), vol=0.1)
sonido('whoosh', w('para', 4, mas=-0.25), vol=0.12)
sonido('click-soft', w('octubre', mas=-0.05), vol=0.12)
sonido('typing', w('mil', 16, mas=-0.1), vol=0.06, dur=1.3, fo=0.3)
sonido('impact-bass-1', w('quiebra', 4, mas=0.07), vol=0.38)
sonido('whoosh-cinematic', w('En la primavera', mas=-0.35), vol=0.1)
sonido('impact-bass-2', w('tiendas', 4, fin=True, mas=0.15), vol=0.14)
sonido('whoosh', w('Años después', 2, mas=-0.3), vol=0.16)
sonido('click-soft', w('Yeims'), vol=0.1)
sonido('click-soft', w('Cláid'), vol=0.1)
sonido('whoosh-short', w('conclusión', mas=-0.35), vol=0.12)
for k in range(7):
    sonido('pop', w('señales', mas=-0.05 + 0.12 * k), vol=0.05)
sonido('impact-bass-2', w('diez', 2, mas=-0.05), vol=0.18)
# Carillion
sonido('click', w('Podrías', mas=-0.25), vol=0.12)
sonido('whoosh-short', w('dos mil dieciocho', mas=-0.15), vol=0.12)
for k in range(4):
    sonido('click-soft', w('dos mil dieciocho', mas=0.6 + 0.07 * k), vol=0.1)
sonido('whoosh-cinematic', w('cayó', mas=-0.3), vol=0.16)
sonido('impact-bass-2', w('Carílion'), vol=0.16)
for p in ('hospitales', 'colegios', 'cárceles'):
    sonido('click-soft', w(p, mas=-0.05), vol=0.12)
sonido('typing', w('trescientos', 2, mas=-0.1), vol=0.06, dur=1.6, fo=0.3)
sonido('impact-bass-2', w('Doscientos', mas=-0.05), vol=0.22)
sonido('click-soft', w('obligó', mas=-0.1), vol=0.12)
sonido('typing', w('esperar', mas=-0.1), vol=0.07, dur=w('días', 3, fin=True) - w('esperar') + 0.3, fo=0.3)
sonido('whoosh', w('pasaba', mas=-0.25), vol=0.16)
sonido('click', w('quince', mas=-0.1), vol=0.12)
sonido('impact-bass-1', w('liquidación', mas=-0.1), vol=0.3)
sonido('pop', w('veintinueve', mas=-0.1), vol=0.1)
sonido('riser', w('siete', mas=-0.9), vol=0.1, dur=1.0, fo=0.1)
sonido('impact-bass-2', w('siete', mas=0.8), vol=0.24)
sonido('click', w('informe', mas=-0.1), vol=0.12)
sonido('impact-bass-2', w('imprudencia', mas=-0.1), vol=0.12)
sonido('impact-bass-2', w('arrogancia', mas=-0.1), vol=0.14)
sonido('impact-bass-1', w('codicia', mas=-0.18), vol=0.32)
# Amazon
sonido('whoosh', w('al', 2, mas=-0.3), vol=0.18)
sonido('click', w('Ámazon', mas=-0.1), vol=0.12)
sonido('whoosh-short', w('Cobra', mas=-0.1), vol=0.12)
sonido('pop', w('vende', mas=-0.1), vol=0.08)
sonido('whoosh-short', w('deprisa', 2, mas=-0.05), vol=0.1)
sonido('whoosh-short', w('paga', 2, mas=-0.1), vol=0.12)
sonido('impact-bass-2', w('negativo', mas=-0.1), vol=0.22)
sonido('whoosh', w('Por eso', 2, mas=-0.45), vol=0.16)
sonido('click-soft', w('medida', mas=-0.1), vol=0.1)
sonido('whoosh-short', w('no', 4, mas=-0.25), vol=0.12)
sonido('click', w('beneficio', 4, fin=True, mas=-0.1), vol=0.18)
sonido('impact-bass-2', w('flujo', 2, mas=-0.12), vol=0.2)
# Las cuatro reglas
for k in range(4):
    sonido('click-soft', w('Cuatro', 3, mas=-0.1 + 0.09 * k), vol=0.12)
sonido('click', w('Una mira', mas=-0.1), vol=0.12)
sonido('typing', w('semana', mas=0.1), vol=0.06, dur=0.9, fo=0.2)
sonido('chime', w('beneficio', 5, mas=-0.05), vol=0.08)
sonido('impact-bass-2', w('problemas', mas=-0.05), vol=0.14)
sonido('click', w('Dos prevé', mas=-0.1), vol=0.12)
for p in ('entrar', 'salir'):
    sonido('typing', w(p, mas=-0.35), vol=0.06, dur=0.6, fo=0.2)
sonido('typing', w('Si', 6, mas=-0.1), vol=0.06, dur=0.8, fo=0.2)
sonido('impact-bass-2', w('negativo', 2, mas=-0.1), vol=0.2)
sonido('whoosh-short', w('ocho', 3, mas=-0.25), vol=0.1)
sonido('click', w('Tres acorta', mas=-0.1), vol=0.12)
for p in (w('Cobra', 2), w('dejes'), w('negocia')):
    sonido('whoosh-short', p - 0.05, vol=0.1)
    sonido('click-soft', p - 0.1, vol=0.12)
sonido('impact-bass-2', w('Carílion', 2, mas=-0.15), vol=0.18)
sonido('click', w('Y cuatro', mas=-0.1), vol=0.12)
sonido('whoosh-short', w('Crecer', 4, mas=-0.35), vol=0.12)
sonido('whoosh', w('correr', mas=-0.1), vol=0.2)
sonido('impact-bass-1', w('pared', mas=0.02), vol=0.42)
# Cierre
sonido('whoosh-cinematic', w('Dóbliu', 3, mas=-0.45), vol=0.14)
for p, n in (('ventas', 1), ('tiendas', 5), ('clientes', 5)):
    sonido('click-soft', w(p, n, mas=0.15), vol=0.12)
sonido('impact-bass-2', w('faltaba', mas=-0.1), vol=0.24)
sonido('impact-bass-1', w('Y', 37, mas=-0.1), vol=0.4)
sonido('pop', w('Si', 7, mas=-0.1), vol=0.1)
sonido('click', w('suscríbete', mas=0.1), vol=0.22)
sonido('chime', w('entiende', fin=True, mas=-0.1), vol=0.08)
sonido('click', LOGO + 0.2, vol=0.2)
sonido('whoosh-short', LOGO + 0.5, vol=0.14)
