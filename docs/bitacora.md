# Bitácora

## Sesión 1 — 29 de octubre de 2026

Punto de partida: ninguna herramienta instalada. Objetivo final: vídeos largos desde un prompt.

### 1. Animación por código → vídeo

- Primer ejercicio: un anuncio de 5 s en estilo motion graphics, para otro proyecto (no está en este repositorio).
- La técnica que funcionó: una escena en canvas cuyo dibujo depende solo del tiempo, `dibujar(t)`.
  Chromium (Playwright) pinta cada cuadro y ffmpeg une los PNG. Es exacto y repetible.
- Desenfoque de movimiento: dos subcuadros por cuadro (120 por segundo para 60 fps), promediados con
  el filtro `tmix` de ffmpeg. Equivale a un obturador de 180°.
- Codificación: H.264 CRF 16 `preset slow`, yuv420p con etiquetas BT.709, AAC a 192 kbps y `+faststart`.
- Coste: 5 s a 1080p60, unos 40 s de render.
- Quedó como `video/renderizar_canvas.mjs` y `video/plantilla_titulo.html`.

### 2. Música y efectos sintetizados

- Con numpy: bombo, charles, palmas, bajo, pad de acordes, campanas y barridos de ruido con filtro
  móvil, más reverb por convolución. Los golpes caían en el pulso de la animación (125 BPM).
- Volumen: la primera mezcla dio −9,8 LUFS, demasiado comprimida por la saturación. Normalizando antes
  de saturar quedó entre −12 y −13 LUFS.
- Quedó como `audio/musica.py` (fondo de cualquier duración) y `audio/mezclar.py` (agache y −14 LUFS).

### 3. Voz con Piper

- Piper 1.8.0 en un entorno de Python aparte; las voces salen de `rhasspy/piper-voices` en Hugging Face.
- Al principio no bajaban: la página de Hugging Face respondía, pero los archivos grandes salen de su
  CDN (`us.aws.cdn.hf.co`), que hubo que añadir a la red permitida del entorno.
- Voces probadas: `es_AR-daniela-high` (ritmo natural) y `es_MX-claude-high` (lenta; hay que acelerarla
  un 20 % con `--velocidad 0.8`). El usuario aún no ha elegido.
- La pronunciación se comprueba antes de sintetizar con el fonetizador de Piper:
  `piper.phonemize_espeak.EspeakPhonemizer().phonemize('es-419', texto)`. Un nombre propio raro se lee
  bien o se escribe como suena.
- Mezcla: con la música al 35 % mientras habla la voz (agache del 65 %, ataque de 8 ms, liberación de
  180 ms), la voz queda unos 10 dB por encima. Con un agache del 55 % fueron 8 dB, y sin normalizar la
  voz solo 3 dB.
- Quedó como `voz/narrar.py`, que además devuelve el inicio y el fin de cada frase.

### 4. Investigación: imágenes sin GPU

- Método: búsquedas web, README de repositorios públicos leídos por `raw.githubusercontent.com` y
  metadatos de Hugging Face (licencia y si piden cuenta) por su API.
- Descubrimos herramientas y modelos posteriores a la fecha de corte de Claude: FLUX.3 Image Klein
  (15-oct-2026), FLUX.2 klein (ene-2026), Iris-3B y Z-Image-Turbo, y que FastSD CPU y
  stable-diffusion.cpp ya los soportan.
- Descartado: servicios en internet (el texto saldría del entorno) y modelos que no caben en 15 GB
  (FLUX.1-schnell en OpenVINO, Qwen-Image, MOSS-Image, Lens).
- El control de seguridad bloqueó compilar stable-diffusion.cpp hasta que el usuario lo autorizó.
- Detalle y fuentes: [investigacion-imagenes.md](investigacion-imagenes.md).

### 5. Pruebas reales de imagen

- Tres prompts por cinco combinaciones de modelo y motor, a 512 px y semilla 42.
- Lo principal: con el mismo modelo, OpenVINO fue unas 8 veces más rápido que stable-diffusion.cpp.
- FLUX.3 Image Klein: 37 s por imagen. SDXS: 0,5 s. Las estimaciones previas fallaron en los dos sentidos.

![Comparativa](resultados/comparativa.jpg)

### 6. Este repositorio

- Herramientas fuera del repositorio, en `~/herramientas-videos`, instaladas por `instalar.sh` con
  versiones fijadas.
- Probado: instalación desde cero en una carpeta nueva (voz e imagen), generación de imagen y voz con
  ella, y reejecución sobre lo ya instalado (7 s).
- `imagen/servidor.py` existe porque la API de FastSD devuelve JPEG con pérdida.
- En formato de vídeo, 768 × 432, FLUX.3 tarda 53 s por imagen:

![Ejemplos 16:9](resultados/ejemplos-16x9.jpg)

### 7. Nuevo rumbo: edición de nivel agencia

- El usuario no quiere vídeos de «imagen + voz»: quiere edición profesional, de agencia de branding.
  Las imágenes son un recurso del montaje; lo que manda es qué pasa en pantalla, cuándo, dónde y cómo.
- Investigación (web y repositorios públicos) en [investigacion-edicion.md](investigacion-edicion.md).
  Hallazgo principal: **HyperFrames** (HeyGen, Apache 2.0, 2026): vídeo como HTML + GSAP, render
  determinista, ~450 bloques, y guías de motion medidas cuadro a cuadro en películas profesionales.
- Comprobado sin instalar: funciona con nuestro Chromium (`HYPERFRAMES_BROWSER_PATH`), la telemetría
  se apaga con `HYPERFRAMES_NO_TELEMETRY=1`, y Node 22 y FFmpeg ya están.
- Imagen: FLUX.3 Image Klein sigue siendo el mejor viable. Qwen-Image-2.1 e Ideogram 4 lideran los
  rankings pero aquí no caben o tardarían unos 20 min por imagen.
- Tres estilos propuestos en [estilo.md](estilo.md), con fotogramas de estilo hechos aquí. Recomendado:
  **A. Editorial cinematográfico**, con B (suizo) y C (collage) como modos. Pendiente de que el usuario elija.
- Aprendido al hacer los fotogramas:
  - La composición se pide en el prompt de la imagen («sujeto en el tercio derecho, espacio negativo a la
    izquierda»), no se fuerza después recortando: escalar una plancha de 1024 px para encuadrarla la ablanda.
  - Un objeto sin recortar deja su fondo como un rectángulo: para el collage hacen falta recortes reales (BiRefNet).
  - Revisar cada fotograma buscando choques de texto con imágenes y frases destacadas partidas.
  - FLUX.3 a 1024 × 576 tarda unos 90 s por imagen con el modelo cargado.

