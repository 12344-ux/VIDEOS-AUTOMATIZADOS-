# Investigación: edición y motion graphics de nivel profesional, por código

29 de octubre de 2026. Objetivo: que cada sesión pueda editar vídeos largos con calidad de agencia
(tipografía en movimiento, transiciones con intención, gráficos, efectos, ritmo, sonido), donde las
imágenes generadas sean un recurso más del montaje y no el vídeo entero.

## En corto

- **Motor recomendado: [HyperFrames](https://github.com/heygen-com/hyperframes)** (HeyGen, Apache 2.0,
  v0.8.216 en npm). El vídeo se escribe como HTML + CSS y se anima con GSAP, Lottie, Three.js o Anime.js;
  Chrome sin interfaz pinta cada cuadro y FFmpeg lo codifica, así que el render es exacto y repetible.
  Está pensado para agentes como Claude y trae lo que convierte «animar» en «dirigir»: unos 450 bloques
  listos (transiciones con shaders, tipografía cinética, rótulos, gráficos, mapas, grano, destellos,
  movimientos de cámara), reglas de motion medidas cuadro a cuadro en películas profesionales, un método
  de guion y otro de revisión, y herramientas locales de color, recortes, ritmo y volumen.
- **Animación: GSAP 3.15**, el estándar de la animación web, gratis desde 2025 con todos sus plugins
  (SplitText, MorphSVG…).
- **Imagen: FLUX.3 Image Klein** sigue siendo el mejor modelo viable en esta CPU (37 s por imagen a
  512 px, 53 s a 768 × 432). Los líderes de los rankings no caben o serían lentísimos aquí.
- **Para que esté en cada sesión:** las skills de HyperFrames (Apache 2.0) y nuestra propia guía de
  estilo pueden vivir en `.claude/skills/` de este repositorio, que Claude carga al abrirlo.

## Motores de vídeo por código

| Proyecto | Licencia | Cómo se escribe | A favor | En contra |
| --- | --- | --- | --- | --- |
| **HyperFrames** (HeyGen) | Apache 2.0, sin límites de uso | HTML + CSS + GSAP/Lottie/Three.js | Hecho para agentes; sin compilación; 450 bloques; skills de dirección; QA integrado (`check`, `snapshot --review`, aserciones de movimiento); color, recortes, ritmo y volumen locales | Joven (2026) y cambia casi a diario; render por captura de cuadros, más lento que Remotion en piezas simples |
| **Remotion** | Propia: gratis para personas y empresas de hasta 3 empleados | Componentes de React | El más maduro; skills oficiales para Claude Code (enero de 2026); render en la nube | Hace falta React y un empaquetador; licencia de pago al crecer |
| **Revideo** (fork de Motion Canvas) | MIT | Generadores de TypeScript | Render sin interfaz | Su hoja de ruta sigue a un producto comercial |
| **Motion Canvas** | MIT | Generadores de TypeScript | Excelente para animaciones explicativas | Sin render sin interfaz de serie |
| **html-video** (Open Design) | Apache 2.0 | Plantillas HTML sobre HyperFrames | 21 plantillas y storyboard por escenas | Capa extra sobre HyperFrames |
| Editly, FFCreator | MIT | JSON o JavaScript | Simples | Nivel de pase de diapositivas |

Lo que inclina la balanza hacia HyperFrames: Claude escribe HTML y CSS con soltura, la licencia no pone
condiciones y, sobre todo, trae el oficio escrito, no solo la herramienta.

### El oficio que trae HyperFrames (resumen de sus guías)

Medido cuadro a cuadro en sus películas de lanzamiento oficiales:

- **Movimientos:** un movimiento rápido dura 0,3–0,6 s y lleva desenfoque de movimiento en su punto más rápido.
- **Curvas según el papel:** una llegada aterriza con cola larga (`expo.out`, `power4.out`); un movimiento
  de cámara o una inundación de color, `power2.inOut`; un zoom a través o una salida acelera (`power3.in`).
  La misma curva en todo es «la curva plana por defecto».
