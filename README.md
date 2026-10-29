# Vídeos automatizados

Crear **vídeos largos a partir de un prompt**, en local: sin GPU, sin servicios de pago y sin que el
texto salga de la máquina. Todo funciona en la CPU de una sesión en la nube de Claude Code.

## Estado (29 de octubre de 2026)

Las piezas ya funcionan y están medidas. Falta unirlas en el montaje final.

| Pieza | Herramienta | Estado |
| --- | --- | --- |
| Voz | Piper, voces en español | ✅ `voz/narrar.py` |
| Imágenes | FastSD CPU + OpenVINO, modelos FLUX.3 Image Klein y SDXS | ✅ `imagen/generar.py` |
| Música de fondo | Síntesis con numpy, sin derechos | ✅ `audio/musica.py` |
| Mezcla de audio | Agache de la música bajo la voz, −14 LUFS | ✅ `audio/mezclar.py` |
| Animaciones y títulos | Canvas en Chromium → MP4 con desenfoque de movimiento | ✅ `video/renderizar_canvas.mjs` |
| Guion a partir del prompt | Lo escribe Claude en la sesión | ⏳ por diseñar |
| Montaje (escenas → vídeo) | ffmpeg | ⏳ siguiente paso |

## Empezar en una sesión nueva

Cada sesión arranca en una máquina limpia, así que lo primero es instalar las herramientas. El
instalador las deja fuera del repositorio, en `~/herramientas-videos`, porque pesan unos 12 GB:

```bash
./instalar.sh              # voz + imagen
./instalar.sh comprobar    # qué hay y qué falta
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

# Voz (con el Python del entorno de Piper)
~/herramientas-videos/piper/bin/python voz/narrar.py --guion guion.json -o narracion.wav

# Música y mezcla
python3 audio/musica.py --duracion 60 -o musica.wav
python3 audio/mezclar.py --voz narracion.wav --musica musica.wav -o mezcla.wav

# Título animado (o cualquier escena HTML con window.cuadro(t))
node video/renderizar_canvas.mjs video/plantilla_titulo.html titulo.mp4 --duracion 5 \
  --param titulo="El faro" --param subtitulo="Capítulo 1" --audio mezcla.wav
```

Los prompts de imagen funcionan mejor en inglés y descriptivos: sujeto, lugar, luz y estilo.

## Rendimiento medido aquí

Máquina: Intel Xeon de 4 núcleos a 2,1 GHz con AMX, 15 GB de RAM, sin GPU.

| Tarea | Tiempo | RAM |
| --- | --- | --- |
| Imagen FLUX.3 Image Klein, 512 × 512 | 37–39 s (73 s la primera) | 8,2 GB |
| Imagen FLUX.3 Image Klein, 768 × 432 (16:9) | 53 s (95 s la primera) | 8,2 GB |
| Imagen FLUX.2 klein 4B, 512 × 512 | 39–43 s | 9,3 GB |
| Imagen SDXS, 512 × 512 | 0,5 s (8–17 s la primera) | 5,0 GB |
| Voz: 10 s de narración | 14,5 s, incluida la carga | — |
| Música: 14 s | 1,9 s | — |
| Título animado: 4 s a 720p30 | 14 s | — |

«La primera» incluye cargar el modelo en memoria. La comparativa completa, con imágenes, está en
[docs/investigacion-imagenes.md](docs/investigacion-imagenes.md).

![Comparativa de modelos](docs/resultados/comparativa.jpg)

## Estructura

```
instalar.sh                 instala y comprueba las herramientas (fuera del repo)
imagen/generar.py           prompt → PNG; arranca y reutiliza imagen/servidor.py
imagen/servidor.py          servidor local que mantiene FastSD cargado y guarda PNG sin pérdida
imagen/pruebas/             banco de pruebas: comparar modelos y montar hojas comparativas
voz/narrar.py               texto o guion → WAV + JSON con los tiempos de cada frase
audio/musica.py             música de fondo sintetizada, de cualquier duración
audio/mezclar.py            voz + música con agache y volumen estándar
video/renderizar_canvas.mjs escena HTML animada → MP4
video/plantilla_titulo.html plantilla de título animado
docs/                       bitácora, investigación, entorno y resultados
CLAUDE.md                   contexto e instrucciones para Claude en cada sesión
```

## Siguiente paso

El montaje: un `montar.py` que, a partir de un guion en JSON, encadene narración, imágenes,
música, títulos y subtítulos en un solo MP4. El diseño propuesto está en
[docs/bitacora.md](docs/bitacora.md#siguiente-paso-el-montaje).

## Licencias

El código del repositorio es del proyecto. Las herramientas y modelos se descargan aparte, cada
uno con su licencia:

- FastSD CPU y stable-diffusion.cpp: MIT. Piper: GPL-3.0 (se usa como programa externo).
- FLUX.3 Image Klein: FLUX Kommunity License, gratis para personas y empresas de menos de 5 M$ al año.
- FLUX.2 klein 4B: Apache 2.0. SDXS: OpenRAIL++.
- Voces de Piper: `es_AR-daniela-high` se entrenó con datos CC BY-SA 4.0 (OpenSLR 61) y
  `es_MX-claude-high` con datos Apache 2.0. Conviene revisarlas antes de un uso comercial.
