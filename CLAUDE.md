# Contexto para Claude

Proyecto: **vídeos largos a partir de un prompt**, generados en local en la CPU de la sesión (voz,
imágenes, música y montaje), sin GPU ni servicios externos. El estado de cada pieza está en el
README; lo hecho, lo decidido y lo pendiente, en `docs/bitacora.md`.

## Rumbo actual

**El primer canal es BusinessForMen**, en español: negocios (gestión empresarial, administración de recursos,
organización interna, branding, marketing digital, negociación, éxito empresarial) para un público sobre todo
masculino que quiere hacerse un caballero profesional con mentalidad de negocios. La marca tiene que sentirse
**premium**: un rojo propio (no un rojo típico) y negro. No es un documental, salvo que el tema lo pida, y los vídeos
no llevan capítulos: un solo hilo, la esencia. Tono: rigor, elegancia y ética, nunca el discurso «alfa».
**Regla del canal: SE DEBE ENTENDER. Si no se entiende, no comunica.** Edición **«HIPER PRO»** (término del usuario:
de estudio, de agencia, de élite): si hablamos de éxito, predicamos con el ejemplo. Anticitera (`videos/anticitera/`)
quedó en pausa; su motor y su kit se reutilizan. Además de los vídeos largos, el canal tiene **cortos verticales** para
Reels, TikTok y Facebook (`canales/businessformen/cortos/`, con sus reglas en su README): el mismo archivo para las tres
apps, sin logos de ninguna ni «sígueme», gancho en el fotograma 0 y final en bucle. Mismo método de trabajo y mismas licencias hasta que el usuario
avise de que se monetiza (entonces, música e imágenes con licencia comercial).

**Edición de nivel agencia, no «imagen + voz».** Lo que pasa en pantalla (cuándo, dónde, cómo, efectos,
gráficos, ritmo, sonido) tiene que ser de agencia de branding: cada plano enseña lo que dice la voz, en la palabra que
lo dice. Las imágenes generadas son material de apoyo. Motor: HyperFrames + GSAP (ver `docs/investigacion-edicion.md`),
ya instalado y medido. El estilo A, editorial cinematográfico (`estilos/estilo-a`, `docs/estilo.md`), fue el de
Anticitera; el de BusinessForMen sale de las pruebas de marca de `canales/businessformen/marca/`.
Para trabajar con HyperFrames, leer antes sus guías en
`~/herramientas-videos/hyperframes/node_modules/hyperframes/dist/skills/` (`hyperframes/SKILL.md` y
`references/`: motion, sound, look, review, format, runtimes) y `estilos/README.md`.

**Rastreador de nichos** (`rastreador/`, con su README): antes de elegir un tema, medirlo. El mapa de TikTok en español
sale de un dataset público de 5.600 M de vídeos (CC BY-NC, solo uso no comercial); los Shorts atípicos, de la API de
YouTube (la clave la pone el proxy del entorno); y el porqué de un vídeo, de `desmontar.py` sobre un archivo que sube el
usuario. Los informes, en `rastreador/informes/`.

**Dos canales de prueba** (desde el 31-oct-2026, una semana): **geografía** con mapas animados (`canales/geografia/`,
voz F4) e **historias reales de supervivencia** (`canales/supervivencia/`, voz M2), cada uno con su canal de Shorts y su
página de Reels de Facebook. Los eligió el usuario con el informe del rastreador. Cortos de 60–90 s, guiones sencillos
pero intrigantes y la retención de `canales/RETENCION.md`; se montan con el kit de BusinessForMen y la marca de cada
canal (`montar.py --canal`, `canales/preparar-corto.sh`). Las historias reales, con los datos contrastados y sin
inventar lo que las fuentes no dicen. **La audiencia de supervivencia** (1-nov): más del 50 % de Colombia y de 50–60 años.
Los dos cortos colombianos (9 y 10) **no funcionaron** (2-nov): se vuelve a la fórmula de los cortos 1–8, historias conocidas
en todo el mundo medidas en inglés y en español, una con hueco y otra con demanda probada (ver `canales/supervivencia/CANAL.md`).

