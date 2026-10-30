# Revisión del documental completo

La apertura tiene su propia revisión en `apertura/REVIEW.md`. Esta cubre los ocho capítulos y la unión.

## Decisiones creativas

- **Cada idea difícil se dibuja cuando la voz la nombra**, sobre una plancha de bronce oscura que hace de pizarra:
  el frente (la rueda mayor da una vuelta y salen 365 días), la órbita con marcas de igual tiempo, el perno y la
  ranura con su desfase real (±6,5°) y la cámara metida entre los ejes, las espirales con la aguja que sigue el
  surco, los anillos de los planetas, el mapa con costas reales y los agujeros que se cuentan hasta 354. Los gráficos
  tienen su propia cámara: entran en el detalle y vuelven.
- **Los rótulos dan lo que la voz no dice**: la fecha exacta, el nombre bien escrito, la fuente (*Scientific
  American*, junio de 1959; Carman y Evans, 2014), la cifra (± 6,5°, 8,85 años, 120 días). Nada repite la frase.
- **Las personas reales no tienen cara**: Stais y el artesano, de espaldas o solo sus manos; Price, Wright, Rehm,
  Hiparco y Posidonio, con su nombre sobre sus objetos o su lugar.
- **Hilos entre capítulos**: el III acaba en la Luna con la que empieza el IV; el IV, en la Luna roja que anuncia el V;
  los agujeros del III («¿cuántos?») se cuentan en el VIII; el VIII vuelve al fragmento de la apertura y el cielo se
  oscurece justo cuando la voz dice «oscurecerse».
- Pasos entre planos con causa: la caja de luz que se enciende (destello), el zoom por la esfera de la caja hasta su
  frente, el corte de la esfera dibujada a la real y vuelta. Entre capítulos, a negro.

## Medido y solo mirado

- `check` sin errores en los nueve proyectos. Medido: tiempos de lectura (los avisos del montador y de `check`),
  contraste en sus muestras, que ningún rótulo salga de su toma, la energía de cada pieza de música bajo 150 Hz
  (dos se rehicieron) y el volumen de entrega.
- Mirado en fotogramas clave de cada capítulo con las planchas reales: choques de texto con los dibujos (se acortaron
  etiquetas), la rueda dibujada sobre la de la lupa y la de la radiografía, encuadres de planchas con anacronismos.
- **El sonido está medido, no oído**: niveles, que esté y dónde cae. Nadie ha escuchado la mezcla final.
- No se pasó `snapshot --review` completo (hojas de costuras y de móvil) a cada capítulo, solo fotogramas elegidos.

## Los planos más flojos

- **Rodas** salió con casas blancas de aspecto moderno y barcos de otra época: se sustituyó por el mapa centrado en
  Rodas (la plancha queda sin usar). **Olimpia** tiene unas gradas que parecen modernas: va reencuadrada y dura 4,6 s.
- La **vitrina** del capítulo VIII muestra una pieza demasiado grande y maciza para ser los fragmentos reales.
- Con más tiempo: planchas propias para Rodas y la vitrina, y un plano del interior del bronce para el VIII.

## Avisos que se quedan

- `dead_stretch` en todos los capítulos: falso, `check` no ve la cámara del lienzo WebGL ni los dibujos que se pintan
  con `hf-seek`.
- `text_below_floor` en las espirales, el perno y el frente: son textos de SVG pequeños que la cámara del gráfico
  amplía (en pantalla miden 40–60 px).
- `line_unread` de los signos Σ y Η: se leen como letras sueltas; la leyenda los explica y está 5 s en pantalla.
- `canvas_content_at_edge`: las planchas van a sangre.
- Los créditos de la tarjeta final duran 8,7 s y la regla pide 9,8 s para la línea de fuentes: están también en la
  descripción.
