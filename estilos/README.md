# Pruebas de estilo: «El faro» en tres estilos

Tres vídeos de 10 s a 1920 × 1080 y 30 fps, hechos con HyperFrames para elegir el estilo de la casa.
Los tres cuentan lo mismo con la misma voz y las mismas imágenes; cambian la puesta en escena, la
tipografía, el tratamiento de la imagen, la música y los efectos de sonido. Los estilos están descritos
en [docs/estilo.md](../docs/estilo.md).

![Comparativa](../docs/resultados/comparativa-estilos.jpg)

Narración (Piper, `es_AR-daniela-high`, a 1,08): *«Cabo Norte, mil ochocientos noventa y uno. Un faro se
enciende. Desde entonces, ni una sola noche a oscuras.»* Empieza en 0,8 s y dura 7 s; el texto en
pantalla cae en la palabra que lo dice, con los tiempos que da `voz/narrar.py`.

## Repetirlas

```bash
./instalar.sh                         # voz, imagen y edición (HyperFrames y modelos de apoyo)
estilos/preparar.sh                   # recursos: unos 17 min en una sesión nueva
estilos/preparar.sh --render          # además los tres vídeos y sus versiones de entrega
cd estilos/estilo-a && ../../video/hf.sh check --json     # revisar uno
```

Los recursos no se versionan: `preparar.sh` los regenera en `salidas/estilos/` a partir de
`recursos/` (prompts y semillas de las imágenes, guion de la voz y descripciones de la música) y los
copia en el `assets/` de cada proyecto. Los efectos de sonido salen de BigSoundBank (CC0) y de la
biblioteca que trae HyperFrames (licencia de Pixabay).

## Qué hace cada una

| | A. Editorial cinematográfico | B. Suizo cinético | C. Collage documental |
| --- | --- | --- | --- |
| Estructura | 3 tomas con un barrido y un destello de luz entre ellas | 3 pantallas en la retícula, unidas por un cuadro que crece y un iris | Un solo plano: la cámara recorre una mesa de archivo |
| Imagen | Las tres planchas a sangre, en 2.5D por capas (WebGL propio) | Las planchas en módulos con trama de impresión de dos tintas | Fotos impresas con borde y nota a pluma; carta náutica y brújula recortada |
| Tratamiento | Etalonaje, viñeta, grano y «ventana» para el texto, en el shader | `monoScreen` de HyperFrames con la paleta (cobalto/papel, tinta/naranja) | `vintage-wash` de HyperFrames con grano y viñeta |
| Tipografía | Cormorant Garamond 500 y cursiva; Hanken Grotesk 600 | Archivo variable: el ancho va de 62 a 100 al aparecer cada palabra | IM Fell English; Special Elite (máquina); La Belle Aurore (pluma) |
| Texto | Año cifra a cifra, subtítulo de gris a tinta, título palabra a palabra con desenfoque | El año rueda como una tragaperras; palabras que suben desde su máscara | Etiqueta tecleada letra a letra, sello, nota que se escribe, título que se imprime |
| Música (MusicGen) | Ambiente de cine, cuerdas graves y piano, 70 BPM | Electrónica mínima, 120 BPM; los cortes caen en el pulso | Guitarra y piano de documental, 90 BPM |
| Sonido | Sirena de niebla, olas, barrido, cerilla al «enciende», golpe en el título | Teclas en cada cifra, barridos, «pop» del cuadro y de la luz, golpe final | Papel, cinta adhesiva, máquina de escribir, sello, pluma, campanilla |
| Render (10 s) | 2 min 1 s | 2 min 31 s | 3 min 14 s |

Volumen de entrega igualado a −15 LUFS con `video/entregar.sh` (pico real entre −1,1 y −1,4 dBTP).

## Lo aprendido al hacerlas

- **2.5D**: desplazar una sola imagen con su profundidad dobla el borde del sujeto. Funciona separarlo
  en capas (`imagen/capas25d.py`): sujeto recortado por la profundidad y fondo con el hueco
  rellenado. Un margen de 30 px se lleva detalles finos, como una barandilla, que el mapa no recoge.
- **Texto sobre imagen**: el comprobador de contraste de HyperFrames encuentra los textos que se leen
  mal. En A se resolvió oscureciendo esa zona en el etalonaje, sin poner una caja detrás.
- **Desenfoque de movimiento** (`data-motion-blur`): se sale de las máscaras con `overflow: hidden`.
  Las cifras que ruedan van sin él (`data-motion-blur="off"`). En una cámara que recorre toda la
  escena, con el obturador a 90° (`data-motion-blur-shutter="90"`) el barrido se sigue leyendo.
- **Falsos avisos de `check`**: un fondo que crece con `scaleX` o queda recortado por un `clip-path`
  no cuenta como fondo, así que da contraste 1:1. Se evita metiendo el texto dentro del fondo y quitando
  el recorte cuando ya cubre todo. El texto letra a letra cuenta cada letra como una palabra; se marca
  con `data-layout-ignore`.
- **Primer fotograma**: es la miniatura en redes, así que debe tener ya la imagen clave. En C, la
  primera foto empieza en el aire.
- `media-treatment --apply` añade atributos `data-hf-id` a todo el HTML: al editar después, buscar
  por `id` con expresiones regulares, no por la etiqueta exacta.
- **Velocidad** (sesión 2): el WebGL va por software, así que cada muestra de textura cuenta. El shader
  de A tomaba 16 muestras por píxel también sin desenfoque; con una sola, el render de los 10 s pasó de
  195 s a 100 s en la misma máquina y con la misma imagen. Medido en `docs/bitacora.md` (sesión 2).
- Para lanzar un render en segundo plano, llamar al binario de HyperFrames directamente. Lanzado con
  `nohup` a través de `video/hf.sh`, se canceló con `render_cancelled_parent_exited`; en primer plano
  el atajo funciona.
