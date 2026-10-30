# Contexto para Claude

Proyecto: **vídeos largos a partir de un prompt**, generados en local en la CPU de la sesión (voz,
imágenes, música y montaje), sin GPU ni servicios externos. El estado de cada pieza está en el
README; lo hecho, lo decidido y lo pendiente, en `docs/bitacora.md`.

## Rumbo actual

**Edición de nivel agencia, no «imagen + voz».** Lo que pasa en pantalla (cuándo, dónde, cómo, efectos,
gráficos, ritmo, sonido) tiene que ser de agencia de branding. Las imágenes generadas son material de
apoyo. Motor: HyperFrames + GSAP (ver `docs/investigacion-edicion.md`), ya instalado y medido. Estilo:
**A, editorial cinematográfico**, elegido por el usuario tras ver las tres pruebas (`estilos/`,
`docs/estilo.md`); el punto de partida es `estilos/estilo-a`.
Para trabajar con HyperFrames, leer antes sus guías en
`~/herramientas-videos/hyperframes/node_modules/hyperframes/dist/skills/` (`hyperframes/SKILL.md` y
`references/`: motion, sound, look, review, format, runtimes) y `estilos/README.md`.

## Al empezar una sesión

1. Lee `README.md` y `docs/bitacora.md`.
2. Ejecuta `./instalar.sh comprobar`. Si falta algo, lanza `./instalar.sh` en segundo plano
   (5–10 min en una máquina nueva) y avanza mientras con lo que no dependa de él. Si ya está todo (la
   sesión se ha reanudado), lanza `./instalar.sh precargar` en segundo plano (unos 6 min): la primera
   lectura de cada archivo va a 10–40 MB/s y, sin precargar, FLUX tardó 11 min en cargar.
3. Retoma por «Siguiente paso» de la bitácora, salvo que el usuario pida otra cosa. Si abre un chat
   nuevo para seguir, confirma en pocas líneas dónde lo dejamos antes de empezar.
4. Al terminar algo importante, añádelo a la bitácora: fecha, qué se hizo, qué se midió, qué se decidió.

## Preferencias del usuario

- Escribe en español. Prefiere resultados probados a listas de opciones: prueba, mide y enseña.
- Lo que se crea se queda en la sesión salvo que diga otra cosa: no publicar artefactos ni subir
  nada a otros sitios. Commits y push, solo a este repositorio y cuando lo pida.
- **Este repositorio es público.** Nada de otros proyectos suyos ni datos personales aquí.
- Uso no comercial, de momento. Si cambia, preferir modelos Apache 2.0 (FLUX.2 klein 4B).
- Imágenes: busca «representaciones bastante asemejadas a lo real y que se entienda lo que son»;
  no hace falta fotorrealismo.
- Quiere edición «de élite»: aplicar el oficio de `docs/investigacion-edicion.md` (curvas según el papel,
  títulos quietos al aterrizar, transiciones con causa, tiempos de lectura) y revisar como un director exigente.
- Voz: **Supertonic-3 M1** (masculina, español neutro), la predeterminada de `voz/narrar.py`. Segunda
  voz: Piper `es_AR-daniela-high` (femenina, acento argentino). Más adelante quiere varios canales de
  nichos distintos, cada uno con su voz: el sistema debe dejar elegir la voz por canal.
- **Todo vídeo con voz de Supertonic avisa de que está generada por máquina** (descripción o rótulo):
  lo exige su licencia Open RAIL-M. MusicGen, además, solo vale para uso no comercial.
- Le gustó descubrir herramientas investigando repositorios públicos de GitHub y Hugging Face.
  Ante un problema nuevo, buscar primero qué existe y qué está al día.

## El entorno (comprobado el 29-oct-2026)

- 4 núcleos, 15 GB de RAM, unos 30 GB de disco, sin GPU. **La CPU cambia entre sesiones**: en la 1, un
  Xeon a 2,1 GHz con AMX; en la 2, un Cascade Lake a 2,8 GHz sin AMX, con FLUX 2,4 veces más lento
  (328 s por imagen a 1280 × 720). Mira `lscpu` al empezar y no compares tiempos entre máquinas distintas.
- **OpenVINO aprovecha esta CPU**: el mismo FLUX.2 klein fue 8 veces más rápido con FastSD CPU
  (OpenVINO) que con stable-diffusion.cpp. Para imágenes, FastSD CPU.
- Red: Hugging Face (y su CDN `*.hf.co`), PyPI, download.pytorch.org, storage.openvinotoolkit.org,
  `raw.githubusercontent.com`, git de GitHub, npm/jsDelivr y los paquetes de Ubuntu (`apt-get`). La web de github.com devuelve 403:
  los README se leen con `curl` a `raw.githubusercontent.com`. WebFetch no llega a sitios fuera de
  la lista permitida; WebSearch sí funciona.