**Tercer canal, de incidentes sin resolver** (3-nov, `canales/incidentes/`, voz M5): lo pidió el usuario para «atraer a más
población»: casos reales y extraños que nadie ha explicado (un avistamiento, una desaparición), como expedientes numerados.
Mismas reglas de retención y de sonido; las hipótesis se cuentan como preguntas, sin afirmar lo que no se sabe (ver su
`CANAL.md`). El primero, Frederick Valentich («No es un avión»).

## Al empezar una sesión

1. Lee `README.md` y `docs/bitacora.md`.
2. Ejecuta `./instalar.sh comprobar`. Si falta algo, lanza `./instalar.sh` en segundo plano
   (5–10 min en una máquina nueva) y avanza mientras con lo que no dependa de él. Si ya está todo (la
   sesión se ha reanudado), lanza `./instalar.sh precargar` en segundo plano (6–16 min): la primera
   lectura de cada archivo va a 10–40 MB/s y, sin precargar, FLUX tardó 11 min en cargar. Mientras precarga, el disco
   va tan lento que la voz tarda 10 veces más y hasta la API de YouTube se agota: medir y generar al terminar.
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
- Voz: **Supertonic-3 M1** (masculina, español neutro), la predeterminada de `voz/narrar.py` y la de los vídeos largos de
  BusinessForMen. **Los cortos de BFM, desde el 10, van con la M2** de supervivencia, sin música y solo con efectos (la
  «nueva receta»: el Ford m2 «se movió más» y el usuario la pidió para los cortos nuevos; ver la regla 12 del README de
  los cortos). Segunda
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
  la lista permitida; WebSearch sí funciona. En la sesión 5 llegaban también YouTube (web, RSS y la API, con clave),
  TikTok, Instagram, la Graph API de Meta y el RSS de Google Trends; Reddit daba 403 y la API de GitHub está cerrada
  para la sesión (la fecha del último commit de un repositorio, con `git clone --filter=blob:none --no-checkout`).
- Instalado de serie: python3.11 (lo necesita FastSD), python3.13, uv, gcc y cmake, ffmpeg, Node 22,
  Playwright con Chromium y fuentes Inter.
- El control de seguridad bloquea descargar y ejecutar código de terceros que el usuario no haya
  pedido explícitamente. Autorizó FastSD CPU, stable-diffusion.cpp y Piper, y para las pruebas de estilo
  «instalar lo que necesites»: HyperFrames y los modelos de apoyo, que es lo que instala `instalar.sh`.
  Para cualquier herramienta nueva, pedirle permiso antes.
- Sonido: BigSoundBank (CC0) llega; Freesound y Pixabay dan 403, la API de Wikimedia 429 y la búsqueda
  de Openverse no responde. Node no usa el proxy por su cuenta: `NODE_USE_ENV_PROXY=1` (lo pone `video/hf.sh`).
- Cada sesión es una máquina nueva: lo que no esté en este repositorio se pierde.
- **La red depende del entorno en que arranca la sesión.** La 12 (6-nov) empezó en «Default», sin dominios: Hugging Face
  daba 403 y no se instalaba nada. Se creó el entorno personal «VIDEOS-AUTOMATIZADOS-» con la lista exacta de dominios
  (`docs/entorno.md`). Si `./instalar.sh` se para con «No llego a huggingface.co», mirar el entorno antes que nada. La clave
  de YouTube no se puede guardar desde el formulario de credenciales (solo `Authorization: Bearer`, que Google rechaza): la
  pone el usuario en los secretos de red del entorno, cabecera `X-Goog-Api-Key`.

## Trampas conocidas

- La API propia de FastSD devuelve JPEG con pérdida. Por eso existe `imagen/servidor.py`, que guarda PNG.
- Nada de disfrazar peticiones con un User-Agent de navegador: el control de seguridad lo para («Bot Check
  Circumvention»). Para datos de plataformas, fuentes públicas u oficiales (RSS, APIs con clave, datasets).
