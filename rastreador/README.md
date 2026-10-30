# Rastreador de nichos

Para dejar de elegir temas a ciegas: medir qué nichos funcionan en vídeo corto en español, encontrar los vídeos que
superan a lo normal y desmontar su formato para hacer nuestra versión. Por qué estas fuentes y no otras:
[docs/investigacion-rastreador.md](../docs/investigacion-rastreador.md).

```bash
./instalar.sh rastreador                       # DuckDB con httpfs, yt-dlp y pytz en ~/herramientas-videos/rastreador
PY=~/herramientas-videos/rastreador/bin/python

# 1. El mapa: TikTok en español, con el dataset de 5.600 millones de vídeos (una vez al mes)
$PY rastreador/tiktok.py extraer 2026-09                       # los vídeos en español de un mes (unos 4,5 min)
$PY rastreador/tiktok.py nichos 2026-09 --minimo 300           # los nichos que más aciertan
$PY rastreador/tiktok.py tema 2026-09 negocio emprend finanz   # un tema: sus subnichos y sus vídeos con más vistas
$PY rastreador/tiktok.py atipicos 2026-09 ideasdenegocio       # los vídeos con más vistas de un nicho

# 2. Lo de esta semana: Shorts de YouTube que multiplican las vistas normales de su canal
python3 rastreador/youtube.py nicho "negociación" "historia de empresas" "ideas de negocio" --dias 30
python3 rastreador/youtube.py buscar "historia de empresas" --dias 30 --min-vistas 10000
python3 rastreador/youtube.py canal @canal

# 3. El porqué: planos, cortes, voz y gancho de un vídeo que el usuario sube a la sesión
python3 rastreador/desmontar.py video.mp4
```

Lo que sale va a `salidas/rastreador/` (fuera del repositorio). Las conclusiones de cada pasada, a `informes/`.

## Qué mide cada pieza

**`tiktok.py`** lee [datasocial/tiktok-5.6B-videos](https://huggingface.co/datasets/datasocial/tiktok-5.6B-videos)
(CC BY-NC 4.0; recogido con la API privada de la app, contra los términos de TikTok: solo para investigar, sin uso
comercial ni redistribución). Cuenta lo orgánico (sin anuncios ni colaboraciones pagadas) y solo vídeos de 7 a 31 días
cuando se midieron: antes de los 7 días aún no han hecho su recorrido (la mediana pasa de 240 vistas a 800).

- **Acierto:** la parte de los vídeos del nicho que llega a 100.000 vistas. **×:** ese acierto frente al de todo el
  idioma (en septiembre de 2026, el 5,2 %).
- **guard/mil** y **comp/mil:** guardados y compartidos por cada mil vistas. Lo útil se guarda; lo que se contagia se
  comparte.
- **IA:** la parte que TikTok marca como generada con IA.
- `--antes` compara con el mes anterior por **cuota** (la parte de los vídeos del mes que lleva el hashtag) y por ×.
  Es orientativo: el rastreo del dataset cambia cada mes (agosto se midió más tarde y con menos vídeos recientes que
  septiembre), así que las cifras absolutas de dos meses no se comparan.

**`youtube.py`** usa la API de datos de YouTube (la clave la añade el proxy del entorno: secreto `X-Goog-Api-Key` para
`www.googleapis.com`) y el RSS de cada canal, que da sus 15 últimos vídeos con las vistas, gratis y sin cuota.

- **×canal:** vistas del Short / mediana de los otros Shorts recientes de su canal. Un 10× en un canal pequeño vale más
  que un millón de vistas en uno que siempre tiene un millón: la idea funciona sin audiencia detrás.
- **v/h:** vistas por hora desde que se publicó. **v/sub:** vistas / suscriptores.
- Busca por relevancia y se queda con lo que declara el idioma: ordenando por vistas, la API no hace caso del idioma
  (para «ideas de negocio», 0 de 50 en español; por relevancia, 34–44 de 50).
- Cada búsqueda de dos páginas gasta unas 202 de las 10.000 unidades diarias. Lo que guarda la API se borra o se
  refresca antes de 30 días (lo pide su política): en el repositorio, solo conclusiones.

**`desmontar.py`** trabaja sobre un archivo: desde esta máquina YouTube pide «Sign in to confirm you're not a bot» (y da
403 al bajar el vídeo) y TikTok rechaza la petición. No hay que saltarse esos bloqueos: el vídeo lo guarda el usuario
desde la app y lo sube. Da los planos (detección de escenas de ffmpeg), la transcripción con tiempos (whisper small en
español, el de HyperFrames), las palabras por segundo, el gancho de los 3 primeros segundos y una hoja con un fotograma
de cada plano. Se copia la mecánica; nunca el guion, la voz ni las imágenes.

## Medido aquí (30-oct-2026, Xeon con AMX)

| Tarea | Tiempo | Notas |
| --- | --- | --- |
| Instalar el rastreador | 22 s (2 s con la caché de uv) | 81 MB más la extensión httpfs (27 MB) |
| Extraer un mes de TikTok en español | 263–271 s | 5,0–5,1 M vídeos; se leen unos 3,7 GB por columnas y quedan 224–230 MB; 5,4 GB de RAM |
| Ranking de nichos, un tema, atípicos | 6–16 s | sobre el parquet local |
| Una búsqueda de Shorts (100 resultados) | 3–5 s | unas 202 unidades de cuota |
| Doce búsquedas de nichos en Shorts | 66 s | unas 2.450 unidades |
| Desmontar un vídeo de 7 s | 95 s la primera vez (baja whisper small, 488 MB); después, segundos | cortes en 0,3 s |

## Límites que hay que tener presentes

- El dataset no dice quién publica cada vídeo: un nicho pequeño puede ser un solo creador muy visto.
- Está muy cargado hacia Estados Unidos (55 de los 99 millones de vídeos de septiembre); en español, 5 millones al mes,
  la mitad publicados desde Estados Unidos.
- El acierto mide vistas, no si el canal gana suscriptores ni si el vídeo vende.
- YouTube: el RSS solo da 15 vídeos por canal; un canal con pocos Shorts recientes sale sin ×canal.