### 8. Pruebas de los tres estilos

- El usuario pidió una prueba de 16:9 y 10 s en cada estilo para decidir, y dio permiso para instalar lo
  necesario. Resultado en [estilos/](../estilos/README.md): «El faro», con la misma historia, voz e
  imágenes en los tres; cambian la puesta en escena, la tipografía, el tratamiento, la música y el sonido.

![Comparativa de estilos](resultados/comparativa-estilos.jpg)

- **HyperFrames 0.8.216** instalado con npm en `~/herramientas-videos/hyperframes` (`./instalar.sh edicion`).
  `video/hf.sh` lo lanza con la configuración del entorno. Render de 10 s a 1080p30 en esta CPU:
  A 2 min 1 s (WebGL por software), B 2 min 31 s, C 3 min 14 s (el desenfoque de una cámara que gira y
  escala obliga a capturar con capturas de pantalla, más lentas). `check` y `snapshot` tardan 7–17 s.
- **Imágenes**: FLUX.3 a 1280 × 720 tardó 138–211 s por imagen. «Negative space for a title» hizo que FLUX
  escribiera letras inventadas en la imagen: no nombrar el texto en el prompt y añadir «no text».
- **Profundidad**: Depth Anything V2 Small (Apache 2.0, ONNX) da mapas limpios en 3 s por imagen
  (`imagen/profundidad.py`). Desplazar una imagen con su profundidad dobla el borde del sujeto; se
  resolvió en capas (`imagen/capas25d.py`, OpenCV del entorno de FastSD): 1,5 s por imagen.
- **Recortes**: BiRefNet lite (MIT, ONNX) recorta la brújula pedida «sobre fondo blanco» en 27 s
  (`imagen/recortar.py`). HyperFrames trae `remove-background`, sin probar.
- **Voz**: Whisper (el `transcribe` de HyperFrames) entendió «Caucao» y se desvió hasta 0,8 s en los
  tiempos. Piper 1.8 da la alineación de fonemas si su entorno tiene `onnx`: `voz/narrar.py` ahora devuelve
  el inicio y el fin de cada palabra, exactos.
- **Música**: MusicGen estéreo small (Meta, CC BY-NC: no comercial) en el entorno de FastSD:
  12 s de audio en 50–55 s (`audio/musica_ia.py`). Los tempos pedidos salieron bien (120 y 90 BPM medidos).
  La guía de sonido de HyperFrames desaconseja sintetizar música con código: por eso un modelo.
- **Efectos**: la biblioteca de HyperFrames (21 sonidos, licencia de Pixabay) no tiene papel, cinta ni
  sello. Freesound, Pixabay y la web de Wikimedia están bloqueados o limitados (403 y 429), y la búsqueda
  de Openverse no responde. **BigSoundBank** sí llega y es CC0: `audio/efectos.py` busca, comprueba la
  licencia de cada sonido y baja WAV. `audio/tecleo.py` arma una máquina de escribir con teclas reales.
- **Fuentes**: de Google Fonts vía jsDelivr (`@fontsource`): Cormorant Garamond, Hanken Grotesk, Archivo
  variable, IM Fell English, Special Elite y La Belle Aurore.
- **Mezcla**: con las pistas separadas en HyperFrames (agache con `data-automation`, limitador en la voz)
  salieron −16,2, −15,5 y −17,9 LUFS. `video/entregar.sh` los iguala a −15 LUFS y baja el peso (A pasó de
  75 MB a 23 MB: el grano dispara el bitrate).
- **Memoria**: cargar BiRefNet mientras el servidor de imágenes tenía FLUX cargado llenó los 15 GB y el
  sistema mató el servidor. Apagarlo (`generar.py --parar`) antes de otros modelos.
- Revisión con `check` de HyperFrames: encontró textos con poco contraste sobre el cielo (resuelto con una
  «ventana» de etalonaje), tipografía por debajo de 28 px (el mínimo legible en un móvil), un subtítulo
  que no daba tiempo a leer y un primer fotograma vacío. También da falsos avisos; están en el README de
  `estilos/`.
- Después de entregar se corrigieron tres detalles en el repositorio que no están en los vídeos enviados:
  la firma de A entra en 7,7 s en vez de 8,3 s, y en B se quitó el recorte del iris al abrirse y se
  marcaron las máscaras del pie.

### 9. La voz principal

- El usuario quería una voz masculina de español latinoamericano neutro; daniela (acento argentino) se
  queda como segunda voz. Se buscó en Hugging Face (modelos de voz en español ordenados por tendencia,
  «me gusta» y descargas) y se probó la misma frase con cada candidata, igualada a −16 LUFS:

| Voz | Tono medio (F0) | Tiempo (frase de 7 s) | Notas |
| --- | --- | --- | --- |
| Piper `es_MX-claude-high` | 187 Hz | 6,5 s | aguda; Whisper entendió «vio» por «guió» |
| Piper `es_MX-ald-medium` | 146 Hz | 2,9 s | igual con «guió» |
| **Supertonic-3 M1** | 134 Hz | 2,8 s | **la elegida** |
| Supertonic-3 M2 / M3 / M4 / M5 | 88 / 98 / 119 / 95 Hz | 2,4–3,7 s | M2 la más grave |
| Kokoro-82M `em_alex` / `em_santa` | 132 / 138 Hz | 2 s | con espeak `es-419` para el seseo |
| VoxCPM2 (diseño de voz por descripción) | — | 47–78 s, más 68 s de carga | 2B, 5 GB; corre en CPU en bf16 |

- **Elegida: Supertonic-3 M1** (Supertone, ONNX). Muy rápida: unas 2,5 veces más rápida que el tiempo
  real. Ya es la voz por defecto de `voz/narrar.py`; `./instalar.sh voz` la instala con sus 10 voces.
- **Licencia de Supertonic-3: Open RAIL-M.** Permite uso comercial, pero su anexo A prohíbe difundir el
  contenido sin avisar de forma clara de que está generado por una máquina: **cada vídeo con esta voz
  debe decirlo** (descripción o rótulo).
- Tiempo de cada palabra: Supertonic no lo da. `voz/alinear.py` hace alineación forzada CTC con un
  wav2vec2 en español (`jonatasgrosman/wav2vec2-large-xlsr-53-spanish`, Apache 2.0, 1,3 GB): frente a la
  alineación exacta de Piper, 17 ms de error medio y 40 ms como máximo en el inicio de cada palabra.
  Whisper (whisper.cpp de HyperFrames) quedó en 160 ms de media y 630 ms como máximo; con DTW (que solo
  funciona con `-nfa`, sin flash attention), en 135 ms y siempre tarde.
