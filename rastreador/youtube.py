"""
Shorts atípicos de YouTube: los que multiplican las vistas normales de su propio canal. Un 10× en un canal pequeño vale
más que un millón de vistas en un canal que siempre tiene un millón: demuestra que la idea funciona sin una audiencia
detrás (el método de Bangermap y yt-competitor-outlier-pipeline, ver docs/investigacion-rastreador.md).

  python3 rastreador/youtube.py buscar "ideas de negocio" --dias 14 --region MX --min-vistas 10000
  python3 rastreador/youtube.py nicho "ideas de negocio" "finanzas personales" "historia de empresas" --dias 30
  python3 rastreador/youtube.py canal @canal                      # los Shorts recientes de un canal, con su múltiplo

Datos: la API de datos de YouTube (la clave la pone el proxy del entorno en la cabecera X-Goog-Api-Key; o la variable
YOUTUBE_API_KEY) y el RSS de cada canal (sus 15 últimos vídeos con las vistas; gratis y sin cuota).
Cuota: cada búsqueda cuesta unas 102 unidades de las 10.000 diarias (search.list 100; vídeos y canales, 1 por cada 50).
Lo que se guarda (salidas/rastreador/youtube/, fuera del repositorio) se borra o se refresca antes de 30 días: lo pide
la política de la API.

Solo cuenta los vídeos que declaran ese idioma (defaultAudioLanguage o defaultLanguage).

Columnas:
  ×canal   vistas del Short / mediana de los otros Shorts recientes del canal (por RSS); «—» si tiene menos de 3
  v/h      vistas por hora desde que se publicó
  v/sub    vistas / suscriptores del canal
"""
import argparse
import concurrent.futures as cf
import datetime as dt
import json
import os
import re
import statistics
import sys
import urllib.parse
import urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(REPO, 'salidas', 'rastreador', 'youtube')
API = 'https://www.googleapis.com/youtube/v3/'
CORTO = 180  # un Short dura hasta 3 minutos
ATIPICO = 3.0


def api(recurso, **p):
    clave = os.environ.get('YOUTUBE_API_KEY')
    if clave:
        p['key'] = clave
    url = API + recurso + '?' + urllib.parse.urlencode(p)
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        cuerpo = e.read().decode(errors='replace')
        sys.exit(f'API de YouTube, {recurso}: {e.code} {cuerpo[:300]}')


def segundos(iso):
    m = re.fullmatch(r'P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', iso or '')
    if not m:
        return 0
    d, h, mi, s = (int(x or 0) for x in m.groups())
    return d * 86400 + h * 3600 + mi * 60 + s


def fecha(s):
    return dt.datetime.fromisoformat(s.replace('Z', '+00:00'))


def rss(canal):
    """Los 15 últimos vídeos del canal: {id: (vistas, es_short, publicado)}."""
    try:
        with urllib.request.urlopen(f'https://www.youtube.com/feeds/videos.xml?channel_id={canal}', timeout=20) as r:
            x = r.read().decode('utf-8', 'replace')
    except Exception:
        return {}
    out = {}
    for e in re.findall(r'<entry>(.*?)</entry>', x, re.S):
        vid = re.search(r'<yt:videoId>(.*?)</yt:videoId>', e)
        vistas = re.search(r'views="(\d+)"', e)
        enlace = re.search(r'<link rel="alternate" href="(.*?)"', e)
        pub = re.search(r'<published>(.*?)</published>', e)
        if vid and vistas:
            out[vid.group(1)] = (int(vistas.group(1)), bool(enlace and '/shorts/' in enlace.group(1)),
                                 pub.group(1) if pub else '')
    return out


def detalles(ids):
    vids = {}
    for i in range(0, len(ids), 50):
        r = api('videos', part='snippet,statistics,contentDetails', id=','.join(ids[i:i + 50]), maxResults=50)
        for v in r.get('items', []):
            vids[v['id']] = v
    return vids


def canales(ids):
    out = {}
    ids = sorted(set(ids))
    for i in range(0, len(ids), 50):
        r = api('channels', part='snippet,statistics', id=','.join(ids[i:i + 50]), maxResults=50)
        for c in r.get('items', []):
            out[c['id']] = c
    return out


