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

- Definir el nicho de los vídeos y la forma de trabajar (el usuario lo hará en el chat siguiente).
- Idea del usuario para más adelante: con el sistema montado, varios canales de nichos distintos, cada uno
  con su voz (y quizá su modo de estilo). Ahora se elige la voz del nicho principal; el sistema debe dejar
  elegir la voz por canal.

## Siguiente paso

1. El usuario define el nicho de los vídeos y cómo se hará. Lo dirá al abrir un chat nuevo, que sirve
   también para comprobar que este repositorio basta para continuar.
2. Un tráiler de 20–30 s en el estilo A, con la voz M1 y en el nicho elegido, partiendo de
   `estilos/estilo-a` (sus tiempos están hechos para la narración de daniela: rehacerlos con los de M1),
   de principio a fin, revisado con el método de HyperFrames (P0, P1, P2) y su `snapshot --review`.
3. Después, el flujo para vídeos largos: guion → storyboard con SDXS → planchas con FLUX.3 → narración con
   tiempos por palabra → composición en HyperFrames por capítulos → revisión → render. Medir cuánto tarda
   un minuto completo (en estas pruebas, 12–19 s de render por segundo de vídeo).
4. Pendiente de probar: `remove-background` de HyperFrames frente a BiRefNet, y MusicGen medium.

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
