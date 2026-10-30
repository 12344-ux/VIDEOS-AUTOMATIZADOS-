# Capítulo VI · Los cinco errantes. Lo lee kit/montar.py; ver su cabecera.
# Forma: el cielo del crepúsculo con su planeta que retrocede (graficos/retro.html); la tapa con los números en
# griego (graficos/griego.html); de vuelta al cielo, los ciclos; y el frente de anillos de la UCL
# (graficos/cosmos.html). Acaba en la caja reconstruida: una hipótesis, aún por fabricar.

# 1 · El crepúsculo: cinco planetas; «errantes»; el retroceso.
toma('crepusculo', 0, entra='negro', mov=dict(zoom=(1.04, 1.1), camX=(-0.01, 0.01)), luz=(0.73, 0.4), luzColor=(0.9, 0.95, 1.0),
     luzI=0.14, ventana=(0.25, 0.5, 0.62), ventanaI=0.45)
bloque(150, 400, [E('A SIMPLE VISTA', w('simple')), C('5', w('cinco', mas=0.1), unidad='planetas', tam=200)], sale=w('Los griegos', mas=-0.45))
grafico('griego', w('Los griegos', mas=-0.3), w('De las ruedas', mas=-0.3), id='griego-a', z=6, sale=w('De las ruedas', mas=-0.6),
        lineas=[dict(g='ΠΛΑΝΗΤΑΙ', trad='ERRANTES', t=w('errantes', mas=-0.1), x=150, y=360)])
grafico('retro', w('vagan', mas=-0.5), w('De las ruedas', mas=-0.3), centro=[0.6, 0.22], largo=760, radio=160,
        desde_t=w('vagan'), hasta_t=w('retroceder', fin=True, mas=0.3), sale=w('De las ruedas', mas=-0.6))
bloque(150, 650, [E('MOVIMIENTO RETRÓGRADO', w('retroceder', mas=-0.2))], sale=w('De las ruedas', mas=-0.6))
sonido('grillos', 0.4, vol=0.14, dur=w('De las ruedas') - 0.5, fi=1.0, fo=0.8)

# 2 · La tapa: dos números escritos con letras.
toma('tapa', w('De las ruedas', mas=-0.3), entra='oscuro', capas=False, mov=dict(zoom=(1.12, 1.2), panX=(-0.06, -0.04)),
     luz=(0.72, 0.4), luzI=0.18, ventana=(0.25, 0.52, 0.62), ventanaI=0.55)
bloque(150, 170, [E('UCL · 2021', w('veintiuno'))], sale=w('Son ciclos', mas=-0.6))
grafico('griego', w('De las ruedas', mas=-0.3), w('Son ciclos', mas=-0.3), id='griego-b', z=6, sale=w('Son ciclos', mas=-0.6),
        lineas=[dict(g='ΨΞΒ', trad='462 · JUNTO A VENUS', t=w('cuatrocientos', mas=-0.1), x=150, y=290),
                dict(g='ΨΜΒ', trad='442 · JUNTO A SATURNO', t=w('cuatrocientos', 2, mas=-0.1), x=150, y=590)])
sonido('escaner', w('cuatrocientos', mas=-0.3), vol=0.12, dur=1.0)

# 3 · Los ciclos: Venus y Saturno.
toma('crepusculo', w('Son ciclos', mas=-0.3), entra='oscuro', mov=dict(zoom=(1.12, 1.2), panX=(0.04, 0.06)), luz=(0.73, 0.4),
     luzColor=(0.9, 0.95, 1.0), luzI=0.18, ventana=(0.25, 0.5, 0.62), ventanaI=0.5)
bloque(150, 380, [E('CICLO DE VENUS', w('tras')), C('462', w('años', mas=0.1), desde=0, dur=1.6, unidad='años', tam=200)], sale=w('Los de Saturno', mas=-0.4))
bloque(150, 380, [E('CICLO DE SATURNO', w('Saturno', 3)), C('442', w('cuatrocientos', 4, mas=0.9), desde=0, dur=1.2, unidad='años', tam=200)],
       sale=w('Con esas', mas=-0.2))
sonido('olas', w('Son ciclos', mas=-0.3), vol=0.1, dur=14, ini=60, fi=0.8, fo=1.0)

# 4 · El frente de anillos.
toma('placa', w('Con esas', mas=0.1), entra='corte', mov=dict(zoom=(1.04, 1.08), camX=(-0.006, 0.006)), brillo=0.58,
     luz=(0.7, 0.3), luzI=0.1, ventana=(0.24, 0.5, 0.55), ventanaI=0.35)
grafico('cosmos', w('Con esas', mas=0.1), w('Aunque', mas=-0.3))
bloque(150, 140, [E('MODELO DE LA UCL', w('reconstruyó'))], sale=w('Aunque', mas=-0.6))
sonido('tictac', w('girando', mas=-0.2), vol=0.16, dur=3.6, fi=0.2, fo=1.0)

# 5 · La caja reconstruida: una hipótesis.
toma('caja', w('Aunque', mas=-0.3), entra='corte', mov='retroceso', luz=(0.66, 0.36), luzI=0.2, ventana=(0.25, 0.55, 0.6), ventanaI=0.45)
bloque(150, 560, [E('RECONSTRUCCIÓN · AÚN SIN FABRICAR', w('reconstrucción'))], sale=DUR - 0.9)

MUSICA = dict(subidas=[(w('nada', fin=True, mas=0.1), w('Pero', mas=-0.1), 0.28),
                       (w('ritmo', fin=True, mas=0.1), w('Un cosmos', mas=-0.1), 0.3)])