- `narrar.py` con M1: la narración de «El faro» (7 s) sale en 14 s con síntesis y alineación.
- El control de seguridad bloqueó instalar Kokoro, Supertonic y VoxCPM2 hasta que el usuario los
  autorizó por su nombre. phonon-40m-es (solo español, 40M) pide cuenta de Hugging Face.
- Se borraron VoxCPM2 y Kokoro para liberar disco (quedaban 3,9 GB). Si un canal futuro pide otra voz, se
  reinstalan: `uv pip install kokoro==0.9.4 "misaki[en]"` o `voxcpm==2.0.3` con torch 2.8 de CPU.

### Decisiones

- Imagen: FastSD CPU con OpenVINO. Calidad: FLUX.3 Image Klein. Bocetos: SDXS. Si el uso pasa a ser
  comercial: FLUX.2 klein 4B (Apache 2.0).
- **Estilo de la casa: A, editorial cinematográfico.** Lo eligió el usuario al ver las pruebas: «le diste
  vida a las imágenes». B y C quedan en `estilos/` por si un tramo los pide como modos.
- **Voz principal: Supertonic-3 M1.** Segunda voz: Piper `es_AR-daniela-high`. Todo vídeo con Supertonic
  avisa de que la voz está generada por máquina (licencia Open RAIL-M).
- Edición: HyperFrames + GSAP. Apoyo: Depth Anything V2 Small (2.5D), BiRefNet lite (recortes),
  MusicGen estéreo small (música, no comercial) y BigSoundBank (efectos CC0).
- Todo en local, sin APIs externas.
- Prompts de imagen en inglés, descriptivos.

### Pendiente

- ~~Definir el nicho de los vídeos y la forma de trabajar~~ (hecho en la sesión 2).
- Idea del usuario para más adelante: con el sistema montado, varios canales de nichos distintos, cada uno
  con su voz (y quizá su modo de estilo). Ahora se elige la voz del nicho principal; el sistema debe dejar
  elegir la voz por canal.

## Sesión 2 — 29 de octubre de 2026, noche

### 1. Nicho y primer vídeo

- Nicho del primer canal: **historia y misterios**. Lo eligió el usuario entre cuatro (con historias de
  negocios, ciencia y casos sin resolver): encaja con el estilo A y FLUX dibuja bien épocas, lugares y
  objetos sin depender de caras ni de fotos reales.
- Primer vídeo: **el mecanismo de Anticitera**, de 8–10 min, porque deja animar engranajes y diales con
  gráficos vectoriales, no solo con imágenes. Fuentes reunidas: Wikipedia (inglés y español), el modelo
  de la UCL de 2021 (Scientific Reports: 30 engranajes en 82 fragmentos, un tercio del aparato), el anillo
  de 354–355 agujeros de Glasgow (2024; Freeth lo discute) y el preprint de Mar del Plata de 2025 sobre
  atascos (sin revisar; sus autores piden cautela).

### 2. Velocidad: dónde se va el tiempo y qué se ganó

El usuario pidió, antes de empezar, hacer el proceso más rápido sin bajar la calidad y sin cambiar la
forma de trabajar. Todo se midió aquí con la prueba de 10 s del estilo A.

- **La máquina cambia entre sesiones.** Esta era un Xeon Cascade Lake a 2,8 GHz (4 núcleos, AVX-512 VNNI,
  **sin AMX**); la de la sesión 1 tenía AMX. FLUX.3 a 1280 × 720 tardó aquí 328 s por imagen (4 pasos de
  ~75 s, el texto 16 s y el VAE unos 10 s), frente a 138–211 s en la sesión 1. MusicGen, 69–96 s por 12 s.
- **Disco al reanudar.** La sesión volvió de una copia guardada: la primera lectura de cada archivo iba a
  10–40 MB/s, y el servidor tardó 17 min en dar la primera imagen (11 de ellos esperando al disco). Un
  archivo ya leído se lee después a 2,2 GB/s. `./instalar.sh precargar` lee las herramientas (15 GB) en
  bloques grandes, cuatro archivos a la vez: 5 min 51 s, en segundo plano.
- **Render del estilo A: de 195 s a 100 s por cada 10 s de vídeo, con la misma imagen** (en PNG sin
  comprimir, un 0,001 % de los píxeles cambia en 1 nivel). El shader de las planchas tomaba 16 muestras
  por píxel también sin desenfoque; ahora toma una. Con el cuadro más barato, HyperFrames pasa solo de 1
  a 2 Chromium (calibra el número según lo que tarda un cuadro): el shader viejo con 2 a la fuerza, 168 s.
  - 3 y 4 Chromium no mejoran (105 y 104 s): con 2, la CPU ya va llena.
  - Sin las planchas, el texto solo tarda 25 s: el WebGL por software (SwiftShader) sigue siendo unas tres
    cuartas partes del coste.
  - A 24 fps, 87 s (−14 %). `--quality draft`, para revisar: 72 s. `high` (preset fast) y las texturas en
    RGBA no cambian nada.
- **Entrega sin recomprimir.** Renderizar ya con `--crf 20` y entregar con `entregar.sh … copiar`:
  2,2 s por cada 10 s, frente a 47 s con la recompresión en preset slow (unos 40 min para 9 min de
  vídeo). Contra una referencia sin pérdida (`--crf 0`), la calidad sube: PSNR 41,3 dB y SSIM 0,949
  frente a 40,5 dB y 0,941 de render a CRF 16 más recompresión. Pesa algo más: 30 MB frente a 23 por
  cada 10 s. Si hay que recomprimir, preset medium: 27 s con la misma calidad que slow. Las pasadas de
  volumen ya no decodifican la imagen (`-vn`).
- **FLUX.3** (la misma semilla y el mismo prompt que `faro.png`, comparados a tamaño real):
  - 3 pasos: 246 s en vez de 328, muy parecida, con algo menos de textura en el cielo y el mar. 2 pasos:
    175 s, claramente más plana y blanda. Se queda en 4 salvo que el usuario decida otra cosa.
  - Caché de compilación de OpenVINO (FastSD la desactiva): la carga baja de 69 s a 14 s, pero ocupa
    5,1 GB de disco. No se activa: basta con no recargar el modelo a mitad de un trabajo.
  - La cuantización dinámica de OpenVINO ya está activa con el mejor valor (grupo 32: 19 s por paso a
    512 px; sin ella, 29 s; con 128, 31 s).
  - El coste crece más que los píxeles: 18,5 s por paso a 512 × 512 y 72 s a 1280 × 720 (3,5 veces los
    píxeles, 4 veces el tiempo). Generar a 960 × 544 y ampliar ×2 con EDSR: ver el apartado 3.
