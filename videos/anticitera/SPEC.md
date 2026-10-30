# «El mecanismo de Anticitera» · el documental completo

```text
GOAL:    9–10 min de historia y misterio que se sigan sin esfuerzo: qué es la máquina, cómo se descubrió lo que
         hacía y qué queda sin saber. Cada idea difícil (las fases, el perno y la ranura, el saros, los planetas)
         se enseña dibujada, en el momento en que la voz la nombra.
OUTPUT:  HyperFrames, 1920 x 1080, 30 fps. Nueve proyectos (apertura/ y cap1/ … cap8/) que se renderizan por
         separado y se unen sin recomprimir (unir.sh). Unos 10 min.
VOICE:   Supertonic-3 M1 con semilla fija por frase; cada capítulo arranca con su rótulo y la voz entra en 3,4 s.
LOOK:    estilo A, como la apertura (SPEC de apertura/): suelo #0D1114, tinta #F3EDE4, acento #E8B66A; Cormorant
         Garamond 500 y cursiva para títulos, nombres y cifras; Hanken Grotesk 600 28 px en versalitas espaciadas
         (0,32 em) para etiquetas, 500 34 px para datos, 28 px para créditos; GFS Didot para el griego.
         Planchas FLUX.3 (1280 x 720, 4 pasos, EDSR a 1920 x 1080) a sangre en 2.5D, con etalonaje, viñeta, grano y
         «ventana» bajo el texto en el shader. Los dibujos van en trazo de 2 px en el acento sobre una plancha de
         bronce oscura (placa, al 55–62 % de brillo), y en tinta lo secundario o lo deducido.
MOTION:  como la apertura: llegadas expo.out, cámara sine/power2.inOut, salidas power3.in más cortas; etiquetas
         letra a letra (30 ms), títulos palabra a palabra (67 ms), cifras con contador que aterriza en su palabra.
         Los dibujos son función del tiempo (graficos/*.html con kit/ayuda.js): su cámara propia entra en el
         detalle (los ejes del perno, las casillas del saros, el dial de los juegos) y vuelve.
CUTS:    corte con oscurecido del 40 % (3 cuadros), barrido con desenfoque, paso por oscuro, destello (la caja de
         luz que se enciende), zoom a través (de la caja reconstruida a su frente). Entre capítulos, a negro.
SOUND:   una pieza de MusicGen por capítulo, extendida a su duración (audio/lecho.py) y más presente con los
         rótulos y en los silencios; efectos CC0 solo con causa en pantalla (tic-tac en las ruedas, la manivela,
         el interruptor y el zumbido de la caja de luz, el mar y los grillos de noche, la fundición).
BANNED:  los de la guía y los de la apertura; además: repetir con letras lo que dice la voz (los rótulos dan el
         dato que la voz no da: fechas exactas, nombres bien escritos, la fuente, la cifra); un dibujo sin causa en
         la voz; poner caras a personas reales (Price, Wright, Stais, Rehm salen de espaldas, en sus objetos o
         solo con su nombre); presentar las planchas como fotos del mecanismo (lo dicen los créditos).
```

## Capítulos

| | Título | Dura | Planos y dibujos |
| --- | --- | --- | --- |
| — | Apertura: el hallazgo | 34 s | ver `apertura/SPEC.md` |
| I | Un bulto olvidado | 58 s | sala del museo · bandeja con los pedazos (golpe de zoom) · la lupa de Stais (1902 cifra a cifra; la rueda se dibuja sobre la del cristal) · la datación tachada · Rehm · el cajón y el contador 1902 → 1951 |
| II | Ver a través del bronce | 76 s | escritorio de Price (1959 a máquina) · la radiografía (destello de la caja de luz; la rueda sobre la de la película) · el taller de Wright · el tomógrafo · la tapa (× 2) · el tercio que se conserva: 82 fragmentos, 30 ruedas |
| III | Una caja con el cielo dentro | 59 s | la caja reconstruida · zoom al frente: la rueda mayor da una vuelta (365 días), anillos del zodíaco y de los 365 días, agujas del Sol y de la Luna · la esfera real · las fases en el dibujo · la fila de agujeros («¿cuántos?») · ruedas en lámina · la Luna |
| IV | La Luna que acelera | 70 s | la Luna sobre el mar · la órbita de Kepler con marcas de igual tiempo · Hiparco · el perno y la ranura: los ejes a 1,1 mm, ± 6,5°, montado sobre la rueda que gira (8,85 años) · la Luna roja |
| V | Anunciar la oscuridad | 72 s | las espirales: 19 años y 235 meses arriba, saros de 223 meses abajo; la aguja sigue el surco; los signos Σ y Η; la rueda de 223 dientes; el dial de los juegos · el eclipse · Olimpia · la Luna roja |
| VI | Los cinco errantes | 75 s | el crepúsculo con su planeta que retrocede (ΠΛΑΝΗΤΑΙ) · la tapa: ΨΞΒ = 462 y ΨΜΒ = 442 · los ciclos · el frente de anillos de la UCL · la caja: una reconstrucción |
| VII | ¿Quién lo construyó? | 65 s | el carguero · las monedas · el mapa de Pérgamo y Éfeso al naufragio · la línea de tiempo del 205 a. C. · el mapa de Corinto y Siracusa · Cicerón y la esfera de Arquímedes · Posidonio en Rodas · las manos del artesano |
| VIII | Lo que el mar guardó | 89 s | el reloj medieval · la línea del hueco de más de 1400 años · la fundición · el anillo de 354 agujeros · las ruedas que se atascan antes de 120 días · el museo · la noche sobre la isla · el fragmento de la apertura: el cielo se oscurece; título y créditos |

## QA

Por capítulo: el primer cuadro (rótulo sobre su plancha, nunca negro del todo pasado el primer segundo), cada
cifra cuando aterriza, cada dibujo en su momento clave (los de arriba) y el último cuadro (negro). Además:
`check` sin errores en los nueve proyectos y `snapshot --review` de cada capítulo (costuras y hoja de móvil).
