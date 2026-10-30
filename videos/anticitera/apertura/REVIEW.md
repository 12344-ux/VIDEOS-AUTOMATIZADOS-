# Revisión de la apertura (34 s)

## Decisiones creativas

- Línea elegida: **el hallazgo**, un zoom continuo en el que cada plano termina en lo que abre el siguiente
  (STORYLINES.md). Sin construir: «la máquina primero» y «las cifras».
- El título solo lo dice la pantalla: la voz acaba en «…que se conoce» y el título aterriza 0,23 s después,
  con el golpe grave.
- Sin subtítulos quemados (competirían con la tipografía editorial): `subtitulos.srt` para YouTube.
- La rueda que revela el escáner son los contornos de la propia plancha (`../lineas_rueda.py`), no un dibujo
  encima: cuadra con la imagen por construcción (comprobado a tamaño real).
- El tren de ruedas del título usa números de dientes del mecanismo real (64, 38, 48 y 24) y gira con sus
  relaciones; los dientes engranan.
- Música: la variante 1 de MusicGen, elegida midiendo (la 2 tenía el 71 % de la energía por debajo de 150 Hz,
  que en un móvil no suena). Entra con la calma, tras el rayo.

## Medido y solo mirado

- `check`: sin errores; contraste correcto en sus muestras; las líneas, con tiempo de lectura.
- `snapshot --review`: los 14 cuadros clave cuentan la historia sin palabras; las seis costuras (rayo,
  barrido, oscuridad, oscurecido, zoom en el buje y llegada) sin saltos; a 360 px se leen las cifras y títulos.
- Corregido en la revisión: «RUEDA PRINCIPAL» rozaba la corona (ahora «RUEDA MAYOR»), la costura borrosa de las capas 2.5D en la isla y las estatuas (borde más
  estrecho y menos margen de relleno), las flechas de los rumbos, la línea guía que tapaba el rótulo, el dato
  del título que chocaba con una rueda, el empuje lento del fondo al final y dos tiempos de lectura.
- El sonido está medido (picos y volumen), no oído.

## El plano más flojo

El fondo del título: el bronce ampliado aún deja ver la gran cruz y el buje, y compite un poco con las ruedas
dibujadas. Con más tiempo, una plancha propia del interior de la máquina. Las estatuas de mármol de pie en el
fondo del mar son poco verosímiles (estarían caídas): se nota poco porque el foco es el efebo de bronce tumbado.

## Avisos que se quedan

- `dead_stretch` 0–6,75 s: falso. Ahí hay lluvia, dos relámpagos y un empuje de cámara en el lienzo WebGL
  (que `check` no ve) y los textos letra a letra van con `data-layout-ignore` (ver estilos/README.md).
- `composition_file_too_large`: `planchas.html` es el motor de las planchas (shader y claves de cámara).