- Bajar vídeos de YouTube o TikTok desde aquí no funciona: YouTube pide «Sign in to confirm you're not a bot» y da 403
  al vídeo; TikTok rechaza la petición. No se esquiva (cookies, proxys): el usuario guarda el vídeo y lo sube.
- La API de YouTube con `order=viewCount` no hace caso de `relevanceLanguage` (devuelve lo más visto del mundo): buscar
  por relevancia y filtrar por el idioma declarado. La clave va como secreto del entorno en la cabecera
  `X-Goog-Api-Key`; como `Authorization: Bearer` Google responde 401. Además de las 10.000 unidades, corta las búsquedas
  por número al día (429 «Search Queries per day»; el 3-nov, tras unas 25 en una tarde más las del rastreador): las
  búsquedas, lo primero. Leer vídeos, canales y comentarios (1 unidad) sigue funcionando; se renueva a medianoche de
  California (las 8:00 UTC).
- DuckDB baja sus extensiones por http sin proxy y falla: `instalar.sh rastreador` baja httpfs por https. DuckDB 2.0
  pide `lambda x: …` en vez de `x -> …`, y `con.execute(…).fetchone()` (las relaciones ya no tienen `fetchone`).
- El dataset de TikTok mide cada mes en otro momento (agosto, más tarde y con menos vídeos recientes): no comparar
  cifras absolutas entre meses, solo cuotas y aciertos relativos.
- El servidor de imágenes escucha en `127.0.0.1:8124` y ocupa 5–12 GB de RAM con el modelo cargado (12 GB con FLUX.3 en la CPU sin AMX).
  `python3 imagen/generar.py --parar` lo apaga.
- Cambiar de modelo en el servidor obliga a cargarlo otra vez (8–95 s).
- SDXS solo da buen resultado a 512 × 512. FLUX acepta cualquier múltiplo de 16.
- FLUX toma los prompts al pie de la letra: «small gold rings» llenó un bolso de anillas. Y la época hay que describirla
  prenda a prenda: «early 1700s uniforms» dio soldados de la Primera Guerra Mundial; «black tricorn hats, long blue coats»,
  los de 1705. Tampoco cuenta bien ni conoce los modelos: «four bright lights» salieron seis en dos columnas, y «Cessna 182»,
  un biplano o un ala baja (hay que decir «exactly four… in one horizontal row» y «high-wing, the wing on top of the cabin»).
  «Exactly four… in single file» volvió a dar cinco o seis; en una fila horizontal, cuatro. Y no hace caso del «without»:
  «turboprop airliner without wings» dibujó las alas y las hélices bajo el rótulo «Sin alas». Se describe lo que se ve («a
  bare smooth tube with only short jagged stubs where the wings were torn off»).
- Mover un entorno virtual rompe sus ejecutables (las rutas van escritas dentro); usar `env/bin/python -m ...`.
- La CPU tiene 4 núcleos: no medir tiempos mientras corre otra cosa pesada.
- Para esperar a procesos largos, usar tareas en segundo plano y Monitor, no `sleep`. Una tarea en segundo plano sin
  plazo se corta a los 30 min (cortó un lote de FLUX en la sesión 11): para lotes y renders largos, plazo de 2 h.
- No cargar otro modelo (BiRefNet, MusicGen) con el servidor de imágenes encendido: se acaba la RAM y el
  sistema lo mata. Apagarlo antes.
- FLUX escribe letras inventadas si el prompt habla de «espacio para un título»: describir solo la zona
  vacía y añadir «no text».
- HyperFrames: el desenfoque de movimiento se sale de las máscaras (`overflow: hidden`); `check` da falsos
  avisos de contraste con fondos escalados o recortados y con la palabra resaltada del subtítulo a medio pasar a la
  siguiente, pero no siempre es falso: en el gancho del Tic Tac el subtítulo blanco caía sobre espuma blanca (mirar
  siempre el fotograma); `media-treatment --apply` añade `data-hf-id` a todo
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
- MusicGen rinde más en lote: varias piezas en una sola llamada (4 a la vez, 1,7 veces más rápido). Con
  pistas de 30 s es mucho más lento que extrapolando desde 10 s: 2 a la vez tardaron 573 s.
