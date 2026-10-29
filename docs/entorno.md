# El entorno y cómo no reinstalar a mano

Cada sesión de Claude Code en la nube arranca en una máquina nueva. Lo que se guarda es lo que está
en este repositorio; lo instalado (unos 12 GB entre programas y modelos) desaparece al cerrar la
sesión. Los modelos no pueden ir en git: pesan varios GB y GitHub no admite archivos tan grandes.

## Opción 1: que se instale solo al abrir cada sesión

En la configuración del entorno (menú del entorno en la barra de título de la sesión → **Edit**), en
**Setup script**, añade:

```bash
cd videos-automatizados- && ./instalar.sh
```

El script de preparación empieza una carpeta por encima del repositorio, por eso va el `cd`. Se
ejecuta al arrancar cada sesión nueva, así que la sesión tardará unos 5–10 minutos más en estar lista.

## Opción 2: instalar cuando haga falta

Sin tocar la configuración: al empezar, Claude ejecuta `./instalar.sh comprobar` y, si falta algo,
lanza `./instalar.sh` en segundo plano mientras trabaja en el guion o en lo que no necesite las
herramientas. Es lo que pide `CLAUDE.md`.

## Qué necesita la red del entorno

En **Network access → Allowed domains**:

- `huggingface.co` y su CDN: `*.hf.co` (o al menos `us.aws.cdn.hf.co`). Sin la CDN, la página de
  Hugging Face responde, pero los modelos no bajan.
- Dejar marcada la casilla de gestores de paquetes (PyPI y similares).

El resto (download.pytorch.org, código de GitHub) ya estaba accesible en la primera sesión.

## Para guardar cambios en GitHub

Para que Claude pueda subir commits a este repositorio, la app de Claude para GitHub tiene que tener
acceso a él: instálala en <https://github.com/apps/claude/installations/select_target> o vuelve a
conectar GitHub desde la configuración de claude.ai.

## La máquina (comprobado el 29-oct-2026)

| Recurso | Qué hay |
| --- | --- |
| CPU | Intel Xeon, 4 núcleos a 2,1 GHz, con AMX, AVX-512 BF16 y VNNI |
| Memoria | 15 GB de RAM |
| Disco | unos 30 GB libres por sesión |
| GPU | ninguna |
| Programas | python3.11 y 3.13, uv, gcc 13, cmake 3.28, ffmpeg 6.1, Node 22, Playwright + Chromium, fuentes Inter |

Lo que ocupa la instalación completa:

| Componente | Disco |
| --- | --- |
| FastSD CPU y su entorno de Python | 2,5 GB |
| Modelos de imagen: FLUX.3 Klein + SDXS + TAESD | ~8 GB |
| FLUX.2 klein 4B (opcional, `imagen-extra`) | 4,6 GB |
| Piper y dos voces | 0,4 GB |
| stable-diffusion.cpp y sus modelos (opcional, `sdcpp`) | 6,5 GB |
