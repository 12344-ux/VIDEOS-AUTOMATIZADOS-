# Investigación: generar imágenes sin GPU

29 de octubre de 2026. Objetivo: imágenes que sean «representaciones bastante asemejadas a lo real y que
se entienda lo que son», hechas en la CPU de la sesión, sin servicios externos.

## En corto

Hay tres caminos, y los tres funcionan aquí:

1. **Modelos de difusión en la CPU.** Lo más parecido a pedir «haz una imagen de…». Con FastSD CPU
   (OpenVINO), FLUX.3 Image Klein hace una imagen de 512 px en unos 37 s con calidad casi fotográfica,
   y SDXS hace bocetos en medio segundo.
2. **Ilustración por código** (SVG y canvas). Funciona sin instalar nada; siempre se ve como ilustración.
3. **Recursos abiertos y 3D** (Fluent Emoji 3D, Poly Haven). Útiles como complemento.

## Resultados medidos en esta máquina

Mismos tres textos (un bolso de cuero terracota, una taza de café y un golden retriever en un parque),
misma semilla, 512 × 512 px, pidiendo ilustración semirrealista. Prompts en
[`imagen/pruebas/prompts.json`](../imagen/pruebas/prompts.json).

![Comparativa de modelos y motores](resultados/comparativa.jpg)

| Modelo | Motor | Primera imagen (con carga) | Siguientes | RAM máx. | Calidad |
| --- | --- | --- | --- | --- | --- |
| **FLUX.3 Image Klein** INT4 | FastSD CPU (OpenVINO) | 73 s | **37–39 s** | 8,2 GB | Muy buena, la más nítida; toma el prompt al pie de la letra |
| **FLUX.2 klein 4B** INT4 | FastSD CPU (OpenVINO) | 58 s | **39–43 s** | 9,3 GB | Muy buena, licencia Apache 2.0 |
| FLUX.2 klein 4B Q4_0 | stable-diffusion.cpp | 330 s | 330–348 s* | 5,8 GB | Muy buena; en una imagen inventó una firma |
| **SDXS-512** | FastSD CPU (OpenVINO + TAESD) | 14 s | **0,5 s** | 5,0 GB | Buena para bocetos; deforma detalles |
| SDXS-512 | stable-diffusion.cpp | 7 s | 7 s* | 1,3 GB | Parecida |

\* stable-diffusion.cpp se usó con su programa de línea de comandos, que recarga el modelo en cada imagen.
En FLUX.2 la carga apenas cuenta: de 330 s, 292 fueron de difusión y 32 de decodificar.

### Lo que aprendimos

- **El motor importa más que el modelo.** El mismo FLUX.2 klein tardó 330 s con stable-diffusion.cpp y
  40 s con OpenVINO. Lo más probable es que OpenVINO aproveche la aceleración AMX del Xeon.
- **Las estimaciones fallaron en los dos sentidos:** FLUX.3 (estimado 1–2 min, real 37 s), SDXS (2–4 s,
  real 0,5 s), FLUX.2 en stable-diffusion.cpp (1,5–4 min, real 5,5 min). Con OpenVINO, esta máquina
  rinde como el Core i7-12700 de escritorio de las pruebas publicadas. Conclusión: medir antes de recomendar.
- **FLUX entiende muy bien el texto** (luz de ventana, vapor, madera, parque soleado), a veces demasiado:
  «small gold rings» llenó el bolso de anillas.

## Modelos para CPU que valen la pena