- **Música**: MusicGen en lote, 4 pistas de 10 s a la vez en 123 s (31 s cada una) frente a 53,5 s una
  sola. Conviene generar todas las piezas de un vídeo juntas: `audio/musica_ia.py` ya las agrupa en lotes
  de 4 (`--lote`). Las pistas cambian respecto a generarlas sueltas con la misma semilla.
- **Voz**: Supertonic M1 dijo 58 s de narración en 41 s. La alineación pasaba la pista entera de una vez
  por wav2vec2, cuya atención crece con el cuadrado de la duración: 9 min pedirían unos 46 GB de RAM.
  Ahora va frase a frase (`alinear.py --frases`, que usa `narrar.py`): 20 s frente a 28 s en 1 min, con
  los mismos tiempos (inicios a 6 ms de media, 17 ms como máximo) y mejor el final de la última palabra.
- **Servidor de imágenes**: `generar.py --parar` no lo apagaba mientras generaba (atendía una petición
  cada vez y no contestaba a `/estado`) y se quedó encendido con 12 GB mientras arrancaban otros modelos.
  Ahora contesta siempre y sigue generando de una en una.
- Visto y no probado: renderizar en la nube de HeyGen o en Lambda (sacaría el proyecto de la máquina) y
  MusicGen convertido a OpenVINO (otro modelo que bajar, sin cifras publicadas). Mesa llvmpipe en lugar de
  SwiftShader: probado en el apartado 3.

### 3. EDSR y llvmpipe (pruebas pedidas por el usuario)

El usuario eligió **4 pasos y 30 fps** (la calidad manda) y pidió probar el EDSR y llvmpipe.

- **EDSR** (el ampliador ×2 de FastSD, `rupeshs/edsr-onnx`, 5,5 MB; `imagen/ampliar.py`): 7 s desde
  960 × 544 y 12,5 s desde 1280 × 720. FLUX a 960 × 544 tarda 166 s (pasos de 38 s), la mitad que a
  1280 × 720. Comparado con la misma imagen (la de 1280 reducida) y midiendo la nitidez con la varianza
  del laplaciano en la linterna y el muro:
  - camino de ahora (1280 + Lanczos y máscara de enfoque): 326 y 147;
  - **1280 + EDSR: 397 y 181**, más nítida y limpia por 11 s más;
  - 1120 + EDSR: 245 y 92; 960 + EDSR: 219 y 64 (960 + Lanczos: 116 y 44).
  - Para ganar tiempo no sirve: desde 960 o 1120 recupera los bordes pero no la textura fina, la misma
    clase de pérdida que con 3 pasos. Sí sirve para ampliar las planchas de 1280.
  - En «manos» y «haz», 1280 + EDSR frente al camino de ahora: piel 210 frente a 160, latón 204 frente a
    174, faro y reflejos 272 frente a 201, cielo 329 frente a 242; sin halos ni artefactos. Las estrellas
    siguen todas, pero salen como puntos más finos y algo menos brillantes (sin el halo de la máscara de
    enfoque): en un cielo nocturno que deba leerse, reforzarlas en el etalonaje.
- Al reanudar la sesión otra vez, `./instalar.sh precargar` tardó 55 s: el disco ya estaba casi todo en local.
- **llvmpipe**: Ubuntu responde (`archive.ubuntu.com`), así que se instalaron `libegl1` y `libegl-mesa0`
  (la parte EGL del Mesa 25.2.8 de la máquina). El shader de las planchas a 1920 × 1080, aislado: 51 ms
  por cuadro frente a 139 ms de SwiftShader (con desenfoque, 194 frente a 394).
  - En HyperFrames, con `--browser-gpu` (llvmpipe para todo): estilo A 83,5 s frente a 94 s, estilo B
    118 s frente a 138 s, pero solo texto **36 s frente a 25 s**: dibujar el texto y el CSS con llvmpipe
    es más lento que en la CPU.
  - Con `video/chrome-llvmpipe.sh`, que deja el WebGL en llvmpipe y dibuja y compone la página en la CPU:
    **estilo A 70 s, estilo B 114 s, solo texto 24 s**. Los cuadros salen iguales salvo el dibujo del grano
    (el azar del shader usa `sin()`, que cada motor calcula a su manera): sin grano, PSNR 48–50 dB y 6
    niveles como mucho; ningún píxel del texto cambia más de 30 niveles.
  - En modo «hardware» la calibración de HyperFrames elige 1 Chromium (85 s): `hf.sh` pone 2 por cada 4
    núcleos si no se pide otra cosa.
- **Preset fast** (`--quality high --crf 20`): la misma calidad que medium contra una referencia sin
  pérdida (PSNR 41,205 dB los dos, SSIM 0,9480 y 0,9479), un 3 % más de peso y el render de 72,5 s a 65,6 s.
- Total en esta máquina: **los 10 s del estilo A, de 195 s al principio de la sesión a 66 s.**

| 9 min de vídeo en esta máquina (35 planchas, 6 piezas de música de 30 s) | Al empezar la sesión | Ahora |
| --- | --- | --- |
| Cargar FLUX en una sesión reanudada | 11 min | en segundo plano (precarga) |
| Planchas FLUX.3, 4 pasos, 1280 × 720 | 191 min | 191 min (+7 min si se amplían con EDSR) |
| Voz y tiempos de palabras | no cabía en la RAM | ~9 min |
| Música | 17 min | ~25 min (con pistas de 30 s, medido en la apertura; en lote) |
| Render a 30 fps | 175 min | ~56 min (6,2 s por segundo, medido en la apertura) |
| Entrega | ~40 min | ~2 min |
| **Total de máquina** | **~7,5 h** | **~4,8 h** |

Las planchas son ya el 70 % del tiempo y, con 4 pasos a 1280 × 720, solo bajan en una máquina con AMX
(138–211 s por plancha en la sesión 1, frente a 328 s aquí). Mientras se generan, Claude escribe las
composiciones, así que ese tiempo no se suma al suyo.

### 4. La apertura de «El mecanismo de Anticitera» (34 s)

El usuario pidió hacerla de una vez, sin paradas. Proyecto en `videos/anticitera/` (guion, prompts, semillas
y `preparar-apertura.sh` para rehacerlo todo; la composición en `apertura/`, con SPEC.md, STORYLINES.md y
REVIEW.md). Datos comprobados en la Wikipedia: Kontos y los buzos de Symi, 1900, 45 m; el mecanismo, sacado en
1901 como un solo bulto y visto con un engranaje en 1902; la rueda mayor, de 13 cm y 223 dientes.

- Forma: un zoom continuo en el que cada plano abre el siguiente (el rayo trae el amanecer, el barrido baja
  al buzo, la oscuridad del fondo descubre las estatuas, un oscurecido lleva al bronce, el escáner revela la
  rueda y se atraviesa su buje). El título solo lo dice la pantalla, tras la última palabra de la voz.