- Para esperar a que acabe un proceso, no usar `pgrep -f` con un texto que también aparece en el propio
  bucle de espera: se encuentra a sí mismo y no termina nunca.
- Cargar cada modelo una vez por trabajo: voz y música antes que FLUX, o después de todo el lote de planchas.
- No editar un guion de bash mientras se ejecuta: bash lo lee sobre la marcha y falla (pasó con
  `preparar-apertura.sh`). Esperar a que acabe o escribir otro archivo.
- Supertonic da ya siempre la misma voz (semilla por frase en `voz/supertonic_frases.py`). Para encajar una toma
  nueva en una composición ya cronometrada, `voz/ajustar.py` (anclas en palabras; tramos de menos de un 5 %).
- Kit de vídeos largos (`videos/anticitera/kit/`): los montajes se anclan a palabras con `w("palabra", n)`; si la
  palabra sale más de una vez, `montar.py` lo avisa y hay que elegir la aparición. El de los cortos (`canales/businessformen/kit/montar.py`) también,
  desde el 1-nov, y con frases: `w('Su familia')` cogía «una despedida a su familia» y la escena entraba 13 s antes
  (`n=1` explícito calla el aviso). También avisa de las anclas de los rótulos (`["palabra", n, …]`) que caen fuera de
  su escena: «Años después» cogía «29 años» y se montaba encima de otro rótulo. Las etiquetas en versalitas
  ocupan unos 46 px por letra: junto a un dibujo, de 16 letras como mucho.
- HyperFrames toma cada HTML con `data-composition-id` de la raíz de un proyecto por otra composición
  (`multiple_root_compositions`): las plantillas, fuera (ver `canales/businessformen/marca/plantillas/`).
- En una subcomposición de HyperFrames el CSS queda encerrado bajo `[data-composition-id="…"]`: la raíz de la
  plantilla no puede llevar estilos (`subcomposition_root_styled_by_class`); va un contenedor interior. Ver
  `canales/businessformen/kit/README.md`.
- MusicGen ignora «no sub bass»: «pulse», «driving electronic» y las cuerdas punteadas salieron con el 71–99 % de la
  energía bajo 150 Hz. Funcionaron las cuerdas frotadas en ostinato con marimba (sesión 3; en la 7, la misma idea dio el
  98 %) y, dos veces de dos en la sesión 7, «solo piano and high strings» (6 y 7 %). Pedir varias candidatas y medir.
- Los golpes `impact-bass` de HyperFrames son subgrave puro y, a volumen 0,3–0,4, suben 5 LU por encima de la voz:
  entregar con `GRAVES=-20 PICO=-2 video/entregar.sh … -15 copiar` (comprime bajo 120 Hz sin recodificar el vídeo).
- Medir los graves de cada pieza de MusicGen antes de usarla (`audio/graves.py`): dos salieron con el 65–98 % de la
  energía bajo 150 Hz, que en un móvil no suena (ver la bitácora, sesión 3). La misma descripción con otra semilla
  puede salir con el 0 % o con el 85 %. Y mirar su energía por tramos: algunas se apagan a los 15–25 s.
- `mix-blend-mode: destination-out` no existe en CSS (el sello salía rosado): el desgaste de un sello va con
  `mask-image: url(desgaste.png)`.
- La etapa `musica` de `canales/preparar-corto.sh` empieza apagando el servidor de imágenes (para que quepa MusicGen): no
  lanzarla mientras otro proceso genera imágenes (en la sesión 7 cortó el lote de FLUX). Para rehacer solo un lecho,
  `audio/lecho.py` directamente. La etapa `imagenes` se salta las planchas que ya tienen PNG (retoma un lote cortado): para
  rehacer una, borrar su `.png`, su `_1920.png` y su `.jpg`. El servidor atiende de una en una: unas candidatas sueltas
  (`generar.py --lote`) se pueden pedir mientras corre un lote y se intercalan.