- **Muelles:** amortiguación de 0,7–0,85 se lee premium; 0,4–0,6, juguetón; por debajo de 0,3, dibujo animado.
- **Salidas** un 40–50 % más cortas que las entradas. **Solape:** lo siguiente empieza cuando lo anterior
  va por el 30–50 %. **Escalonado:** letras a un cuadro, palabras a 60–120 ms, elementos de lista a 40–80 ms.
- **Cortes** en el cuadro más rápido del movimiento, con la misma dirección y velocidad a ambos lados.
- **Títulos:** quietos del todo cuando aterrizan; el movimiento pasa al siguiente elemento. Variar la
  entrada (palabra a palabra con desenfoque de 6 px a 0, de gris a tinta, letra a letra para un nombre…).
- **Lectura:** una línea se sostiene 0,5 s + 0,3 s por palabra; la última de la película, al menos 2 s.
- **Tamaño:** títulos al 4–9 % de la altura del cuadro; un solo color de acento, y con significado.
- **Ritmo:** planos de 1,8–3 s de media con movimiento dentro; montajes de 0,13–0,8 s; pausa de
  0,3–0,75 s antes del remate.
- **Transiciones con causa:** 3–5 tipos por película, cada una provocada por algo en pantalla: zoom a
  través de un elemento, el objeto se convierte en el mundo, morph, arrastre, inundación de color, barrido
  (whip), iris desde un punto, corte con oscurecido, cambio con desenfoque. Nunca un fundido entre mundos.
- **Lo que delata lo generado por máquina:** títulos que respiran o flotan, escalado lento eterno,
  rebote en interfaces, anillos al hacer clic, la misma curva en todo.
- **Guion:** una voz sintética lee unas 2,2 palabras por segundo. Unas 19 palabras por escena (9 s).
  Revelar cada elemento cuando la voz lo nombra, no todo al principio.
- **Música:** un movimiento que debe caer en un golpe empieza 40–190 ms antes; el golpe es instantáneo.
  Cualquier tratamiento se agota a los 6 s.
- **Revisión:** describir cada fotograma clave como lo haría un desconocido; problemas P0, P1 y P2;
  comprobar a ancho de móvil (360 px).

## Recursos de apoyo para el montaje

| Necesidad | Herramienta | Licencia | Nota |
| --- | --- | --- | --- |
| Imágenes base («planchas») | FLUX.3 Image Klein INT4 (FastSD CPU) | FLUX Kommunity | Ya instalado; edita con hasta 10 referencias, clave para la coherencia entre escenas |
| Bocetos y storyboard | SDXS (FastSD CPU) | OpenRAIL++ | 0,5 s por imagen: 40 miniaturas en 20 s |
| Recortes de objetos | BiRefNet (vía rembg u ONNX) | MIT | La mejor calidad abierta; ~15 s por imagen en un portátil Apple. RMBG-2.0 es no comercial |
| Recortes de personas | `u2net_human_seg` (el de HyperFrames) | — | Solo personas |
| Profundidad para 2.5D | Depth Anything V2 Small (ONNX) | Apache 2.0 | Paralaje y movimientos de cámara sobre una imagen fija |
| Ampliación a 1080p | EDSR (FastSD) o ESRGAN (stable-diffusion.cpp) | — | Para planchas generadas a menor resolución |
| Color, LUT, grano, viñeta | `hyperframes media-treatment` | Apache 2.0 | Un look coherente en todo el vídeo |
| Voz | Piper (instalado) o Kokoro (el que integra HyperFrames) | GPL-3.0 / Apache 2.0 | Comparar en español antes de decidir |
| Subtítulos palabra a palabra | Alineaciones de Piper, o `hyperframes transcribe` (whisper.cpp, Parakeet) | — | Para subtítulos cinéticos |
| Música | Nuestro `audio/musica.py`; Stable Audio Open Small para texturas | — / Stability Community | Las bibliotecas de pago de HeyGen requieren cuenta |
| Efectos de sonido | 21 incluidos en HyperFrames + Openverse (CC0 / CC BY) | varias | Openverse responde desde aquí |
| Tipografías | 18 incluidas en HyperFrames + Fontsource (OFL) por npm | OFL | Instrument Serif y Caveat probadas aquí |

## Por qué no el mejor modelo de los rankings