- El escáner revela los contornos de la propia plancha (`lineas_rueda.py`: bordes de Canny solo en la corona,
  los radios y el buje), así que cuadra con la imagen por construcción. El tren de ruedas del título usa
  dientes del mecanismo real (64, 38, 48 y 24), engranados y girando con sus relaciones.
- Tiempos en esta máquina (sin AMX): voz 29,7 s en 43 s; música, 2 variantes de 30 s en lote en 573 s (2,2
  veces lo que salía extrapolando desde pistas de 10 s); 5 planchas de 312–375 s; EDSR 11–12,5 s cada una;
  profundidad y capas 2–2,5 s. Recursos en total: 38 min 40 s. Render: 34 s en 210 s (6,2 s por segundo de
  vídeo, llvmpipe y 2 Chromium), 86 MB; la entrega, a −14,9 LUFS copiando el vídeo.
- La revisión (check, `snapshot --review`, costuras y hoja de móvil) encontró y se corrigió: la franja
  borrosa de las capas 2.5D en la isla y las estatuas (`capas25d.py --suavidad 0.012 --margen 12`), flechas
  que parecían barras, una línea guía sobre un rótulo, un dato bajo una rueda, el empuje lento del fondo al
  final (un tic de vídeo generado), dos tiempos de lectura cortos, la tormenta inicial demasiado floja
  (−34,6 dB de media frente a −18,5 con la voz: subida 8–10 dB) y la música solo 7 dB bajo la voz (ahora ~10).
- Música: la variante 1, elegida midiendo (la 2 tenía el 71 % de la energía bajo 150 Hz, inaudible en un móvil).
- `subtitulos.srt` para YouTube, sacado de los tiempos de cada palabra (`subtitulos.py`, sin palabras sueltas).
- Aviso de la licencia de Supertonic en pantalla al final: «Voz sintética generada por IA».
- Al reanudar la sesión otra vez, la precarga tardó 7 min 32 s.

### Decisiones (sesión 2)

- Nicho: historia y misterios. Primer vídeo: Anticitera, de 8–10 min.
- **FLUX.3 con 4 pasos a 1280 × 720 y vídeo a 30 fps** (elección del usuario).
- Render: el shader de una muestra sin desenfoque; WebGL con llvmpipe y la página en la CPU
  (`video/chrome-llvmpipe.sh`, lo pone `hf.sh` si está el EGL de Mesa); 2 Chromium por cada 4 núcleos;
  el render final con `--quality high --crf 20` y la entrega copiando el vídeo.
- Al reanudar una sesión, `./instalar.sh precargar` en segundo plano.
- Orden de un vídeo largo, cargando cada modelo una sola vez: guion → voz y tiempos → música (todas las
  piezas en un lote) → planchas de FLUX en un lote, en segundo plano mientras Claude escribe las
  composiciones → profundidad y capas → render por capítulos → entrega.

### Pendiente (sesión 2)

- Que el usuario vea la comparación y diga si las planchas se amplían con EDSR (más nitidez, 11 s más por
  plancha) en lugar de con Lanczos y máscara de enfoque.
- Un kit de componentes del estilo A (plancha 2.5D, rótulos, capítulos, subtítulos, datos) que se rellene
  desde el guion, para escribir 9 minutos de composiciones sin hacerlas a mano una a una; y, si el usuario
  quiere, subagentes en paralelo por capítulos (la guía de HyperFrames lo recomienda a partir de 6 escenas).

## Sesión 3 — 30 de octubre de 2026

El usuario vio la apertura («estuvo genial») y pidió el vídeo completo, trabajando sin paradas mientras él no
estaba. El trabajo de la sesión 2 estaba en otra rama sin unir: se trajo por avance rápido.

### 1. La máquina y los tiempos

- Esta vez la CPU tiene AMX (como en la sesión 1). FLUX.3 a 1280 × 720 con 4 pasos: **82–98 s por plancha** (85–92 lo
  normal; 172 s si coincide con la voz). En la sesión 2, sin AMX, 328 s. EDSR: 6 s por plancha (12,5 s en la 2).
- MusicGen, pistas de 30 s: 2 a la vez en 297–305 s; 4 a la vez en 410 s (1070 s compartiendo la CPU).
- La sesión se reanudó a mitad desde una copia guardada: todo lo que había en disco siguió ahí (planchas, música),
  pero no los procesos. La precarga tardó 8 min 50 s; los lechos de música, leídos en frío, 5 min 21 s.

### 2. La voz, reproducible

- **Supertonic no era determinista**: parte de `np.random.randn` sin semilla y cada ejecución daba otra toma (en la
  apertura, palabras hasta 0,3 s más tarde y 0,4 s más de duración). `voz/supertonic_frases.py` fija ahora la semilla
  de cada frase con el CRC32 de su texto: dos ejecuciones dan el mismo WAV, byte a byte.
- Para no tocar la apertura ya aprobada, `voz/ajustar.py` estira o encoge cada tramo entre palabras ancla (atempo de
  ffmpeg, sin cambiar el tono) hasta los tiempos de la composición: 8 anclas, todos los tramos a menos de un 3 %.
  Las anclas que pedían un 10–29 % se quitaron: se oiría.
- La narración de los ocho capítulos (1263 palabras, 8 min 26 s de voz) salió en 8 min 33 s, a la vez que FLUX.

### 3. Guion y datos

- Ocho capítulos tras la apertura: el olvido (1902–1951), cómo se miró dentro (Price, Karakalos, Wright, 2005), el
  frente, la Luna que acelera (perno y ranura), las espirales de la cara trasera, los planetas (UCL 2021), quién lo
  hizo y lo que queda sin saber (Glasgow 2024, Mar del Plata 2025). Unos 10 min con la apertura.
- Datos comprobados con búsquedas web; fuentes y cautelas en `videos/anticitera/FUENTES.md`. Los nombres difíciles se
  escriben como suenan para la voz («Prais», «Máikel Rait», «Glásgou») y los subtítulos los devuelven a su ortografía.

### 4. El kit del estilo A (`videos/anticitera/kit/`)

- `montar.py` arma cada capítulo como proyecto de HyperFrames desde una descripción corta (`montaje/capN.py`): tomas
  de plancha con su cámara y su paso (corte con oscurecido, barrido, oscuro, destello, zoom a través), rótulos
  (etiqueta, nombre, cifra con contador, dato con tachado, título, «a máquina», pie), líneas guía, gráficos y sonidos.
  **Todo se ancla a la palabra de la narración** (`w("palabra")`), así que rehacer la voz no descuadra nada; avisa de
  las palabras que salen más de una vez y de los rótulos que no dan tiempo a leer.
