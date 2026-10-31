# Corto 5 · «El perrito» (modelo de negocio). Lo lee canales/businessformen/kit/montar.py: cortos/05-el-perrito.
# Vertical, 48 s, en bucle: el cierre («por eso sigue costando 1,50 $») vuelve al gancho («el mismo precio desde 1985»)
# sobre el mismo perrito. La idea, para que se entienda: las cuotas son casi nada de lo que ingresa y más de la mitad de
# lo que gana; el perrito es la razón para volver. Edición: 2.5D en el perrito y en el almacén, transiciones con causa
# (la cortina roja de la marca, barridos, un iris desde el perrito) y un golpe rojo para la pregunta final.
formato(1080, 1920, voz0=0.1, cola=0.45)
subtitulos()

ETIQUETA = dict(tx=90, ty=210)    # la etiqueta de precio, a la izquierda del vaso y sobre el perrito (medido en la imagen)
escena('s01', 'perrito', 0, modo='gancho', **ETIQUETA,               # R9 2.5D: EL MISMO PRECIO DESDE 1985
       titulo='<span class="l">El mismo precio</span><span class="l"><span class="bloque">desde 1985.</span></span>')
escena('s02', 'inflacion', w('Con la inflación', mas=-0.2), entrada='barrido')     # R6: 1,50 $ frente a 4,55 $
escena('s03', 'amenaza', w('Cuando', mas=-0.2), entrada='cortina')                 # R7: «Si subes el perrito, te mato»
escena('s04', 'pregunta', w('Cómo', mas=-0.2))                                      # R13: ¿CÓMO GANA DINERO? → LA ENTRADA
escena('s05', 'almacen', w('Para comprar', mas=-0.2), entrada='subida')            # R9 2.5D + R8: la tarjeta de socio
escena('s06', 'cuotas', w('Esas cuotas', mas=-0.2), entrada='barrido')             # R6: 1,9 % de lo que ingresa; 51 % del beneficio
escena('s07', 'perrito', w('El perrito no', mas=-0.2), modo='razon', **ETIQUETA,   # R15: el perrito, otra vez
       entrada={'tipo': 'iris', 'x': 420, 'y': 680},
       titulo='<span class="l l1">No es el <span class="tacha">negocio.<i></i></span></span><span class="l l2">Es la razón</span>'
              '<span class="l l3"><span class="bloque">para volver.</span></span>')
escena('s08', 'golpe', w('Antes de subir', mas=-0.2),                               # R1: la pregunta, con la firma BFM
       etq='Antes de subir un precio,', b1='¿Dónde ganas<br>de verdad?', b2='',
       conf={'etq': {'palabra': 'antes', 'grande': True}, 'b1': {'palabra': 'dónde', 'y': 420, 'tam': 116}, 'b2': None,
             'firma': True, 'firma_t': 2.1})
escena('s09', 'perrito', w('Por eso', mas=-0.2), modo='cierre', **ETIQUETA,         # R15: vuelve el gancho (el bucle)
       entrada='cortina',
       titulo='<span class="l l1">Por eso sigue</span><span class="l l2"><span class="bloque">costando 1,50 $.</span></span>')
DURACION = w('medio', 3, fin=True, mas=1.2)

sin_subtitulos(0, w('Con la inflación', mas=-0.25))               # el gancho ya lo escribe
sin_subtitulos(w('Con la inflación', mas=-0.25), w('Cuando', mas=-0.25))
sin_subtitulos(w('si subes', mas=-0.2), w('Cómo', mas=-0.25))     # la cita, escrita
sin_subtitulos(w('Cómo', mas=-0.25), w('Para comprar', mas=-0.25))
sin_subtitulos(w('Esas cuotas', mas=-0.25), DURACION)            # el dato, la razón, la pregunta y el cierre: escritos

# --- Música: lecho sin entrada; se calla en el golpe y vuelve para el cierre.
musica('lecho', 0, DURACION, vol=0.27, fi=0.05, fo=0.25,
       puntos=[(w('Antes de subir', mas=-0.45), 0.27), (w('Antes de subir', mas=-0.2), 0.0),
               (w('Por eso', mas=-0.35), 0.0), (w('Por eso', mas=-0.1), 0.28)])

# --- Efectos
sonido('pop', w('dólar', mas=-0.08), vol=0.35)                                        # la etiqueta
sonido('whoosh-short', w('Con la inflación', mas=-0.22), vol=0.28)
sonido('0194', w('inflación', mas=0.1), vol=0.35, ini=0.1, dur=0.45, fo=0.1)          # monedas: sube lo que costaría
sonido('0194', w('cuatro', mas=0.2), vol=0.3, ini=3.0, dur=0.45, fo=0.1)
sonido('whoosh', w('Cuando', mas=-0.25), vol=0.22)
sonido('click', w('subirlo', mas=-0.12), vol=0.4)
sonido('impact-bass-1', w('mato', mas=0.02), vol=0.3)                                  # TE MATO
sonido('whoosh-short', w('Cómo', mas=-0.22), vol=0.25)
sonido('click', w('vendiendo', fin=True, mas=0.03), vol=0.45)                          # NO VENDIENDO, tachado
sonido('pop', w('entrada', mas=-0.05), vol=0.35)                                       # la entrada
sonido('whoosh-short', w('Para comprar', mas=-0.22), vol=0.25)
sonido('whoosh', w('cuota', mas=-0.45), vol=0.25)                                      # llega la tarjeta
sonido('whoosh-short', w('Esas cuotas', mas=-0.22), vol=0.25)
sonido('pop', w('dos', mas=-0.05), vol=0.3)
sonido('1417', w('mitad', mas=0.05), vol=0.45)                                         # 51 %
sonido('whoosh-short', w('El perrito no', mas=-0.22), vol=0.25)
sonido('click', w('negocio', mas=0.2), vol=0.4)
sonido('impact-bass-2', w('Antes de subir', mas=-0.22), vol=0.34)                      # el golpe rojo
sonido('whoosh', w('Por eso', mas=-0.25), vol=0.22)
