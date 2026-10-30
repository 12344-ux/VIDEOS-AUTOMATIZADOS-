# Capítulo II · Ver a través del bronce (1951–2005). Lo lee kit/montar.py; ver su cabecera.
# Revisión 2 (tras la primera entrega, que se quedaba en «imagen + voz»): un plano por idea, de 3 a 6 s, y en cada
# uno algo que pasa en la palabra que lo dice: el escáner que atraviesa el bronce y deja ver las ruedas de dentro,
# las ruedas señaladas, la luz rasante que hace aparecer las letras griegas, los fragmentos que se cuentan.

# 1 · El escritorio de Price: el año.
toma('escritorio', 0, entra='negro', mov=dict(zoom=(1.04, 1.1), panY=(0.01, -0.01)), capas=False, sat=0.5,
     luz=(0.5, 0.14), luzI=0.2, luzR=0.3, ventana=(0.25, 0.55, 0.6), ventanaI=0.5)
bloque(150, 400, [E('ATENAS', w('cincuenta', mas=-0.3)), C('1951', w('cincuenta'), tam=230)], sale=w('Derek', mas=-0.45))
sonido('lapiz', w('mil', mas=0.2), vol=0.2, dur=2.4, fi=0.2, fo=0.6)

# 2 · Más cerca: la foto del fragmento y sus dibujos de ruedas; su nombre.
toma('escritorio', w('Derek', mas=-0.25), entra='corte', capas=False, sat=0.5, centro=(0.62, 0.55),
     mov=dict(zoom=(1.45, 1.55), panX=(-0.02, 0.03)), luz=(0.5, 0.14), luzI=0.2, ventana=(0.25, 0.5, 0.55), ventanaI=0.6)
bloque(150, 420, [E('FÍSICO E HISTORIADOR', w('físico')), N('Derek\nde Solla Price', w('Derek'), tam=120)], sale=w('Ocho', mas=-0.45))

# 3 · Su artículo de 1959, a máquina, sobre sus dibujos.
toma('escritorio', w('Ocho', mas=-0.25), entra='barrido', capas=False, sat=0.45, centro=(0.83, 0.5), brillo=0.75,
     mov=dict(zoom=(1.6, 1.7), panY=(0.02, -0.02)), luz=(0.5, 0.14), luzI=0.15, ventana=(0.3, 0.5, 0.7), ventanaI=0.7)
bloque(150, 400, [E('SCIENTIFIC AMERICAN · 1959', w('artículo')), M('«An Ancient\nGreek Computer»', w('título', mas=0.1), tam=116)],
       sale=w('En mil novecientos setenta', mas=-0.5))
sonido('paginas', w('publica', mas=-0.1), vol=0.25, dur=1.4)
sonido('maquina', w('título', mas=0.05), vol=0.32, dur=1.9, fo=0.2)

# 4 · 1971: la caja de luz se enciende (destello) con la radiografía.
toma('radiografia', w('En mil novecientos setenta', mas=-0.3), entra='destello', luzColor=(0.92, 0.96, 1.0),
     mov=dict(zoom=(1.42, 1.5), panX=(-0.13, -0.11), panY=(0.03, 0.05)), luz=(0.62, 0.45), luzI=0.1, luzR=0.3,
     ventana=(0.26, 0.3, 0.55), ventanaI=0.6)
bloque(150, 200, [E('1971 · RAYOS GAMMA', w('setenta')), D('Con el físico Charalampos Karakalos', w('físico', 2))],
       sale=w('atraviesa', mas=-0.4))
sonido('interruptor', w('En mil novecientos setenta', mas=-0.34), vol=0.35, dur=1.0)
sonido('zumbido', w('En mil novecientos setenta', mas=-0.25), vol=0.12, dur=6.0, fi=0.2, fo=0.5)

# 5 · «Atraviesa los fragmentos»: el escáner barre el bronce y deja ver las ruedas ocultas.
toma('fragmento', w('atraviesa', mas=-0.25), entra='corte', capas=False, centro=(0.7307, 0.4648),
     mov=dict(zoom=(1.05, 1.1)), luz=(0.72, 0.3), luzI=0.12, ventanaI=0.2)
grafico('rayos', w('atraviesa', mas=-0.25), w('Su', mas=-0.3), imagen='fragmento_rx.jpg', archivos=['fragmento_rx.jpg'],
        barre=w('atraviesa', mas=0.1), termina=w('gamma', fin=True), sale=w('Su', mas=-0.6))
