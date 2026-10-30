# Capítulo II · Ver a través del bronce (1951–2005). Lo lee kit/montar.py; ver su cabecera.
# Forma: cada intento de mirar dentro es una luz distinta: la lámpara del escritorio de Price, la caja de luz de
# la radiografía (que se enciende: destello), el flexo del taller de Wright y la luz fría del tomógrafo. Acaba
# contando lo que hay: 82 fragmentos, 30 ruedas, un tercio de la máquina.

# 1 · El escritorio de Price.
toma('escritorio', 0, entra='negro', mov=dict(zoom=(1.04, 1.09), panY=(0.01, -0.01)), capas=False,
     luz=(0.5, 0.14), luzI=0.2, luzR=0.3, ventana=(0.25, 0.55, 0.6), ventanaI=0.5)
bloque(150, 520, [E('1951 · FÍSICO E HISTORIADOR', w('mil')), N('Derek\nde Solla Price', w('Derek'), tam=112)], sale=w('Ocho', mas=-0.5))
sonido('lapiz', w('Derek', mas=0.4), vol=0.22, dur=2.4, fi=0.2, fo=0.6)

# 2 · Su artículo de 1959, a máquina.
toma('escritorio', w('Ocho', mas=-0.3), entra='corte', mov=dict(zoom=(1.3, 1.36), panX=(0.06, 0.07), panY=(0.0, 0.02)), capas=False,
     luz=(0.5, 0.14), luzI=0.2, luzR=0.3, ventana=(0.26, 0.5, 0.62), ventanaI=0.55)
bloque(150, 440, [E('SCIENTIFIC AMERICAN · JUNIO DE 1959', w('artículo')), M('«An Ancient Greek Computer»', w('título', mas=0.1), tam=96)],
       sale=w('En mil novecientos setenta', mas=-0.6))
sonido('paginas', w('publica', mas=-0.1), vol=0.25, dur=1.4)
sonido('maquina', w('título', mas=0.05), vol=0.3, dur=1.7, fo=0.2)

# 3 · La radiografía: la caja de luz se enciende (destello) y se ven las ruedas de dentro.
toma('radiografia', w('En mil novecientos setenta', mas=-0.3), entra='destello', luzColor=(0.92, 0.96, 1.0),
     mov=dict(zoom=(1.42, 1.5), panX=(-0.13, -0.11), panY=(0.03, 0.05)), luz=(0.62, 0.45), luzI=0.1, luzR=0.3,
     ventana=(0.26, 0.24, 0.5), ventanaI=0.55)
bloque(150, 150, [E('1971 · RAYOS GAMMA', w('setenta')), D('Con el físico Charalampos Karakalos', w('Jaralambos'))], sale=w('Por primera', mas=-0.4))
grafico('rueda', w('ruedas', mas=-0.5), w('Su', mas=-0.3), id='rueda-rx', centro=[0.41, 0.58], radio=215, dientes=44, giro=2,
        en=w('ruedas', mas=-0.1), sale=w('Su', mas=-0.55))
sonido('interruptor', w('En mil novecientos setenta', mas=-0.34), vol=0.35, dur=1.0)
sonido('zumbido', w('En mil novecientos setenta', mas=-0.25), vol=0.12, dur=w('Su') - w('En mil novecientos setenta') - 0.1, fi=0.2, fo=0.5)

# 4 · El taller de Wright y su modelo de latón.
toma('taller', w('Su', mas=-0.3), entra='corte', mov='izq', luz=(0.86, 0.18), luzI=0.18, ventana=(0.25, 0.52, 0.62), ventanaI=0.45)
bloque(150, 470, [E('MUSEO DE CIENCIAS DE LONDRES', w('conservador')), N('Michael Wright', w('Máikel'), tam=120)], sale=w('construye', mas=-0.2))
bloque(150, 470, [E('DÉCADAS DE MODELOS', w('modelos', mas=-0.1))], sale=w('En dos mil cinco', mas=-0.6))
sonido('tictac3', w('construye', mas=-0.2), vol=0.18, dur=2.6, fi=0.3, fo=0.6)

# 5 · El tomógrafo en el museo (2005).
toma('tomografo', w('En dos mil cinco', mas=-0.3), entra='barrido', mov='empuje', luz=(0.7, 0.45), luzColor=(0.75, 0.9, 1.0),
     luzI=0.16, ventana=(0.25, 0.5, 0.62), ventanaI=0.45)
bloque(150, 450, [E('2005 · TOMOGRAFÍA DE RAYOS X', w('cinco')), D('Cardiff · Atenas · Salónica', w('internacional')),
                  D('Hewlett-Packard · luz rasante', w('técnica'))], sale=w('Bajo', mas=-0.6))
sonido('transformador', w('tomógrafo', mas=-0.3), vol=0.14, dur=6.0, fi=0.4, fo=0.8)
sonido('escaner', w('técnica', mas=-0.1), vol=0.16, dur=1.0)

# 6 · Las letras bajo la corrosión: se lee más del doble.
toma('tapa', w('Bajo', mas=-0.3), entra='corte', capas=False, mov=dict(zoom=(1.08, 1.16), panX=(0.02, -0.01)),
     luz=(0.72, 0.4), luzI=0.18, ventana=(0.25, 0.5, 0.6), ventanaI=0.5)
bloque(150, 380, [E('TEXTO LEGIBLE', w('lee', mas=-0.2)), C('× 2', w('doble'), tam=210)], sale=w('Son', mas=-0.5))

# 7 · Lo que hay: 82 fragmentos, 30 ruedas, un tercio de la máquina.
toma('placa', w('Son', mas=-0.3), entra='oscuro', mov=dict(zoom=(1.04, 1.08), camX=(-0.006, 0.006)), brillo=0.6,
     luz=(0.7, 0.3), luzI=0.1, ventana=(0.25, 0.5, 0.6), ventanaI=0.35)
grafico('tercio', w('Son', mas=-0.3), DUR)
bloque(150, 300, [E('FRAGMENTOS', w('fragmentos', 2)), C('82', w('fragmentos', 2, mas=0.4), desde=0, dur=1.0, tam=200)], sale=DUR - 0.9)
bloque(150, 640, [E('RUEDAS DENTADAS', w('treinta')), C('30', w('dentadas', mas=0.2), desde=0, dur=0.9, tam=200)], sale=DUR - 0.9)

MUSICA = dict(subidas=[(w('antiguo', fin=True, mas=0.1), w('En mil novecientos setenta', mas=-0.1), 0.32)])