- `planchas.html`: el motor de la apertura con caché de texturas y saturación por plano. `ayuda.js`: los gráficos son
  función del tiempo (evento `hf-seek`), y pueden seguir la cámara de la plancha (una rueda dibujada sobre la de la
  lupa o la de la radiografía).
- Gráficos (`graficos/`): rueda, frente (rueda mayor, zodíaco, 365 días, Sol, Luna y esfera de fases), órbita de
  Kepler con marcas de igual tiempo, perno y ranura (±6,5°, ejes a 1,1 mm, montado sobre la rueda que gira), espirales
  (235 y 223 casillas, signos Σ y Η, dial de los juegos), tercio conservado, mapa (costas de Natural Earth, `mapa.py`),
  línea de tiempo, griego (ΠΛΑΝΗΤΑΙ, ΨΞΒ, ΨΜΒ), retrógrado, cosmos de anillos, anillo de 354 agujeros y atasco.
- Fallos encontrados al revisar: ids de rótulos repetidos entre tomas (todas comparten documento, y GSAP animaba los
  de otra), anclas en la primera aparición de una palabra repetida («cuenta», «fragmentos», «dos»), etiquetas en
  versalitas más anchas de lo calculado (unos 46 px por letra a 28 px con 0,32 em) que pisaban los dibujos, y patrones
  de trazos medidos en unidades de `pathLength` en vez de píxeles.

### 5. Recursos

- 28 planchas nuevas en 48 min con su EDSR, profundidad y capas. Se reencuadraron dos: Olimpia (unas gradas parecían
  modernas) y la radiografía (salió a la izquierda). Rodas (casas blancas y barcos de otra época) se cambió por el mapa.
- Música: una pieza por capítulo; **las piezas 4 y 5 tenían el 98 % y el 65 % de la energía bajo 150 Hz** y se
  rehicieron (0 % y 6 %). `audio/lecho.py` las extiende a la duración del capítulo con fundidos de potencia constante
  y las deja a −16 LUFS.
- Efectos CC0 de BigSoundBank: manivela, interruptor, zumbido de transformador, máquina de escribir, grillos, fuego,
  yunque, monedas, cajón, pasos.

### 6. Render y unión

- `check` sin errores en los nueve proyectos; los avisos que quedan, explicados en `videos/anticitera/REVIEW.md`.
- **Render de los nueve proyectos: 28 min 41 s** para 9 min 58,5 s de vídeo, a 2,7–3,0 s por segundo (la apertura,
  34 s en 103 s; los capítulos, con sus dibujos, 2,8 s por segundo). En la sesión 2, sin AMX, eran 6,2 s por segundo.
- `unir.sh` une sin recomprimir (1 min 16 s). Las partes salían de −18,2 a −20,8 LUFS (el capítulo IV, 2,6 dB más
  bajo que la apertura): ahora cada una se iguala a −19 LUFS en coma flotante antes de unirlas. El total, a −15,2 LUFS;
  el pico real, a −1,3 dB (con el tope de −1,5 de `entregar.sh` el AAC acababa en −0,9: `PICO=-2`).
- El vídeo: 1920 × 1080 a 30 fps, 17 956 cuadros, 1,1 GB. Subtítulos de todo el vídeo (244) en
  `videos/anticitera/subtitulos.srt`, con la ortografía real de los nombres, y los minutos de cada capítulo en
  `capitulos.txt`. Una versión a 720p para verlo en el móvil.
- Tiempo de máquina de todo el vídeo en esta CPU: planchas con su posproceso 48 min, voz 9 min, música unos 15 min,
  render y unión 30 min: **unas 1 h 45 min**, la mitad que lo estimado en la sesión 2 sin AMX (~4,8 h).

![Anticitera en 16 fotogramas](resultados/anticitera-hoja.jpg)

### Decisiones (sesión 3)

- EDSR para ampliar las planchas (lo recomendado en la sesión 2; la nitidez se nota en piel, latón y reflejos).
- Un proyecto de HyperFrames por capítulo, unidos sin recomprimir (`unir.sh`); el sonido de cada parte se recorta a la
  duración exacta de su vídeo antes de unirlo.
- Las imágenes son ilustraciones generadas: lo dice la tarjeta final, junto al aviso de voz sintética.

### 7. Revisión tras la primera entrega (y pausa)

- **Lo que dijo el usuario:** la edición bajó mucho respecto a la apertura de 35 s; en muchas partes no se entiende lo
  que se ve (una plancha con glifos inventados mientras la voz habla de letras griegas) y quedó en «imágenes con voz».
- **Diagnóstico** con `videos/anticitera/kit/auditar.py` (24 fotogramas por minuto, cada uno con lo que dice la voz en
  ese instante): imágenes que no corresponden a lo dicho, planos de 8 a 20 s sin que pase nada, letra pequeña para
  el móvil y esquemas finos y abstractos.
- **Reglas de la revisión:** un plano por idea (de 3 a 6 s); en cada plano, una acción anclada a la palabra que la
  nombra (un aro con guía y rótulo, un foco, el escáner, un golpe de zoom, un dibujo); etiquetas de 36 px y datos de
  46 px; trazos más gruesos; cambiar las planchas que contradicen a la voz.
- **Piezas nuevas** (en `graficos/`): `senal` (aros que siguen la cámara de la plancha, foco, guía y rótulo con halo
  oscuro, aro a trazos que cae), `rayos` con `kit/rayosx.py` (un escáner que deja ver una versión «radiografía» de la
  plancha con ruedas ocultas), `inscripcion` (letras griegas que aparecen con la luz rasante), `grieta` (grietas que se
  abren con ancho variable) y `lunas` (la Luna noche a noche, con pasos desiguales). `frente` nombra las agujas, enciende
  las fases una a una y se acerca a cada anillo cuando la voz lo nombra. `montar.py`: `D(..., tam=)`.
- **Planchas nuevas:** `tapa2` (bronce liso, base de la inscripción), `fragmentos`, `vitrina2` y `bulto`; 86–88 s cada
  una con FLUX.3 (la primera, 383 s con la carga del modelo).
- **Hecho:** capítulos I y II rehechos, revisados y renderizados (`renders/cap1.mp4` y `cap2.mp4`; los de la primera
  versión, en `renders/v1/`). El II se le envió al usuario como piloto, a 720p. El III tiene el montaje nuevo escrito
  (`montaje/cap3.py`) sin revisar ni renderizar; del IV al VIII, sin revisar. Las versiones anteriores de los montajes,
  en `montaje/capN_v1.py`.
