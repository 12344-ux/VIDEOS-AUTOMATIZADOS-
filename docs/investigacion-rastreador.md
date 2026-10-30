# Investigación: un rastreador de nichos y vídeos virales para cortos

30 de octubre de 2026. Objetivo: dejar de elegir temas a ciegas. Encontrar con datos qué nichos tiran en vídeo
corto (Reels, TikTok, Shorts) en español, y vídeos concretos que funcionan, para estudiar su formato y hacer nuestra
versión con el kit del canal.

## En corto

- **No hay una herramienta abierta que lo haga todo** (TikTok, Reels y Shorts, en español y con métricas fiables).
  Lo que existe se reparte en cuatro grupos: buscadores de vídeos atípicos de YouTube (maduros, con la API oficial
  gratuita), scrapers no oficiales de TikTok e Instagram (frágiles, contra sus términos, piden cuenta o proxys),
  monitores de noticias en tendencia y servicios de pago.
- **El hallazgo: un dataset público con 5.598 millones de vídeos de TikTok** en Hugging Face
  ([`datasocial/tiktok-5.6B-videos`](https://huggingface.co/datasets/datasocial/tiktok-5.6B-videos)). Trae vistas,
  likes, comentarios, compartidos, guardados, idioma, país, hashtags, texto en pantalla, duración y la marca de IA de
  TikTok, en un archivo por mes de julio de 2014 a octubre de 2026 (460 GB en parquet). Permite medir nichos en
  español con datos reales, leyendo solo las columnas y los países que hacen falta. **Pega:** se recogió con la API
  privada de la app de TikTok, contra sus términos, y su licencia es no comercial (CC BY-NC 4.0).
- **Para Shorts: la API oficial de YouTube** (clave gratuita, 10.000 unidades al día) más **el RSS de cada canal**
  (gratis y sin cuota: sus 15 últimos vídeos con las vistas, y los Shorts se distinguen por el enlace). Con eso sale
  el método de las mejores herramientas: cuántas veces multiplica un Short la mediana de su propio canal.
- **Instagram: sin una fuente fiable con vistas.** La API oficial no da vistas en la búsqueda por hashtag, e
  instaloader pide iniciar sesión y arriesga bloqueos. TikTok sirve de indicador: los mismos formatos se suben a las
  dos.
- **Recomendación:** un rastreador propio y pequeño con esas piezas y el método de los «outliers», más un desmontaje
  de cada vídeo atípico (gancho, cortes, estructura) para recrear la mecánica, nunca el contenido.

## Qué llega desde esta máquina (probado el 30-oct-2026)

| Fuente | Respuesta | Qué da |
| --- | --- | --- |
| YouTube, web y RSS de canal | 200 | El RSS da los 15 últimos vídeos con sus vistas; los Shorts llevan `/shorts/` en el enlace (probado con un canal grande). La lista de solo Shorts (`UUSH…`) da 404 por RSS |
| API de datos de YouTube (`googleapis.com`) | 403 sin clave | Responde «unregistered callers»: solo falta la clave |
| TikTok, web | 200 | — |
| TikTok Creative Center | 301 → 200 | Redirige a `ads.tiktok.com/creative/creativeCenter/trends`, «TikTok One Creative Suite»: una aplicación que carga los datos en el navegador; el HTML no trae ninguno |
| Instagram, web; Graph API de Meta | 200; 400 sin token | — |
| Google Trends, RSS de búsquedas en tendencia | 200 | 10 por país con su tráfico aproximado (ES, MX, CO, AR y US): actualidad (fútbol, famosos), no nichos |
| Reddit (JSON público) | 403 | — |
| API de GitHub | bloqueada en esta sesión | Los README se leen por `raw.githubusercontent.com`; la fecha del último commit, con `git clone --filter=blob:none --no-checkout` (sin bajar el código) |
| Hugging Face: API y visor de datasets | 200 | El visor lee filas del dataset de TikTok, pero su filtro da error 500 con 5.600 millones de filas: hace falta un motor de consultas propio (DuckDB) |

## Candidatos

### Shorts de YouTube: buscadores de vídeos atípicos

| Proyecto | Licencia | Último commit | Datos | Qué hace | Para nosotros |
| --- | --- | --- | --- | --- | --- |
| [AdesiaHQ/bangermap-integrations](https://github.com/AdesiaHQ/bangermap-integrations) | MIT | 10-ago-2026 | API de YouTube (clave) | Servidor MCP y skill: el múltiplo de cada vídeo sobre la línea base de su canal; barrer un nicho desde un canal semilla | El método más claro. En TypeScript (`npx`); unas 5 unidades por canal |
| [svx2027/yt-competitor-outlier-pipeline](https://github.com/svx2027/yt-competitor-outlier-pipeline) | MIT | 26-oct-2026 | yt-dlp, sin clave | Lee las pestañas `/videos`, `/shorts` y `/streams` de un canal; múltiplo sobre la mediana de cada formato (3× o 5×) y comprobación de que no falta ningún vídeo | Bueno para estudiar a fondo competidores concretos sin gastar cuota |
| [Xeron2000/viral-shorts](https://github.com/Xeron2000/viral-shorts) | MIT | 30-nov-2025 | API de YouTube (clave) | Servidor MCP: Shorts por tema y por horas, vistas por hora, engagement y combinaciones de palabras con muchas vistas por hora dentro de un tema (subnichos) | La idea de los subnichos por palabras es buena; parado desde hace 11 meses y con 10 resultados por búsqueda |
| [jobtanut/Outlier-Lab](https://github.com/jobtanut/Outlier-Lab) | MIT | 27-oct-2026 | API de YouTube y, opcional, la de Analytics | Tablero local de atípicos con umbrales según el tamaño del canal (3×, 5×, 10×), búsqueda por formato de título y encaje con tu audiencia | Solo vídeos largos (excluye Shorts): sirve para los vídeos largos del canal |

### TikTok

| Proyecto | Licencia | Actividad | Qué es | Para nosotros |
| --- | --- | --- | --- | --- |
| [datasocial/tiktok-5.6B-videos](https://huggingface.co/datasets/datasocial/tiktok-5.6B-videos) (Hugging Face) | CC BY-NC 4.0 | actualizado el 23-oct-2026 | 5.598.141.717 filas y 31 columnas; 148 archivos mensuales (septiembre de 2026: 11 GB) | El mapa de nichos: vistas, guardados y compartidos por hashtag, idioma y país, y su evolución mes a mes. No trae los seguidores del creador. Su ficha dice que se recogió con la API móvil de TikTok (firma de peticiones y registro de dispositivos): contra los términos de TikTok. Solo para investigar, sin uso comercial ni redistribución |
| [davidteather/TikTok-Api](https://github.com/davidteather/TikTok-Api) | MIT | 23-ago-2026 | Navegador automatizado (Playwright) con la cookie `ms_token` de una sesión | Su README avisa de que TikTok bloquea al detectar un bot y recomienda proxys residenciales. Frágil y contra los términos: descartado |
| Creative Center de TikTok | — | — | La web de TikTok para anunciantes: hashtags, canciones, creadores y vídeos en tendencia por país y sector | Útil a mano, en el navegador. No se puede automatizar desde aquí: es una aplicación con sesión |
| [Shofo/shofo-tiktok-general-small](https://huggingface.co/datasets/Shofo/shofo-tiktok-general-small) (Hugging Face) | propia: investigación | 19-feb-2026 | 50.000 vídeos con transcripción, comentarios y métricas, en inglés y español (unos 500 GB con los vídeos) | Viejo para tendencias; sirve para estudiar patrones de vídeos virales |

### Instagram Reels

| Proyecto | Licencia | Último commit | Qué da | Para nosotros |
| --- | --- | --- | --- | --- |
| [instaloader/instaloader](https://github.com/instaloader/instaloader) | MIT | 26-oct-2026 (v4.16) | Perfiles, hashtags y reels | Los hashtags y casi todo lo demás piden iniciar sesión; Instagram limita y bloquea las cuentas que descargan mucho. Contra sus términos |
| Graph API de Meta (oficial) | — | — | Con una cuenta profesional y una app de Meta: los medios más populares o recientes de un hashtag, con likes y comentarios; como mucho 30 hashtags distintos cada 7 días | Legal, pero sin vistas. Se puede sumar cuando el canal tenga su cuenta profesional |

### Otros

- [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) (MIT, 28-oct-2026): skill de Claude Code que busca
  qué se ha dicho de un tema en los últimos 30 días y lo ordena por interacción. Reddit, Hacker News y YouTube (con
  yt-dlp) son gratis; TikTok e Instagram van por ScrapeCreators (de pago, con 10.000 llamadas gratis). Sirve para
  documentar un guion, no para medir nichos.
- [sansan0/TrendRadar](https://github.com/sansan0/TrendRadar) (GPL-3.0, 29-oct-2026): monitor de noticias en tendencia con
  filtros por palabra, análisis con IA, avisos y servidor MCP. Sus fuentes son portales chinos (a través de newsnow)
  y RSS: no sirve para cortos en español.
- [trendsmcp-ai/trends-mcp](https://github.com/trendsmcp-ai/trends-mcp) (MIT el adaptador): volumen de hashtags de TikTok
  y de búsquedas de YouTube y Google, pero los datos son de su servicio de pago (100 consultas al mes gratis).
- [TYKAIRO-AI/ViralScout-MCP](https://github.com/TYKAIRO-AI/ViralScout-MCP) (código visible, licencia restrictiva): analiza
  el gancho y el ritmo a partir de una transcripción pegada. Claude lo hace directamente: no aporta.
- [NanmiCoder/MediaCrawler](https://github.com/NanmiCoder/MediaCrawler) (no comercial): plataformas chinas (Xiaohongshu,
  Douyin, Kuaishou, Bilibili, Weibo). Fuera de alcance.
- **Google Trends:** el RSS de tendencias funciona aquí, para la actualidad. La API oficial sigue en alfa desde julio
  de 2025 y se accede por solicitud; pytrends está abandonada.
- **Servicios de pago** (Apify, ScrapeCreators, TikHub, EnsembleData) y **comerciales** (vidIQ, 1of10, Sandcastles,
  Shortimize): los mismos datos con coste, y las búsquedas salen del entorno.
- **Modelos que predicen la viralidad:** en Hugging Face solo hay pruebas pequeñas (clasificadores de popularidad
  entrenados con datos de Snapchat, con decenas de descargas) y retos académicos (VQualA 2025). Nada que mejore a
  medir lo que ya funciona.

## Recomendación: nuestro propio rastreador

**El método** (el de Bangermap y yt-competitor-outlier-pipeline): un vídeo es atípico cuando multiplica la mediana
de su propio canal en el mismo formato. Un 10× en un canal pequeño vale más que un millón de vistas en un canal que
siempre tiene un millón: demuestra que la idea funciona sin una audiencia detrás. Se dan siempre dos números por
separado, el múltiplo y las vistas absolutas, y se compara por días desde la publicación (las vistas son las de hoy).

**Las piezas:**

1. **Mapa de nichos en TikTok** (una vez al mes): consultas con DuckDB al dataset, leyendo solo las columnas
   necesarias y los países de habla hispana. Por hashtag o grupo de hashtags: número de vídeos, vistas medianas y del
   10 % mejor, tasa de guardado (lo útil se guarda), tasa de compartir (lo viral se comparte), crecimiento frente al
   mes anterior, duración típica y cuánto pesa (y rinde) lo marcado como IA. Sale un ranking de nichos y los vídeos
   atípicos de cada uno.
2. **Shorts atípicos de la semana:** con la API de YouTube, los Shorts recientes de cada tema, idioma y país
   (`search.list`, 100 unidades por búsqueda), con sus estadísticas y las de sus canales (1 unidad por cada 50), y el
   múltiplo sobre la mediana de los Shorts del canal (por el RSS, gratis). La cuota gratuita da para unas 90
   búsquedas al día.
3. **Desmontaje de cada atípico elegido:** transcripción con tiempos, cortes por segundo (detección de escenas de
   ffmpeg), texto en pantalla, el gancho de los 3 primeros segundos, duración y estructura (gancho, tensión, giro,
   remate, bucle). Sale una ficha del formato y, de ella, un guion nuestro para el kit. Se copia la mecánica; nunca el
   guion, la voz ni las imágenes de otro.
4. **Informe con fecha:** qué nichos suben, qué formatos se repiten y diez vídeos para estudiar. En el repositorio
   (que es público) van las conclusiones y los enlaces, no los datos en bruto. La política de la API de YouTube no
   deja guardar sus datos más de 30 días sin refrescarlos.

**Hecho el mismo día:** el usuario dio permiso, creó la clave y aceptó el dataset. El rastreador está en
[rastreador/](../rastreador/README.md), con su [primer informe](../rastreador/informes/2026-10-30.md). La clave va como
secreto del entorno en la cabecera `X-Goog-Api-Key` (no como variable `YOUTUBE_API_KEY`), y bajar vídeos de YouTube o
TikTok desde aquí resultó imposible sin esquivar sus bloqueos: el desmontaje trabaja con archivos que sube el usuario.

**Lo que se pidió para la primera prueba:**

- Permiso para instalar `duckdb` (MIT; consulta el parquet a distancia por columnas) y `yt-dlp` (Unlicense; lee
  las pestañas de un canal y baja un vídeo para analizarlo) en un entorno aparte.
- Una clave de la API de datos de YouTube (gratis: Google Cloud → habilitar «YouTube Data API v3» → crear una clave),
  guardada en los ajustes del entorno con el nombre `YOUTUBE_API_KEY`. Nunca en el chat ni en el repositorio.
- Decidir si se usa el dataset de TikTok, sabiendo de dónde salen sus datos.

## Fuentes

- Repositorios (README leídos el 30-oct-2026; fechas de último commit con git): los enlazados en las tablas.
- Dataset de TikTok: [ficha](https://huggingface.co/datasets/datasocial/tiktok-5.6B-videos), tamaño y filas con el
  visor de datasets de Hugging Face (`datasets-server.huggingface.co/size`).
- YouTube: cuotas en los README de viral-shorts, Outlier-Lab y Bangermap; [tutorial de un detector de atípicos con la API](https://dev.to/muhammad_ismail_7be1ea3f9/build-a-youtube-outlier-detector-in-python-with-the-youtube-data-api-v3-3jnk).
- Instagram: [referencia de `top_media`](https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-hashtag/top-media) de la Graph API.
- Google Trends: [anuncio de la API en alfa](https://developers.google.com/search/blog/2025/07/trends-api) (julio de 2025) y
  [el estado de pytrends en 2026](https://dev.to/esteban_ortega/pytrends-is-dead-heres-how-to-get-google-trends-data-in-2026-1a18).
- TikTok Creative Center: [ayuda de TikTok sobre Trends](https://ads.tiktok.com/help/article/how-to-use-trends) y
  [sobre el Creative Center](https://ads.tiktok.com/help/article/creative-center).
- Predicción de engagement: [reto VQualA 2025](https://arxiv.org/abs/2509.02969v1) y [dataset de Snapchat (ECCV 2024)](https://arxiv.org/abs/2410.00289v1).