def puntuar(vids, chans, feeds, ahora):
    filas = []
    for vid, v in vids.items():
        dur = segundos(v['contentDetails'].get('duration'))
        if not dur or dur > CORTO:
            continue
        st, sn = v.get('statistics', {}), v['snippet']
        vistas = int(st.get('viewCount', 0))
        horas = max((ahora - fecha(sn['publishedAt'])).total_seconds() / 3600, 1)
        c = chans.get(sn['channelId'], {})
        subs = int(c.get('statistics', {}).get('subscriberCount', 0) or 0)
        feed = feeds.get(sn['channelId'], {})
        otros = [n for k, (n, es_short, _) in feed.items() if es_short and k != vid]
        mult = vistas / statistics.median(otros) if len(otros) >= 3 and statistics.median(otros) > 0 else None
        filas.append(dict(id=vid, titulo=sn['title'], canal=sn['channelTitle'], canal_id=sn['channelId'],
                          publicado=sn['publishedAt'], dur=dur, vistas=vistas, likes=int(st.get('likeCount', 0) or 0),
                          comentarios=int(st.get('commentCount', 0) or 0), vh=vistas / horas, subs=subs,
                          vsub=vistas / subs if subs else None, mult=mult, n_otros=len(otros),
                          canal_desde=c.get('snippet', {}).get('publishedAt', ''),
                          es_short=feed.get(vid, (0, None))[1]))
    return filas


def del_idioma(v, idioma):
    sn = v['snippet']
    return (sn.get('defaultAudioLanguage') or sn.get('defaultLanguage') or '').lower().startswith(idioma)


def buscar_shorts(consulta, dias, region, idioma, paginas):
    ahora = dt.datetime.now(dt.timezone.utc)
    desde = (ahora - dt.timedelta(days=dias)).strftime('%Y-%m-%dT%H:%M:%SZ')
    ids, token = [], None
    for _ in range(paginas):
        # Con order=viewCount la API no hace caso de relevanceLanguage: devuelve lo más visto del mundo (para «ideas de
        # negocio», 0 de 50 en español). Con order=relevance, 34–44 de 50 lo están; el orden lo ponen después las métricas.
        p = dict(part='id', q=consulta, type='video', videoDuration='short', order='relevance', publishedAfter=desde,
                 relevanceLanguage=idioma, maxResults=50)
        if region:
            p['regionCode'] = region
        if token:
            p['pageToken'] = token
        r = api('search', **p)
        ids += [x['id']['videoId'] for x in r.get('items', [])]
        token = r.get('nextPageToken')
        if not token:
            break
    vids = {k: v for k, v in detalles(ids).items() if del_idioma(v, idioma)}
    chans = canales([v['snippet']['channelId'] for v in vids.values()])
    with cf.ThreadPoolExecutor(8) as ex:
        feeds = dict(zip(chans, ex.map(rss, chans)))
    return puntuar(vids, chans, feeds, ahora)


def guardar(nombre, datos):
    os.makedirs(DATOS, exist_ok=True)
    slug = re.sub(r'[^a-z0-9]+', '-', nombre.lower()).strip('-')[:60]
    ruta = os.path.join(DATOS, f'{dt.date.today()}_{slug}.json')
    json.dump(datos, open(ruta, 'w'), ensure_ascii=False, indent=1)
    return ruta


def corto(n):
    n = float(n or 0)
    for lim, suf in ((1e6, ' M'), (1e3, ' k')):
        if n >= lim:
            return f'{n / lim:.1f}'.replace('.', ',').replace(',0', '') + suf
    return str(int(n))


def tabla(cab, filas):
    out = ['| ' + ' | '.join(cab) + ' |', '| ' + ' | '.join('---' for _ in cab) + ' |']
    out += ['| ' + ' | '.join(str(c) for c in f) + ' |' for f in filas]
    return '\n'.join(out)


def imprimir(filas, top, orden='mult', minimo=0):
    clave = {'mult': lambda f: (f['mult'] or 0, f['vh']), 'vh': lambda f: f['vh']}[orden]
    filas = sorted([f for f in filas if f['vistas'] >= minimo], key=clave, reverse=True)[:top]
    print(tabla(['×canal', 'Vistas', 'v/h', 'v/sub', 'Suscriptores', 'Días', 'Dur.', 'Canal', 'Título', ''],
                [[f"{f['mult']:.1f}×".replace('.', ',') if f['mult'] else '—', corto(f['vistas']), corto(f['vh']),
                  f"{f['vsub']:.1f}".replace('.', ',') if f['vsub'] else '—', corto(f['subs']),
                  (dt.datetime.now(dt.timezone.utc) - fecha(f['publicado'])).days, f"{f['dur']} s",
                  f['canal'].replace('|', '/')[:28], f['titulo'].replace('|', '/')[:70],
                  f"[ver](https://www.youtube.com/shorts/{f['id']})"] for f in filas]))