Los líderes abiertos en octubre de 2026 son Qwen-Image-2.1 (licencia no comercial) e Ideogram 4.0.
Qwen-Image-2.1 ocupa 4,2 GB cuantizado más 5 GB de codificador de texto y solo corre con
stable-diffusion.cpp, que aquí tardó 5,5 min por imagen con un modelo la mitad de grande: unos 20 min
estimados. Ideogram 4 pide más de 27 GB y cuenta en Hugging Face. FLUX.3 Image Klein en OpenVINO es,
con diferencia, la mejor relación calidad/tiempo en esta máquina.

## Detalles prácticos comprobados (sin instalar nada)

- HyperFrames necesita Node 22+ y FFmpeg: los dos están.
- Usa su propio Chrome, pero acepta otro con `HYPERFRAMES_BROWSER_PATH`: aquí está
  `/opt/pw-browsers/chromium_headless_shell-1243/…/chrome-headless-shell`.
- Envía estadísticas de uso anónimas (PostHog); se apagan con `HYPERFRAMES_NO_TELEMETRY=1`.
- Carga GSAP desde jsDelivr y algunas fuentes desde Google Fonts; jsDelivr responde desde aquí.
- Sus herramientas de HeyGen (catálogo de música, avatares, voces) piden cuenta; no hacen falta.

## Pendiente de probar (con permiso)

1. Instalar HyperFrames y medir cuánto tarda en renderizar aquí (no hay cifras de CPU publicadas fiables).
2. Comparar Piper y Kokoro en español.
3. BiRefNet y Depth Anything V2 Small: velocidad y calidad en esta CPU.
4. Un tráiler de 20–30 s en el estilo elegido, de principio a fin.

## Fuentes

- [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) y sus skills: `skills/hyperframes/references/motion.md`, `film.md`, `story.md`, `review.md`, `look.md`, `types/explainer.md` y `skills/media-use/` (leídas el 29-oct-2026)
- [hyperframes en npm](https://www.npmjs.com/package/hyperframes)
- [Remotion: plugin para Claude Code](https://www.remotion.dev/docs/ai/claude-code-plugin), [remotion-dev/skills](https://github.com/remotion-dev/skills), [licencia de Remotion](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md)
- [nexu-io/html-video](https://github.com/nexu-io/html-video), [midrender/revideo](https://github.com/midrender/revideo), [motion-canvas/motion-canvas](https://github.com/motion-canvas/motion-canvas)
- [Comparativa de alternativas a Remotion](https://github.com/a1adams/remotion-alternatives)
- Sobre HyperFrames: [The Menon Lab](https://themenonlab.blog/blog/heygen-hyperframes-video-as-code), [guía de rendimiento](https://hyperframes.heygen.com/guides/performance), [reseña en DEV](https://dev.to/andrew-ooo/hyperframes-review-heygens-html-to-video-for-ai-agents-170i)
- GSAP gratis: [Webflow](https://webflow.com/blog/gsap-becomes-free), [licencia estándar](https://gsap.com/community/standard-license/)
- Recortes: [comparativa de modelos](https://aireiter.com/blog/best-background-removal-api), [RMBG-2.0](https://www.analyticsvidhya.com/blog/2025/03/rmgb-v2-0/)
- Profundidad: [Depth Anything 3 small](https://huggingface.co/depth-anything/da3-small), [paralaje con Depth Anything V2](https://habr.com/en/articles/897860)
- Música: [ACE-Step 1.5](https://github.com/ace-step/ACE-Step-1.5), [Stable Audio Open Small](https://www.alternativeto.net/news/2025/5/stability-ai-open-sources-an-audio-model-that-can-run-on-smartphones-with-arm-cpus/)
- Voz: [comparativa de TTS en el dispositivo](https://picovoice.ai/blog/on-device-tts/), [TTS abiertos 2026](https://ocdevel.com/blog/20250720-tts)
- Modelos de imagen: [ranking de Artificial Analysis](https://artificialanalysis.ai/image/leaderboard/text-to-image?open-weights=true), [modelos para autoalojar](https://pinggy.io/blog/best_free_open_source_ai_image_generators_to_self_host/)