| Modelo | Para qué | Publicado* | Aquí | RAM | Descarga | Licencia | ¿Sin cuenta? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FLUX.3 Image Klein INT4 (FastSD) | La mejor calidad viable. Edita con hasta 10 referencias | ~36 s | **37–39 s** | 8,2 GB | 5,6 GB | FLUX Kommunity: gratis por debajo de 5 M$/año | Sí |
| FLUX.2 klein 4B (FastSD o sd.cpp) | Buena calidad, licencia libre. También edita | 61 s (Mac) | **39–43 s** (OpenVINO) | 9,3 GB | 4,6–5 GB | Apache 2.0 | Sí |
| Iris-3B Turbo INT8 (FastSD) | 1024 px directo, sin VAE | ~90 s (1024 px) | ~90 s (estimado) | 8,4 GB | 6,9 GB | Apache 2.0 | Sí |
| Z-Image-Turbo (sd.cpp) | Calidad alta y buen texto dentro de la imagen | sin datos | ~15 min (estimado) | 7–8 GB | ~7 GB | Apache 2.0 | Sí, con el VAE de Comfy-Org |
| SD-Turbo (FastSD) | Bocetos a 512 px | 1,7 s | 1–2 s (estimado) | 2–11 GB según modo | — | Solo investigación y no comercial | Sí |
| SDXS-512 (FastSD o sd.cpp) | Lo más rápido | 0,82 s | **0,5 s** | 5,0 GB | 0,7–0,9 GB | OpenRAIL++ | Sí |

\* Tiempos de los autores en un Core i7-12700 (512 px salvo indicación), y de FLUX.2 klein en un Mac.
«¿Sin cuenta?» = se descarga sin iniciar sesión en Hugging Face (comprobado con cada repositorio).
Ojo: el VAE oficial de FLUX.2-dev y el de FLUX.1-schnell sí piden cuenta; hay copias libres en los
paquetes de manishdashsharma y de Comfy-Org.

**No caben aquí:** FLUX.1-schnell en OpenVINO (30 GB de RAM), Qwen-Image (20 mil millones de
parámetros), MOSS-Image (codificador Qwen3.5 9B) y Lens (codificador GPT-OSS-20B).

## Las herramientas

| Proyecto | Cómo es | A favor | En contra |
| --- | --- | --- | --- |
| **FastSD CPU** (rupeshs, MIT) | Python + OpenVINO, el motor de Intel | Pensado para CPU Intel; aquí, unas 8 veces más rápido con el mismo modelo. CLI, web, API y servidor MCP | Instalación pesada (2,5 GB de Python); su API devuelve JPEG |
| **stable-diffusion.cpp** (leejet, MIT) | Un programa en C++, sin dependencias | El catálogo más amplio (más de 40 modelos), formato GGUF | En esta CPU, mucho más lento; compilarlo lleva unos 25 min |

También revisados: OnnxStream (para muy poca memoria, tipo Raspberry Pi; aquí no hace falta),
diffusers con PyTorch (el estándar, pero más lento en CPU) y servidores MCP que envuelven estos
motores (DiffuGen, sdmcp y el de FastSD CPU).

## Caminos sin modelos generativos

**Ilustración por código.** Formas, degradados, brillos y sombras en SVG, convertidos a imagen con
Chromium. Fuente: [`ejemplos/ilustraciones-svg.html`](ejemplos/ilustraciones-svg.html).

![Ilustraciones SVG](resultados/ilustraciones-svg.jpg)

A favor: instantáneo, editable, vectorial y animable. En contra: siempre parece ilustración; personas,
animales y escenas complejas quedan mucho menos naturales.

**Recursos abiertos y 3D.**

- Fluent Emoji 3D de Microsoft (MIT): unos 1.500 objetos en estilo 3D, accesibles por jsDelivr.
- Poly Haven (CC0): 521 modelos 3D y fondos de iluminación. Para renderizarlos hace falta three.js o
  Blender (`bpy` 5.2.3 en PyPI, 403 MB). No se probaron.
- Objaverse (Hugging Face): unos 800.000 modelos 3D con licencias variadas.
- Modelos de texto a SVG (OmniSVG 1.1, StarVector): de investigación y pensados para GPU.

## Complementos útiles

- `vtracer` (PyPI): pasa una imagen generada a SVG editable.
- `rembg` (MIT): quita el fondo de una foto.
- Edición con imágenes de referencia (FLUX.2 klein y FLUX.3 Klein): partir de una foto real y cambiar la escena.
- Ampliación: EDSR en FastSD (`--upscale`) y ESRGAN en stable-diffusion.cpp.

