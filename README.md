# Vídeos automatizados

Crear **vídeos largos a partir de un prompt**, con **edición de nivel agencia**, en local: sin GPU,
sin servicios de pago y sin que el texto salga de la máquina. Todo funciona en la CPU de una sesión en
la nube de Claude Code. Las imágenes generadas son material de apoyo; el vídeo lo hace la edición.

## Estado (29 de octubre de 2026)

Las piezas ya funcionan y están medidas, y hay tres vídeos de prueba de 10 s, uno por estilo
([estilos/](estilos/README.md)). El estilo elegido es el A, editorial cinematográfico. Nicho del primer
canal: historia y misterios; primer vídeo, «El mecanismo de Anticitera» (8–10 min). Antes de empezarlo se
aceleró el proceso: el render del estilo A tarda un tercio y la entrega ya no recomprime (ver la
[bitácora](docs/bitacora.md#2-velocidad-dónde-se-va-el-tiempo-y-qué-se-ganó)). Ya está la apertura de 34 s
(`videos/anticitera/`, reproducible con `preparar-apertura.sh --render`); falta el vídeo largo por capítulos.

| Pieza | Herramienta | Estado |
| --- | --- | --- |
| Voz | Supertonic-3 M1 (principal) y Piper `es_AR-daniela-high` | ✅ `voz/narrar.py` |
| Imágenes | FastSD CPU + OpenVINO, modelos FLUX.3 Image Klein y SDXS | ✅ `imagen/generar.py` |
| Ampliación ×2 | EDSR de FastSD (ONNX) | ✅ `imagen/ampliar.py` |
| Tiempo de cada palabra | Alineación forzada en español (wav2vec2), o la de fonemas de Piper | ✅ `voz/alinear.py` |
| Música de fondo | MusicGen estéreo (uso no comercial); antes, síntesis con numpy | ✅ `audio/musica_ia.py` |
| Efectos de sonido | Grabaciones CC0 de BigSoundBank y la biblioteca de HyperFrames | ✅ `audio/efectos.py`, `audio/tecleo.py` |
| Mezcla de audio | Agache de la música bajo la voz, −14 LUFS | ✅ `audio/mezclar.py` |
| Animaciones en canvas | Canvas en Chromium → MP4 con desenfoque de movimiento | ✅ `video/renderizar_canvas.mjs` |
| Motor de edición y motion | HyperFrames 0.8.216 + GSAP; WebGL con llvmpipe de Mesa | ✅ instalado y medido, `video/hf.sh` |
| 2.5D y recortes | Depth Anything V2 Small, capas con OpenCV, BiRefNet lite | ✅ `imagen/profundidad.py`, `capas25d.py`, `recortar.py` |
| Volumen de entrega | loudnorm en dos pasadas a −15 LUFS | ✅ `video/entregar.sh` |
| Estilo de animación | A, editorial cinematográfico, elegido tras probar tres ([estilos/](estilos/README.md)) | ✅ elegido |
| Guion a partir del prompt | Lo escribe Claude en la sesión | ⏳ por diseñar |

## Empezar en una sesión nueva

Cada sesión arranca en una máquina limpia, así que lo primero es instalar las herramientas. El
instalador las deja fuera del repositorio, en `~/herramientas-videos`, porque pesan unos 14 GB:

```bash
./instalar.sh              # voz + imagen + edición (HyperFrames y modelos de apoyo)
./instalar.sh comprobar    # qué hay y qué falta
./instalar.sh precargar    # sesión reanudada: lee las herramientas en segundo plano (unos 6 min)
```

En una sesión nueva tarda unos 5–10 minutos (estimado por las velocidades de descarga medidas:
la mayor parte son los modelos de Hugging Face). Si ya está instalado, solo comprueba (7 s). Para que
se haga solo al abrir cada sesión, ver [docs/entorno.md](docs/entorno.md).

Necesita que la red del entorno permita `huggingface.co` y su CDN (`*.hf.co`).

## Cómo se usa cada pieza

```bash
# Imagen (la primera llamada arranca un servidor que deja el modelo cargado)
python3 imagen/generar.py "a lighthouse on a rocky coast at sunset, semi-realistic digital illustration" \
  -o faro.png --ancho 768 --alto 432
python3 imagen/generar.py "..." -o boceto.png --modelo sdxs     # medio segundo
python3 imagen/generar.py --lote escenas.json                   # varias de una vez

# Voz (con el Python del entorno de Piper): Supertonic-3 M1 por defecto
~/herramientas-videos/piper/bin/python voz/narrar.py --guion guion.json -o narracion.wav
~/herramientas-videos/piper/bin/python voz/narrar.py --guion guion.json -o narracion.wav --voz es_AR-daniela-high

# Música y mezcla
python3 audio/musica.py --duracion 60 -o musica.wav
python3 audio/mezclar.py --voz narracion.wav --musica musica.wav -o mezcla.wav

# Título animado (o cualquier escena HTML con window.cuadro(t))
node video/renderizar_canvas.mjs video/plantilla_titulo.html titulo.mp4 --duracion 5 \
  --param titulo="El faro" --param subtitulo="Capítulo 1" --audio mezcla.wav

# Edición con HyperFrames (desde la carpeta de un proyecto, ver estilos/)
../../video/hf.sh check --json
../../video/hf.sh render -o video.mp4 --quality high --crf 20   # ya con la calidad de entrega
video/entregar.sh video.mp4 entrega.mp4 -15 copiar   # −15 LUFS; el vídeo se copia sin recomprimir

# Apoyo a la edición (con el Python del entorno de FastSD)
PY=~/herramientas-videos/fastsdcpu/env/bin/python
$PY imagen/profundidad.py faro.png -o faro_prof.png         # mapa de profundidad, 3 s
$PY imagen/capas25d.py faro.png faro_prof.png -o faro        # sujeto y fondo para el 2.5D
$PY imagen/recortar.py brujula.png -o brujula_recorte.png --ajustar
$PY audio/musica_ia.py "slow cinematic ambient, soft piano, 70 bpm" -o musica.wav --duracion 12
python3 audio/efectos.py buscar "match" "typewriter"          # efectos CC0
python3 audio/efectos.py bajar 0004 -d sfx/
```

Los prompts de imagen funcionan mejor en inglés y descriptivos: sujeto, lugar, luz y estilo.

## Rendimiento medido aquí

La máquina cambia entre sesiones: siempre 4 núcleos, 15 GB de RAM y sin GPU, pero en la sesión 1 fue un
Xeon a 2,1 GHz con AMX y en la 2 un Cascade Lake a 2,8 GHz sin AMX.

| Tarea | Sesión 1 (con AMX) | Sesión 2 (sin AMX) | RAM |
| --- | --- | --- | --- |
| Imagen FLUX.3 Image Klein, 512 × 512 | 37–39 s (73 s la primera) | 85 s (18,5 s por paso; 104 s la primera) | 8,2 GB |
| Imagen FLUX.3 Image Klein, 768 × 432 (16:9) | 53 s (95 s la primera) | — | 8,2 GB |
| Imagen FLUX.3 Image Klein, 1280 × 720 | 138–211 s | 328 s (246 s con 3 pasos) | 8,2–12 GB |
| Imagen FLUX.2 klein 4B, 512 × 512 | 39–43 s | — | 9,3 GB |
| Imagen SDXS, 512 × 512 | 0,5 s (8–17 s la primera) | — | 5,0 GB |
| Voz Piper: 10 s de narración | 14,5 s, incluida la carga | — | — |
| Voz Supertonic-3 con tiempos de palabras | 7 s en 14 s | 58 s en 61 s (síntesis 41 s) | 2 GB |
| Música sintetizada: 14 s | 1,9 s | — | — |
| Música MusicGen estéreo: 12 s | 50–55 s | 69–96 s; en lote de 4, 31 s por cada 10 s | 3 GB |
| Título animado: 4 s a 720p30 | 14 s | — | — |
| Profundidad (Depth Anything V2 Small) | 3 s por imagen | 5 s | — |
| Recorte (BiRefNet lite), 768 × 768 | 27 s | — | — |
| Render HyperFrames: 10 s a 1080p30 | 2 min–3 min 14 s, según el estilo | estilo A: 66 s (195 s al empezar); B: 114 s | — |
| Ampliar ×2 con EDSR | — | 7 s desde 960 × 544; 12,5 s desde 1280 × 720 | — |
| Entrega de 10 s de vídeo | — | 2,2 s copiando; 47 s recomprimiendo con preset slow | — |

«La primera» incluye cargar el modelo en memoria. La comparativa completa, con imágenes, está en
[docs/investigacion-imagenes.md](docs/investigacion-imagenes.md).

![Comparativa de modelos](docs/resultados/comparativa.jpg)

## Estructura

```
instalar.sh                 instala y comprueba las herramientas (fuera del repo)
imagen/generar.py           prompt → PNG; arranca y reutiliza imagen/servidor.py
imagen/servidor.py          servidor local que mantiene FastSD cargado y guarda PNG sin pérdida
imagen/profundidad.py       mapa de profundidad (Depth Anything V2 Small)
imagen/capas25d.py          sujeto y fondo rellenado para el 2.5D por capas
imagen/recortar.py          quita el fondo de un objeto (BiRefNet lite)
imagen/ampliar.py           amplía ×2 con EDSR (el de FastSD) y encaja en 1920 × 1080
imagen/pruebas/             banco de pruebas: comparar modelos y montar hojas comparativas
voz/narrar.py               texto o guion → WAV + JSON con los tiempos de cada frase y palabra
voz/alinear.py              tiempo de cada palabra de cualquier voz (alineación forzada)
voz/supertonic_frases.py    síntesis con Supertonic-3 (la usa narrar.py)
audio/musica_ia.py          música de fondo con MusicGen
audio/efectos.py            busca y baja efectos de sonido CC0 (BigSoundBank)
audio/tecleo.py             pista de máquina de escribir con teclas reales
audio/musica.py             música de fondo sintetizada (la primera versión)
audio/mezclar.py            voz + música con agache y volumen estándar
video/hf.sh                 HyperFrames con la configuración del entorno (WebGL con llvmpipe, 2 Chromium)
video/chrome-llvmpipe.sh    Chrome para HyperFrames: WebGL en llvmpipe y la página en la CPU
video/entregar.sh           versión de entrega: −15 LUFS y archivo más ligero
video/renderizar_canvas.mjs escena HTML animada → MP4
video/plantilla_titulo.html plantilla de título animado
estilos/                    las tres pruebas de estilo en HyperFrames y su preparar.sh
videos/anticitera/          el primer vídeo: guion, prompts, preparar-apertura.sh y la apertura en HyperFrames
docs/                       bitácora, investigaciones (imagen y edición), estilo, entorno y resultados
CLAUDE.md                   contexto e instrucciones para Claude en cada sesión
```

## Siguiente paso

Definir el nicho de los vídeos y hacer un tráiler de 20–30 s de principio a fin en el estilo A, con la
voz M1. El plan
está en [docs/bitacora.md](docs/bitacora.md#siguiente-paso); la investigación, en
[docs/investigacion-edicion.md](docs/investigacion-edicion.md).

![Las tres pruebas de estilo](docs/resultados/comparativa-estilos.jpg)

## Licencias

El código del repositorio es del proyecto. Las herramientas y modelos se descargan aparte, cada
uno con su licencia:

- FastSD CPU y stable-diffusion.cpp: MIT. Piper: GPL-3.0 (se usa como programa externo).
- FLUX.3 Image Klein: FLUX Kommunity License, gratis para personas y empresas de menos de 5 M$ al año.
- FLUX.2 klein 4B: Apache 2.0. SDXS: OpenRAIL++.
- HyperFrames: Apache 2.0. GSAP: licencia gratuita de GreenSock. Fuentes de las pruebas: OFL
  (Special Elite: Apache 2.0).
- Depth Anything V2 Small: Apache 2.0. BiRefNet lite: MIT. MusicGen: CC BY-NC 4.0, **solo uso no
  comercial**; para uso comercial habría que cambiar de modelo de música.
- Efectos: BigSoundBank, CC0; biblioteca de HyperFrames, licencia de Pixabay.
- Supertonic-3: Open RAIL-M. Permite uso comercial, pero obliga a avisar de que el contenido está
  generado por máquina y prohíbe suplantar a personas. Alineador wav2vec2 en español: Apache 2.0.
- Voces de Piper: `es_AR-daniela-high` se entrenó con datos CC BY-SA 4.0 (OpenSLR 61) y
  `es_MX-claude-high` con datos Apache 2.0. Conviene revisarlas antes de un uso comercial.
