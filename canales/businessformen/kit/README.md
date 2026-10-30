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