- **Decisión:** el usuario para aquí Anticitera, sin gastar más tiempo en este vídeo, y cambia de rumbo (ver el
  punto 8).

### 8. Nuevo rumbo: BusinessForMen

- **El canal:** BusinessForMen, en español. Negocios para un público sobre todo masculino: gestión empresarial,
  administración de recursos, organización interna, branding, marketing digital, negociación y éxito empresarial,
  con la idea de hacerse un caballero profesional con mentalidad de negocios. Marca premium, con un rojo propio y
  negro. No es un documental (salvo que el tema lo pida) y los vídeos no llevan capítulos.
- **Regla del canal:** se debe entender; si no se entiende, no comunica. Edición «HIPER PRO» (término del usuario):
  de estudio y de agencia.
- **Decidido con el usuario:** el nombre es BusinessForMen (sin apóstrofo, que YouTube no admite en el identificador);
  seguimos en este repositorio; mismo método y mismas licencias hasta que avise de que se monetiza; la voz,
  Supertonic-3 M1.
- **Primer paso:** pruebas de marca, tres identidades con el mismo texto (unos 15 s), cada una con su logo animado y
  una miniatura, en `canales/businessformen/marca/`.

### 9. Pruebas de marca de BusinessForMen

- **Qué:** tres identidades con el mismo texto de 13,6 s sobre la MAAN (la mejor alternativa a un acuerdo negociado),
  cada una con su logo animado al final y una miniatura: **Sastre** (burdeos `#8E1B2C`, Bodoni Moda y Jost, lenta y
  fina), **Consejo** (carmesí `#B0122F`, Inter Tight y Plex Mono, rápida, cortes secos) y **Lacre** (rojo lacre
  `#B3261E`, Archivo Narrow e Instrument Serif, tipografía que golpea y un sello que se estampa). Detalle en
  `canales/businessformen/marca/README.md`; se repiten con su `preparar.sh`.
- **Medido:** voz, 1 min 47 s; música, 3 × 20 s en 207 s más 49 s de carga; imagen de FLUX, 113 s con la carga;
  render, de 30 a 32 s por vídeo de 18,8 s (todo CSS: 1,7 s por segundo de vídeo, frente a los 2,8 s del estilo A con
  WebGL); entrega a −15 LUFS, de 2,7 a 3,5 MB.
- **La música de «Consejo»:** la primera tenía el 90 % de la energía bajo 150 Hz («pulse» da sub-bajo). Se pidieron dos
  más brillantes: una con el 75 % por encima de 150 Hz (la elegida) y otra con el 82 % por encima de 6 kHz (casi solo
  agudos). Pedir instrumentos del registro medio y medir siempre.
- **Lo que enseñó HyperFrames:** las plantillas no pueden estar en la raíz del proyecto (cuentan como otra
  composición); las capas a pantalla completa empiezan ocultas por CSS; animar `letter-spacing` da saltos; un subrayado
  absoluto dentro de un elemento en línea no se ve (hace falta `inline-block`); y partir una palabra en letras hace que
  `check` cuente cada letra como una palabra al medir el tiempo de lectura.
- **Enviado al usuario:** la hoja comparativa y los tres vídeos. Falta que elija.

### 10. La marca elegida y el primer guion

- **Decidido con el usuario:** la marca es la ruta **Consejo**. Los vídeos tienen que ser impredecibles: nada de
  «texto a un lado e imagen al otro» repetido como una plantilla de PowerPoint (el defecto de Anticitera), golpes de
  marca como la pantalla roja de «Estás pidiendo», storytelling con casos reales de empresas y guiones de estudio.
- **Escrito:** las reglas de edición y un repertorio de quince recursos (`canales/businessformen/EDICION.md`), y el
  borrador del primer vídeo, «Por qué quiebran empresas que ganan dinero»
  (`canales/businessformen/videos/01-flujo-de-caja/GUION.md`): hilo en W. T. Grant, eco en Carillion, contraste en
  Amazon y cuatro reglas; 964 palabras, unos 7 min con el ritmo medido de la voz (2,57 palabras por segundo).
- **Datos comprobados con búsquedas** y anotados con su fuente en el guion; quedan tres por contrastar en una segunda
  fuente antes de producir.

### 11. Producción: el primer tramo del vídeo 1 (0:00–2:28)

- **El usuario aprobó el guion** y pidió producir los primeros 2–3 minutos de una vez. Hecho: del gancho a «crecer
  hasta morir», con el logo al final (2 min 28 s).
- **Kit del canal** (`canales/businessformen/kit/`): `montar.py` junta las escenas (una subcomposición por escena,
  anclada a las palabras de la voz), la música y los efectos; `marca.css` y `ayuda.js` son la marca Consejo y sus
  animaciones. 18 escenas en `videos/01-flujo-de-caja/escenas/`, cada una con un recurso distinto del anterior
  (`EDICION.md`): cifras que cuentan, la pantalla roja, un titular recreado, la pregunta a negro, cuadros que se llenan,
  la factura sobre el taller, la pantalla partida, CAJA con monedas dentro, el ciclo de caja con el punto que lo
  recorre, el sello PENDIENTE, el almacén que se queda sin color, la línea de los plazos y la gráfica que acaba en rojo.
- **Medido:** voz de 143,3 s en 1 min 12 s (2,6 palabras por segundo, más rápida de lo calculado: el tramo de 2:43 del
  guion dura 2:23); tres imágenes de FLUX, 110 s la primera con la carga y 84 s las otras; cuatro músicas de 20 s en
  un lote, unos 4 min; render, 205 s para 2 min 28 s (1,4 s por segundo de vídeo; todo CSS y SVG, sin WebGL); entrega
  a −15,2 LUFS, 29 MB. Enviado al usuario.
- **La música, otra vez:** la primera tanda («pulse», «driving electronic») salió con el 94 % y el 99 % de la energía
  bajo 150 Hz; en la segunda, las dos de cuerdas punteadas, con el 74 % y el 71 %. Se usan dos de cuerdas frotadas con
  marimba (0 % y 26 %).
- **Lo que rompió HyperFrames:** el CSS de cada subcomposición queda encerrado bajo su `data-composition-id`, así que
  la raíz de la plantilla no puede llevar estilos (hace falta un contenedor interior); las tildes de las mayúsculas
  asomaban por encima de la máscara (ahora las palabras suben desde el 140 %); `trocea()` perdía los `<br>`.

### 12. El vídeo 1, completo (6 min 19 s)

- **El usuario vio el primer tramo** («¡Está BRUTAL, qué estilazo!… te mantiene enganchado») y pidió terminarlo.
  Hecho: la historia de W. T. Grant, Carillion, Amazon, las cuatro reglas y el cierre, con 25 escenas nuevas (43 en
  total) y el logo al final. El gancho sigue igual: la voz nueva da los mismos tiempos en el primer tramo (0 palabras
  distintas en las 384 primeras), así que sus escenas no se tocaron.