- Instalado de serie: python3.11 (lo necesita FastSD), python3.13, uv, gcc y cmake, ffmpeg, Node 22,
  Playwright con Chromium y fuentes Inter.
- El control de seguridad bloquea descargar y ejecutar código de terceros que el usuario no haya
  pedido explícitamente. Autorizó FastSD CPU, stable-diffusion.cpp y Piper, y para las pruebas de estilo
  «instalar lo que necesites»: HyperFrames y los modelos de apoyo, que es lo que instala `instalar.sh`.
  Para cualquier herramienta nueva, pedirle permiso antes.
- Sonido: BigSoundBank (CC0) llega; Freesound y Pixabay dan 403, la API de Wikimedia 429 y la búsqueda
  de Openverse no responde. Node no usa el proxy por su cuenta: `NODE_USE_ENV_PROXY=1` (lo pone `video/hf.sh`).
- Cada sesión es una máquina nueva: lo que no esté en este repositorio se pierde.

## Trampas conocidas

- La API propia de FastSD devuelve JPEG con pérdida. Por eso existe `imagen/servidor.py`, que guarda PNG.
- El servidor de imágenes escucha en `127.0.0.1:8124` y ocupa 5–12 GB de RAM con el modelo cargado (12 GB con FLUX.3 en la CPU sin AMX).
  `python3 imagen/generar.py --parar` lo apaga.
- Cambiar de modelo en el servidor obliga a cargarlo otra vez (8–95 s).
- SDXS solo da buen resultado a 512 × 512. FLUX acepta cualquier múltiplo de 16.
- FLUX toma los prompts al pie de la letra: «small gold rings» llenó un bolso de anillas.
- Mover un entorno virtual rompe sus ejecutables (las rutas van escritas dentro); usar `env/bin/python -m ...`.
- La CPU tiene 4 núcleos: no medir tiempos mientras corre otra cosa pesada.
- Para esperar a procesos largos, usar tareas en segundo plano y Monitor, no `sleep`.
- No cargar otro modelo (BiRefNet, MusicGen) con el servidor de imágenes encendido: se acaba la RAM y el
  sistema lo mata. Apagarlo antes.
- FLUX escribe letras inventadas si el prompt habla de «espacio para un título»: describir solo la zona
  vacía y añadir «no text».
- HyperFrames: el desenfoque de movimiento se sale de las máscaras (`overflow: hidden`); `check` da falsos
  avisos de contraste con fondos escalados o recortados; `media-treatment --apply` añade `data-hf-id` a todo
  el HTML. Detalles en `estilos/README.md`.
- Piper no da el mismo audio dos veces (tiene ruido aleatorio): los tiempos varían hasta 50 ms entre
  ejecuciones. Generar la narración una vez y cronometrar la composición sobre ese archivo.
- Un render en segundo plano se lanza con el binario de HyperFrames directamente; con `nohup` a través de
  `video/hf.sh` se canceló (`render_cancelled_parent_exited`).
- El WebGL del render va por software: cada muestra de textura cuesta. El shader de las planchas tomaba
  16 muestras por píxel también sin desenfoque y el render tardaba el doble.
- `video/hf.sh` usa llvmpipe de Mesa para el WebGL (si está el EGL de Mesa, que pone `./instalar.sh
  edicion`) y deja el texto y la composición en la CPU con `video/chrome-llvmpipe.sh`: con todo en llvmpipe
  (`--browser-gpu` a secas) el texto va un 45 % más lento. El grano sale con otro dibujo que con
  SwiftShader; `HF_SWIFTSHADER=1` vuelve a SwiftShader.
- La calibración automática de HyperFrames elige a veces 1 Chromium (mide un primer cuadro lento):
  `hf.sh` pone 2 por cada 4 núcleos; con 3 o 4 no mejora.
- No recomprimir lo renderizado: render con `--quality high --crf 20` (preset fast, la misma calidad que
  medium y un 10 % más rápido) y `video/entregar.sh … copiar`. Recomprimir 9 min con preset slow eran
  unos 40 min, y con peor calidad.
- Una narración larga se alinea frase a frase (`voz/alinear.py --frases`, lo hace `narrar.py`): entera,
  la atención de wav2vec2 no cabe en la RAM.
- MusicGen rinde más en lote: varias piezas en una sola llamada (4 a la vez, 1,7 veces más rápido).
- Cargar cada modelo una vez por trabajo: voz y música antes que FLUX, o después de todo el lote de planchas.

## Cómo decidir

- Antes de recomendar una herramienta o un modelo, probarlo aquí y medir tiempo y RAM. En la primera
  sesión las estimaciones fallaron en los dos sentidos.
- El banco de pruebas está en `imagen/pruebas/`: `comparar.py`, `sdcpp.py` y `hoja.py`.
- En los prompts de imagen, pedir también la composición (dónde va el sujeto y dónde queda espacio para
  el texto), con el mismo sufijo de dirección de arte en todo el vídeo.