- La unidad en minúscula dentro de un rótulo (`8.849 m`) va en `<i class="m">`: un `span` dentro del `span` del rótulo
  hereda su caja y su filete naranja, y la «m» sale en una cajita aparte.
- Una imagen que falta sale en negro en el render: la avisa `montar.py` («faltan imágenes», desde la sesión 7) y, en la
  sesión 8, también el `check` (`missing_local_asset`), que entonces se salta todas las pruebas del navegador: para revisar
  antes de tener todas las planchas, una provisional en `proyecto/assets/img/` (nunca en `salidas/`: taparía la ampliación
  de la buena). En esta máquina no hay `/usr/bin/time`: medir con `$SECONDS`. Y un círculo SVG que nace sin radio, o con uno calculado negativo antes de su escena, da
  avisos del navegador en el render: radio inicial 0 y el tiempo de la escena, como mínimo, 0.
- El 2.5D por capas (`imagen/capas25d.py`) solo vale si el corte sigue el contorno de un objeto sobre un fondo liso: en
  una mesa, un pasillo o una pizza en su caja deja una franja borrosa. Mirarlo a tamaño real en el MP4, no en la hoja.
- En vertical, las mayúsculas de Inter Tight 800 ocupan unos 0,6 em por letra: calcular el ancho de cada línea
  (cabe en unos 880 px) o el titular parte en un renglón más y pisa lo de debajo.
- En las plantillas de escena, el `w()` de JavaScript solo acepta **una palabra** (`w("Por")`, no `w("Por eso")`): con dos
  da un error y la escena entera se queda sin animar (invisible). El de `montaje.py` sí acepta varias.
- Dentro de una escena, los tiempos de `w()` son desde que empieza la escena: si la escena entra después de la palabra,
  sale negativo. Un tween que empieza antes y acaba después ya va por la mitad en el primer fotograma (el contador de días
  empezaba en el 4); uno que **acaba** antes de que empiece la escena **no se aplica** (la 2.ª escena del hielo, en el
  corto 7, salía con el hielo entero y sin ella): lo que deba seguir hecho en una escena repetida va en `alBuscar`.
- `tl.fromTo` pinta su origen al crearse (`immediateRender`): un segundo `fromTo` sobre el mismo elemento, o uno que
  empieza visible, lo enseña antes de tiempo. `immediateRender: false` o empezar oculto con CSS.
- El lint de GSAP de HyperFrames rechaza animar `left`/`top` (`gsap_non_transform_motion`): mover con `x`/`y`.
- **Un trazo que «se dibuja» en un mapa con `vector-effect: non-scaling-stroke`**: Chrome mide `stroke-dasharray` y
  `stroke-dashoffset` en píxeles de pantalla, no en las unidades del dibujo. Con el largo de `getTotalLength()` tal cual, en
  cuanto la cámara acerca el mapa el trazo sale a trozos y empieza por el otro extremo (en el corto 17 iba por delante del
  barco). Multiplicar el largo por la escala de la cámara en cada fotograma: `trazo(x, k)` en los mapas de los cortos 17 y 18.
  Los mapas anteriores (Andes, Ghinsberg…) usan el largo sin escalar: revisarlos si se rehacen.
- En el JS de una plantilla no se puede llamar `f` a nada (`const f = $(".fecha")`): `f()` es de `ayuda.js`, la escena entera
  deja de funcionar y el `check` lo da como `invalid_inline_script_syntax`. Lo mismo que `L`, `traza`, `W`, `tl`…
- Los parámetros de `escena()` no pueden llamarse como los suyos: un camino del mapa llamado `entrada` se tomó por la
  transición de entrada (`KeyError` en `montar.py`).