sonido('escaner', w('atraviesa', mas=0.05), vol=0.3, dur=1.0)
sonido('transformador', w('atraviesa', mas=-0.2), vol=0.14, dur=8.0, fi=0.3, fo=0.6)

# 6 · Más cerca, ya en rayos X: las ruedas de dentro, señaladas; sus dientes se cuentan.
toma('fragmento', w('Por primera', mas=-0.25), entra='corte', capas=False, centro=(0.66, 0.55),
     mov=dict(zoom=(1.55, 1.62)), luz=(0.72, 0.3), luzI=0.1, ventanaI=0.2)
grafico('senal', w('Por primera', mas=-0.25), w('Su', mas=-0.3), id='senal-ruedas', z=3,
        marcas=[dict(u=0.625, v=0.593, r=132, t=w('ruedas', mas=-0.05), sale=w('Su', mas=-0.55), n='RUEDA OCULTA', lado='izq'),
                dict(u=0.797, v=0.343, r=98, t=w('dentro', mas=0.1), sale=w('Su', mas=-0.55), n='OTRA MÁS', lado='izq', vert='aba')])
bloque(150, 690, [C('36', w('dientes', mas=0.1), desde=0, dur=1.0, unidad='dientes', tam=170)], sale=w('Su', mas=-0.5))
sonido('tictac', w('contar', mas=-0.3), vol=0.22, dur=1.6, fo=0.4)

# 7 · «Su reconstrucción tiene errores»: la de 1974, tachada.
toma('escritorio', w('Su', mas=-0.25), entra='corte', capas=False, sat=0.45, centro=(0.83, 0.62), brillo=0.7,
     mov=dict(zoom=(1.7, 1.78)), luz=(0.5, 0.14), luzI=0.12, ventana=(0.3, 0.5, 0.7), ventanaI=0.7)
bloque(150, 440, [E('PRICE · 1974', w('Su', mas=-0.1)), D('«Gears from the Greeks»', w('Su', mas=-0.05), tacha=w('errores'))],
       sale=w('Máikel', mas=-0.3))

# 8 · El taller de Wright.
toma('taller', w('Máikel', mas=-0.12), entra='corte', mov='izq', luz=(0.86, 0.18), luzI=0.18, ventana=(0.25, 0.52, 0.62), ventanaI=0.5)
bloque(150, 440, [E('SCIENCE MUSEUM', w('conservador')), N('Michael Wright', w('Máikel'), tam=124)], sale=w('pasa', mas=-0.3))

# 9 · «Rueda a rueda»: cada rueda del modelo, señalada en su palabra; modelos que funcionan.
toma('taller', w('pasa', mas=-0.1), entra='corte', centro=(0.72, 0.48), mov=dict(zoom=(1.45, 1.52), camX=(0.01, -0.01)),
     luz=(0.86, 0.18), luzI=0.18, ventana=(0.25, 0.5, 0.55), ventanaI=0.55)
grafico('senal', w('pasa', mas=-0.1), w('En dos mil cinco', mas=-0.3), id='senal-taller', z=3,
        marcas=[dict(u=0.695, v=0.46, r=290, t=w('rueda', mas=-0.1), sale=w('En dos mil cinco', mas=-0.6)),
                dict(u=0.76, v=0.54, r=120, t=w('rueda', 2, mas=-0.05), sale=w('En dos mil cinco', mas=-0.6)),
                dict(u=0.655, v=0.53, r=105, t=w('construye', mas=-0.1), sale=w('En dos mil cinco', mas=-0.6))])
bloque(150, 440, [E('DÉCADAS', w('décadas')), D('Corrige la reconstrucción', w('corrigiéndola'))], sale=w('En dos mil cinco', mas=-0.6))
sonido('tictac3', w('rueda', mas=-0.2), vol=0.2, dur=3.6, fi=0.3, fo=0.6)

# 10 · 2005: el tomógrafo en el museo; el fragmento, dentro.
toma('tomografo', w('En dos mil cinco', mas=-0.3), entra='barrido', mov=dict(zoom=(1.14, 1.22), panX=(-0.08, -0.06)),
     luz=(0.7, 0.45), luzColor=(0.75, 0.9, 1.0), luzI=0.16, ventana=(0.25, 0.7, 0.62), ventanaI=0.5)