- **Datos contrastados** antes de escribir: Carillion, 376 M£ en dividendos entre 2012 y 2016, 217 M£ más que la caja
  de sus operaciones (informe del Parlamento), unos 420 contratos públicos, 29 M£ en caja frente a casi 7.000 M£ en la
  liquidación; W. T. Grant, operaciones que no generaban caja hasta 1973 (Largay y Stickney) y 37,8 M$ de beneficio
  en el ejercicio cerrado en enero de 1973. La línea de beneficio de 1966–1973 se dibuja en «forma aproximada» y solo
  se rotulan los extremos, que tienen fuente.
- **Recursos y tiempos:** voz completa (98 frases, 374,7 s) en 4 min 15 s; cuatro músicas más (semilla 13) en 267 s,
  esta vez todas limpias de graves (1 %, 6 %, 2 % y 13 % bajo 150 Hz: piano y chelo, cuerdas sostenidas, piano
  eléctrico con violines, cuerdas y piano); tres imágenes de FLUX con su EDSR en 5 min 15 s (la tienda de los 60, la
  tienda vacía y la grúa sobre un hospital, las tres a la primera); 77 fotogramas de revisión en 37 s.
- **Recursos de la segunda parte:** el mapa de Estados Unidos (us-atlas, dominio público) con mil puntos que se
  encienden desde Lynn y, más tarde, se apagan hacia allí; el gráfico de beneficio plano y caja hundida, con lo
  atrapado entre las dos; el depósito con agujero (entra deuda, salen dividendos); el sello QUIEBRA que sacude el plano;
  el estudio de 1980 recreado y la línea de tiempo «10 años antes»; 1975 que gira como un cuentakilómetros hasta 2018;
  las barras de dividendos con lo que no salió del negocio en rojo; 120 cuadros, uno por día; 29 M£ frente a un cuadrado
  rojo 241 veces mayor, a escala; IMPRUDENCIA, ARROGANCIA, CODICIA; AL REVÉS boca abajo; la línea de tiempo del ciclo
  negativo de Amazon; la carta de 2004 con BENEFICIO tachado; las cuatro reglas con su índice (semanas, la tabla de
  13 semanas con la 9 en rojo, el ciclo que encoge, la flecha que choca con un muro); la tienda vacía con LE FALTABA
  CAJA; el tercer golpe rojo, LA CAJA ES REALIDAD; y la llamada a suscribirse con el botón de la marca.
- **Revisión de director** sobre los fotogramas con la frase de la voz debajo. Se corrigió: el año con punto de miles
  («1.963»), el nombre que pisaba el mapa (el mapa bajó), la tarjeta que asomaba antes de entrar, el «$» que tocaba la
  pila, la cifra que se salía del margen, un punto rojo en el extremo de cada trazo aún sin dibujar (remates redondos:
  ahora `traza()` lo oculta hasta que empieza; también lo tenía el primer tramo), el «2018» que se cortaba antes de
  aterrizar y que dejaba un hueco junto al 1 (cifras tabulares: ahora cada columna va a su sitio con el avance medido
  de cada cifra) y la carta que se transparentaba bajo el texto. `check`: sin errores ni avisos.
- **Para subir** (`canales/businessformen/videos/01-flujo-de-caja/PUBLICACION.md`): título, descripción con fuentes,
  los avisos (voz generada con IA, MusicGen CC BY-NC, imágenes generadas) y etiquetas; dos miniaturas (`miniatura.sh`:
  las cifras +38 M$ / −120 M$ o GANABA DINERO / Y QUEBRÓ); subtítulos SRT (`kit/subtitulos.py`) con los nombres bien
  escritos («Dóbliu Ti Grant» → «W. T. Grant», `recursos/pantalla.json`) y las cantidades en cifras.
- **Se rompió y se arregló:** editar `preparar.sh` mientras corría (la trampa ya anotada): se devolvió el archivo a su
  versión hasta que acabó. `const L` en una plantilla chocaba con la `L` de `ayuda.js` (el JS de la plantilla comparte
  ámbito con las ayudas). Un `tl.set(…, 0)` no se pinta en el primer fotograma de la escena: lo que nace oculto va con
  CSS o con `fromTo`.

## Siguiente paso

1. Que el usuario vea el vídeo 1 completo y diga qué cambiar o si se sube así (y qué miniatura).
2. El vídeo 2 del canal con el mismo kit: tema, guion con historias reales y datos contrastados, y producción de una
   vez, midiendo cuánto tarda de principio a fin.
3. Si se retoma Anticitera: revisar el III (ya montado) y del IV al VIII con las mismas reglas, y unir con `unir.sh`
   (en `renders/` solo están la apertura y los capítulos I y II nuevos; renderiza lo que falte).

## Primera idea de montaje (sustituida)

Antes del nuevo rumbo se pensó en montar con ffmpeg (movimiento lento sobre cada imagen, fundidos y
subtítulos). Se queda como referencia; el montaje se hará con HyperFrames. Propuesta original para un `montar.py`:

1. **Guion.** Claude lo escribe a partir del prompt, en un `guion.json` con el título y las escenas:
   `{"narracion": "...", "imagen": "prompt en inglés", "pausa": 0.8}`.
2. **Voz.** `narrar.py --guion` da `narracion.wav` y los tiempos; de ahí sale cuánto dura cada escena.
3. **Imágenes.** `generar.py --lote` a 768 × 432 (53 s cada una) o 1024 × 576. Un vídeo de 10 min con
   una imagen cada 15 s son 40 imágenes, unos 35 min. Para un borrador rápido, SDXS.
4. **Música y mezcla.** `musica.py --duracion` con la duración total y después `mezclar.py`.
5. **Montaje.** Cada imagen con un movimiento lento de cámara (zoom y paneo, el «efecto Ken Burns»),
   fundidos entre escenas, subtítulos sacados de los tiempos de la narración y un título al principio
   con `plantilla_titulo.html`.
6. **Velocidad.** Para vídeos largos, montar con filtros de ffmpeg en vez de pintar cada cuadro en el
   navegador: el render en canvas cuesta unos 3,6 s por segundo de vídeo a 720p30, demasiado para
   10 minutos.
7. **Opcional.** Escalar las imágenes a 1080p: FastSD trae `--upscale` (EDSR) y stable-diffusion.cpp, ESRGAN.

Antes de construirlo, preguntar al usuario: duración típica, formato (16:9 o 9:16), si lleva
subtítulos, estilo visual y voz.