## Servicios en internet (descartados)

Pollinations.ai tiene una entrada gratuita sin clave y con límite de uso; Hugging Face, OpenAI y
Google ofrecen APIs con clave y coste. En todos, el texto de cada imagen sale del entorno hacia sus
servidores; Pollinations dice no guardar nada, pero nadie lo ha verificado.

## Fuentes

- [rupeshs/fastsdcpu](https://github.com/rupeshs/fastsdcpu) (README del 25-oct-2026: tiempos, RAM, FLUX.3 Klein e Iris-3B en OpenVINO)
- [leejet/stable-diffusion.cpp](https://github.com/leejet/stable-diffusion.cpp) y su documentación de [FLUX.2](https://github.com/leejet/stable-diffusion.cpp/blob/master/docs/flux2.md), [FLUX.3](https://github.com/leejet/stable-diffusion.cpp/blob/master/docs/flux3.md), [Z-Image](https://github.com/leejet/stable-diffusion.cpp/blob/master/docs/z_image.md) y [modelos destilados](https://github.com/leejet/stable-diffusion.cpp/blob/master/docs/distilled_sd.md)
- [manishdashsharma/flux2-klein-cpu](https://github.com/manishdashsharma/flux2-klein-cpu) y su [paquete en Hugging Face](https://huggingface.co/manishdashsharma/flux2-klein-4b-gguf)
- Modelos: [leejet/FLUX.2-klein-4B-GGUF](https://huggingface.co/leejet/FLUX.2-klein-4B-GGUF), [leejet/Z-Image-Turbo-GGUF](https://huggingface.co/leejet/Z-Image-Turbo-GGUF), [rupeshs/flux3-image-klein-int4-ov](https://huggingface.co/rupeshs/flux3-image-klein-int4-ov), [rupeshs/flux2-klein-4b-int4-ov](https://huggingface.co/rupeshs/flux2-klein-4b-int4-ov), [rupeshs/iris-3b-int8-ov](https://huggingface.co/rupeshs/iris-3b-int8-ov), [rupeshs/sdxs-512-0.9-openvino](https://huggingface.co/rupeshs/sdxs-512-0.9-openvino)
- FLUX.3 Image Klein: [VentureBeat](https://venturebeat.com/technology/black-forest-labs-opens-flux-3-image-klein-weights-with-free-commercial-use-limited-to-smaller-businesses), [The Decoder](https://the-decoder.com/black-forest-labs-open-weights-image-model-flux-3-image-klein-runs-on-consumer-gpus-with-just-8-gb-of-vram/), [OrcaRouter](https://www.orcarouter.ai/blog/flux-3-image-klein-launch)
- [vitoplantamura/OnnxStream](https://github.com/vitoplantamura/OnnxStream)
- [OmniSVG](https://github.com/OmniSVG/OmniSVG) y [StarVector](https://github.com/joanrod/star-vector)
- Servidores MCP: [skeeto/sdmcp](https://github.com/skeeto/sdmcp), [DiffuGen](https://glama.ai/mcp/servers/@CLOUDWERX-DEV/DiffuGen/blob/7f495aead20e96650a7cda7bd4b6184d3f89e869/README.md), [image-generation-mcp](https://glama.ai/mcp/servers/pvliesdonk/image-generation-mcp)
- [microsoft/fluentui-emoji](https://github.com/microsoft/fluentui-emoji), [Poly Haven](https://polyhaven.com), [Objaverse](https://huggingface.co/datasets/allenai/objaverse)
- Pollinations: [comparativa de Novita](https://blogs.novita.ai/free-ai-image-generation-api-no-key-required/), [ficha del proyecto](https://awesome.ecosyste.ms/projects/github.com%2Fpollinations%2Fpollinations)
- Dibujo de SVG con modelos de lenguaje: [Simon Willison, «pelican riding a bicycle»](https://feeds.simonwillison.net/tags/pelican-riding-a-bicycle)