bloque(150, 220, [E('TOMOGRAFÍA · 2005', w('cinco')), D('Cardiff · Atenas · Salónica', w('internacional'))], sale=w('una técnica', mas=-0.45))
grafico('senal', w('En dos mil cinco', mas=-0.3), w('una técnica', mas=-0.3), id='senal-tomo', z=3,
        marcas=[dict(u=0.665, v=0.56, r=105, t=w('tomógrafo', mas=-0.1), sale=w('una técnica', mas=-0.6), n='EL FRAGMENTO',
                     s='rayos X de alta energía', lado='izq', vert='aba', foco=True)])
sonido('transformador', w('tomógrafo', mas=-0.3), vol=0.16, dur=4.0, fi=0.3, fo=0.6)
sonido('escaner', w('energía', mas=-0.2), vol=0.18, dur=1.0)

# 11 · La luz rasante sobre el bronce: aparecen las letras (relieves de décimas de milímetro).
toma('tapa2', w('una técnica', mas=-0.3), entra='oscuro', capas=False, sat=0.8, brillo=0.9, mov=dict(zoom=(1.04, 1.07)),
     luz=(0.3, 0.5), luzI=0.1, ventana=(0.2, 0.15, 0.45), ventanaI=0.65)
grafico('inscripcion', w('una técnica', mas=-0.3), w('Son', mas=-0.3), z=3, area=[160, 300, 1600, 680],
        barre=w('luz', mas=-0.1), termina=w('finos', fin=True, mas=0.6), sale=w('Son', mas=-0.55),
        destaca=dict(g='ΗΛΙΟΣ', trad='«Sol»', x=1180, y=560, w=330, t=w('griegas', mas=-0.1)))
bloque(150, 120, [E('LUZ RASANTE', w('luz'))], sale=w('Bajo', mas=-0.4))
sonido('escaner', w('luz', mas=-0.1), vol=0.14, dur=1.0)

# 12 · Más cerca: miles de letras; se lee más del doble.
toma('tapa2', w('Bajo', mas=-0.25), entra='corte', capas=False, centro=(0.66, 0.52), mov=dict(zoom=(1.3, 1.36)),
     luz=(0.3, 0.5), luzI=0.1, sat=0.8, ventana=(0.2, 0.3, 0.5), ventanaI=0.65)
bloque(150, 160, [E('TEXTO LEGIBLE', w('lee', mas=-0.2)), C('× 2', w('doble'), tam=210)], sale=w('Son', mas=-0.55))

# 13 · Los 82 fragmentos, contados.
toma('fragmentos', w('Son', mas=-0.25), entra='corte', capas=False, mov=dict(zoom=(1.04, 1.1), panX=(0.0, 0.01)),
     luz=(0.65, 0.4), luzI=0.12, ventana=(0.2, 0.5, 0.5), ventanaI=0.6)
bloque(150, 300, [E('FRAGMENTOS', w('fragmentos', 2, mas=-0.3)), C('82', w('fragmentos', 2, mas=0.2), desde=0, dur=1.0, tam=210)],
       sale=w('Apenas', mas=-0.4))
bloque(150, 640, [E('RUEDAS', w('fragmentos', 2, mas=0.5)), C('30', w('treinta', mas=0.3), desde=0, dur=0.8, tam=170)], sale=w('Apenas', mas=-0.4))
sonido('monedas', w('fragmentos', 2, mas=-0.2), vol=0.18, dur=1.2)

# 14 · Un tercio de la máquina.
toma('placa', w('Apenas', mas=-0.2), entra='oscuro', mov=dict(zoom=(1.04, 1.08), camX=(-0.006, 0.006)), brillo=0.55,
     luz=(0.7, 0.3), luzI=0.1, ventana=(0.25, 0.5, 0.6), ventanaI=0.35)
grafico('tercio', w('Apenas', mas=-0.2), DUR)
bloque(150, 380, [E('SE CONSERVA', w('tercio', mas=-0.2)), C('1/3', w('tercio', mas=0.2), tam=230)], sale=DUR - 0.9)

MUSICA = dict(subidas=[(w('antiguo', fin=True, mas=0.1), w('En mil novecientos setenta', mas=-0.1), 0.32)])
