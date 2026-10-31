# Kit de montaje de BusinessForMen

Un vídeo del canal es una lista de escenas ancladas a las palabras de la voz. Cada escena es una subcomposición de
HyperFrames escrita a mano (una plantilla HTML con GSAP) con la marca Consejo compartida. `montar.py` lo junta todo
en un proyecto que se revisa y se renderiza con `video/hf.sh`.

```bash
canales/businessformen/videos/<vídeo>/preparar.sh          # voz, música e imágenes, en salidas/businessformen/<vídeo>/
python3 canales/businessformen/kit/montar.py <vídeo>        # escribe videos/<vídeo>/proyecto/ y copia los recursos
cd canales/businessformen/videos/<vídeo>/proyecto && ../../../../../video/hf.sh check --json
../../../../../video/hf.sh render -o salida.mp4 --quality high --crf 20 --quiet
```

## Las piezas

- `videos/<vídeo>/montaje.py`: las escenas (`escena(id, plantilla, desde, **parámetros)`), la música (`musica(...)`)
  y los efectos (`sonido(...)`), con los tiempos sacados de la voz: `w("palabra", n)`. La cabecera de `montar.py`
  explica la API.
- `videos/<vídeo>/escenas/*.html`: una plantilla por escena. Dentro, `{{ID}}`, `{{DUR}}`, `/*MARCA*/` (el CSS común,
  `marca.css`) y `/*AYUDA*/` (el JS común, `ayuda.js`): `w()`, `f()` y `serie()` dan los tiempos de las palabras en el
  tiempo de la escena; `sube()`, `entra()`, `aparece()`, `cuenta()`, `traza()`, `trocea()`, `cortina()` y `alBuscar()`
  son las animaciones de la marca.
- `marca.css` y `ayuda.js`: lo que comparten todas las escenas.

## Cortos verticales, transiciones y 2.5D (sesión 4)

- `formato(1080, 1920, voz0=0.1, cola=…)`, `subtitulos()` y `sin_subtitulos(desde, hasta)` en `montaje.py`: el lienzo
  vertical y los subtítulos quemados (ver `../cortos/README.md`). `/*CORTO*/` mete `corto.css` en una plantilla.
- `escena(…, entrada="cortina" | "barrido" | "subida" | {"tipo": "iris", "x": …, "y": …})`: la escena entra sobre la
  anterior, que sigue debajo mientras dura la transición (0,4–0,5 s; el anfitrión de la anterior se alarga). Cada escena
  va encima de la anterior (`z-index`) y en pistas alternas del Studio. La entrada es un `clip-path` sobre la raíz de la
  escena, así que no choca con los temblores (que mueven la raíz con `x`/`y`).
- `profundidad(t0, d, {f1, s1, sx, sy, …})` en `ayuda.js`: el 2.5D por capas. La plantilla pone dos capas
  (`.fondo25` con `<n>_fondo.jpg` y `.frente25` con `<n>_frente.png`, de `imagen/capas25d.py`) y el frente se mueve más
  que el fondo. Lo que tiene que moverse con una capa (un precio en una pantalla de la foto) va dentro de esa capa.
  **Solo sirve si el corte sigue el contorno de algo sobre un fondo liso** (el auditorio y su público, el perrito y el
  vaso sobre negro): en una superficie que se aleja poco a poco (una mesa vista en picado, un pasillo, una pizza en su
  caja) cualquier corte la cruza y deja una franja borrosa que se ve aunque el paralaje sea pequeño. Ahí, acercamiento
  sin capas. Si el corte automático parte el objeto, `"umbral"` en `imagenes.json` (ver `../cortos/preparar.sh`), y
  mirar el resultado a tamaño real al principio y al final del movimiento: el hueco rellenado asoma donde no se espera
  (el interior de un vaso, que está más lejos que su borde).
- `aparece(sel, 0, d)` deja el elemento invisible en el fotograma 0 (el `fromTo` empieza en opacidad 0): lo que tiene
  que estar en la miniatura no se anima, se deja puesto.
- Una plantilla que no está en `escenas/` se busca en `../comun/` (el golpe rojo de los cortos).

## Lo que hay que saber (medido o roto al hacer el vídeo 1)

- HyperFrames encierra el CSS de cada subcomposición bajo `[data-composition-id="…"]`: la raíz de la plantilla no
  puede llevar estilos. Por eso cada plantilla tiene una raíz sin clase y, dentro, `<div id="{{ID}}" class="esc">`.
- Las tildes de las mayúsculas (Á, É, Ú) asoman por encima de la máscara de una palabra que va a subir: `sube()`
  parte del 140 % de su alto.
- `trocea()` respeta los `<br>`; sin eso, dos renglones se pegan («cajao sin financiación»).
- Un contenedor con `position: absolute` y un subrayado absoluto dentro de un elemento en línea no se ve: hace falta
  `inline-block`.
- Las cifras se escriben con punto de miles y el signo menos tipográfico (`fmt()`); `toLocaleString("es-ES")` no
  agrupa los números de cuatro cifras.
- Los efectos largos de la biblioteca (el `riser` dura 10 s) se recortan con `dur` para que no pasen del final.
- Un trazo con remate redondo o cuadrado deja un punto en su extremo antes de dibujarse (el guion de largo cero):
  `traza()` lo oculta hasta que empieza.
- Los años no llevan punto de miles: `cuenta(…, { crudo: true })`.
- Un `tl.set(…, 0)` no se pinta en el primer fotograma de la escena: lo que nace oculto, con CSS o con `fromTo`.
- El JS de la plantilla comparte ámbito con `ayuda.js`: no declarar `W`, `L`, `T0`, `DUR`, `RAIZ`, `tl`…
- Con `.num` (cifras tabulares) un año grande deja un hueco junto al 1 («201 8»). Las cifras de Inter Tight son
  proporcionales si no se pide otra cosa; para un cuentakilómetros, cada columna va a su sitio con el avance medido de
  cada cifra (`videos/01-flujo-de-caja/escenas/salto.html`).
- `check` da por solapados los textos que se tapan a propósito (una carta bajo un velo, las columnas de cifras que se
  rozan): `data-layout-allow-overlap` en ese bloque; si una capa opaca tapa del todo el texto de debajo, mejor ocultarlo.
- Plantillas de la segunda parte del vídeo 1 que se pueden reutilizar: el mapa que se enciende y se apaga (`mapa`,
  `apagon`, con `mapa.py`), el depósito con agujero (`deposito`), la tabla de 13 semanas (`regla2`), el ciclo que
  encoge (`regla3`), el cuadrado a escala (`liquidacion`) y la carta recreada (`carta`).