- HyperFrames avisa (`composition_file_too_large`) de las composiciones de más de 300 líneas sin contar los estilos: con
  `ayuda.js` dentro, una plantilla de mapa con cinco modos llegó a 305. Comentarios cortos y líneas juntas.
- En un `<g>` de SVG, `transformOrigin: "0px 0px"` de GSAP cuenta desde la esquina de **su dibujo**, no desde el origen del
  SVG: con Australia entera (que llega a x −5.300) la cámara del mapa se desplazaba cientos de píxeles. Para una cámara
  sobre un mapa, `svgOrigin: "0 0"`. Y `vector-effect: non-scaling-stroke` en los trazos, si el zoom es grande.
- En SVG, el CSS de la plantilla pisa los atributos `fill` y `stroke`: `setAttribute('fill', …)` o un tween de `attr: { stroke }`
  no cambian nada si una regla CSS ya los fija (la barra de CO₂ del corto 12 seguía verde). Usar `el.style.fill` o tweens de
  `fill`/`stroke` como propiedades CSS.
- El halo oscuro de un rótulo SVG sobre un mapa (`paint-order: stroke`) pide un relleno opaco: con uno semitransparente el
  trazo se ve por dentro de la letra y el rótulo sale perfilado.
- Texto blanco sobre el naranja `#FF5E1A` da 2,6:1 y no se lee: texto oscuro (`#0b0a09`). Con amarillos y naranjas,
  medir el contraste antes de elegir el color del texto.
- **Los efectos de sonido se miden antes de renderizar** (`python3 audio/revisar_mezcla.py <proyecto>`, 0 avisos): en
  Juliane sonaban +1,4 LU por encima de la voz (el trueno y los golpes graves, hasta 15 LU) y la revisión por fotogramas
  no lo enseña. El `ebur128` de ffmpeg solo escribe la sonoridad de cada ventana con `-v verbose`.
- Una proyección azimutal centrada lejos de los continentes (el Pacífico) dibuja el que rodea el antípoda (África) como
  un anillo que tapa todo el mapa: dibujar solo la tierra a menos de unos 100° del centro.
- Callar la música del todo en un golpe deja silencios en las pausas de la voz (en el corto 7, dos de 0,3 s): bajarla
  (0,025), no callarla. `revisar_mezcla.py` avisa de los huecos de la mezcla antes de renderizar.
- `pkill -f` con un texto que también aparece en el propio comando mata la propia shell (salida 144) y deja el render a
  medias: matar por PID (`ps -eo pid,args`).
- `revisar_mezcla.py` mide en ventanas de 400 ms: un efecto a menos de 0,4 s de una palabra cuenta como «con voz» (8 LU
  bajo ella). Para que el whoosh de una transición caiga en la pausa, el corte va unos 0,38 s antes de la frase.
- Un ambiente rítmico (una máquina) muy bajo deja huecos entre golpe y golpe: bajo una pausa que no debe quedar en
  silencio, uno continuo (el viento desde dentro, BigSoundBank 1714).
- `video/entregar.sh` normaliza con loudnorm, que por el pico pasa a su modo dinámico: en un corto en bucle el final
  salía 5–6 dB más alto que el principio (el bucle saltaba) y el gancho, 2–4 dB más bajo que el resto. Los cortos se
  entregan con `BUCLE=1` (trata el sonido tres veces seguido y se queda el del medio). Un limitador con ganancia fija
  arreglaba el bucle, pero tenía que recortar unos 5 dB de los picos de la voz y el AAC acababa a −0,4 dBTP.

## Cómo decidir

- Antes de recomendar una herramienta o un modelo, probarlo aquí y medir tiempo y RAM. En la primera
  sesión las estimaciones fallaron en los dos sentidos.
- El banco de pruebas está en `imagen/pruebas/`: `comparar.py`, `sdcpp.py` y `hoja.py`.
- En los prompts de imagen, pedir también la composición (dónde va el sujeto y dónde queda espacio para
  el texto), con el mismo sufijo de dirección de arte en todo el vídeo.