def resumen(consulta, filas, minimo):
    vistas = [f['vistas'] for f in filas]
    mults = [f['mult'] for f in filas if f['mult'] and f['vistas'] >= minimo]
    return dict(consulta=consulta, shorts=len(filas), mediana=statistics.median(vistas) if vistas else 0,
                vh=statistics.median([f['vh'] for f in filas]) if filas else 0,
                atipicos=sum(m >= ATIPICO for m in mults), medidos=len(mults),
                pequenos=sum(1 for f in filas if f['mult'] and f['mult'] >= ATIPICO and f['subs'] < 100_000
                             and f['vistas'] >= minimo))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='orden', required=True)
    for nombre in ('buscar', 'nicho'):
        b = sub.add_parser(nombre)
        b.add_argument('consultas', nargs='+')
        b.add_argument('--dias', type=int, default=14, help='publicados en los últimos N días')
        b.add_argument('--region', default='', help='código de país: MX, ES, CO, AR, US…')
        b.add_argument('--idioma', default='es')
        b.add_argument('--paginas', type=int, default=2, help='cada página son 50 resultados y 100 unidades')
        b.add_argument('--min-vistas', type=int, default=10_000, help='un atípico con menos vistas no cuenta')
        b.add_argument('--n', type=int, default=20)
        b.add_argument('--orden', dest='por', choices=('mult', 'vh'), default='mult')
    c = sub.add_parser('canal')
    c.add_argument('canal', help='@handle o id UC…')
    a = p.parse_args()

    if a.orden == 'canal':
        ident = a.canal
        if ident.startswith('@'):
            r = api('channels', part='id', forHandle=ident)
            if not r.get('items'):
                sys.exit(f'No encuentro {ident}')
            ident = r['items'][0]['id']
        feed = rss(ident)
        ahora = dt.datetime.now(dt.timezone.utc)
        vids = detalles(list(feed))
        filas = puntuar(vids, canales([ident]), {ident: feed}, ahora)
        print(f'## {a.canal}: {sum(1 for f in filas if f["es_short"])} Shorts entre sus 15 últimos vídeos\n')
        imprimir([f for f in filas if f['es_short']], 15)
        return

    resumenes = []
    for q in a.consultas:
        filas = buscar_shorts(q, a.dias, a.region, a.idioma, a.paginas)
        ruta = guardar(f'{q}-{a.region or "todo"}-{a.dias}d', filas)
        resumenes.append(resumen(q, filas, a.min_vistas))
        if a.orden == 'buscar':
            r = resumenes[-1]
            print(f'## «{q}»: {r["shorts"]} Shorts de los últimos {a.dias} días{" en " + a.region if a.region else ""}; '
                  f'{r["atipicos"]} de los {r["medidos"]} con más de {a.min_vistas} vistas pasan de {ATIPICO:.0f}× su canal\n')
            imprimir(filas, a.n, a.por, a.min_vistas)
            print(f'\n({ruta})\n')
    if a.orden == 'nicho':
        print(f'## Nichos en Shorts, últimos {a.dias} días{" en " + a.region if a.region else ""}\n')
        resumenes.sort(key=lambda r: (r['atipicos'], r['mediana']), reverse=True)
        print(f'Atípicos: Shorts con más de {a.min_vistas} vistas que pasan de {ATIPICO:.0f}× la mediana de su canal.\n')
        print(tabla(['Consulta', 'Shorts', 'Mediana de vistas', 'v/h (mediana)', f'Con más de {corto(a.min_vistas)}',
                     f'Atípicos (≥{ATIPICO:.0f}×)', 'De canales < 100 k'],
                    [[r['consulta'], r['shorts'], corto(r['mediana']), corto(r['vh']), r['medidos'], r['atipicos'],
                      r['pequenos']] for r in resumenes]))


if __name__ == '__main__':
    main()
