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

**Sesión 12 (6-nov-2026):** la sesión arrancó en el entorno «Default», con la red limitada y sin ningún dominio añadido:
Hugging Face daba 403 en el proxy y `./instalar.sh` se paraba al empezar. Una sesión en marcha no se puede pasar a un entorno
con red sin restricciones, así que se creó el entorno personal **«VIDEOS-AUTOMATIZADOS-»** (lo aprobó el usuario) con
exactamente estos dominios, y con ellos se instaló todo y se hicieron los cortos 17 y 18:

| Para qué | Dominios |
| --- | --- |
| Modelos y voces (Hugging Face y su CDN) | `huggingface.co`, `cdn-lfs.hf.co`, `cdn-lfs-us-1.hf.co`, `cdn-lfs-eu-1.hf.co`, `us.aws.cdn.hf.co`, `cas-bridge.xethub.hf.co`, `cas-server.xethub.hf.co`, `transfer.xethub.hf.co` |
| torch para CPU (el índice redirige ahora a `download-r2`) | `download.pytorch.org`, `download-r2.pytorch.org` |
| Fuentes (@fontsource) y mapas (world-atlas) | `cdn.jsdelivr.net` |
| Efectos CC0 | `bigsoundbank.com` |
| La extensión httpfs de DuckDB (rastreador) | `extensions.duckdb.org` |
| Contrastar los datos de los guiones | `en.wikipedia.org`, `es.wikipedia.org` |

PyPI, npm, `apt-get`, GitHub (git y `raw.githubusercontent.com`) entran con la casilla de gestores de paquetes o ya estaban.
La API de Wikipedia limita el ritmo (429): pedir los artículos de uno en uno, con unos segundos entre petición y petición.

**La clave de la API de YouTube** (para `rastreador/youtube.py`) no se puede guardar desde el formulario de credenciales de la
sesión: solo admite `Authorization: Bearer`, y Google responde 401 con esa cabecera. Se añade a mano en la configuración del
entorno (secretos de red) para `www.googleapis.com`, en la cabecera `X-Goog-Api-Key`. Sin ella el rastreador no puede medir.

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
