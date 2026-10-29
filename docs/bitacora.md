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

### Decisiones

- Imagen: FastSD CPU con OpenVINO. Calidad: FLUX.3 Image Klein. Bocetos: SDXS. Si el uso pasa a ser
  comercial: FLUX.2 klein 4B (Apache 2.0).
- Todo en local, sin APIs externas.
- Prompts de imagen en inglés, descriptivos.

### Pendiente

- Elegir la voz.
- Elegir el estilo.

## Siguiente paso

1. Que el usuario elija estilo (`docs/estilo.md`).
2. Con su permiso, instalar HyperFrames y sus skills (en `.claude/skills/` de este repositorio, para que
   estén en cada sesión), apuntándolo a nuestro Chromium y sin telemetría. Medir el render aquí.
3. Comparar Piper y Kokoro en español; probar BiRefNet (recortes) y Depth Anything V2 Small (2.5D).
4. Un tráiler de 20–30 s de «El faro» en el estilo elegido, de principio a fin, y revisarlo con el método
   de HyperFrames (P0, P1, P2).
5. Después, el flujo para vídeos largos: guion → storyboard con SDXS → planchas con FLUX.3 → narración →
   composición en HyperFrames → revisión → render.

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
