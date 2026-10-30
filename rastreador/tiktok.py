"""
Mapa de nichos de TikTok con el dataset público datasocial/tiktok-5.6B-videos (Hugging Face): 5.598 millones de vídeos,
un parquet por mes de publicación, con vistas, likes, comentarios, compartidos, guardados, idioma, país, hashtags y texto
en pantalla. Licencia CC BY-NC 4.0 (solo uso no comercial) y datos recogidos con la API privada de la app, contra los
términos de TikTok: para investigar, sin redistribuirlos. DuckDB lee a distancia solo las columnas que hacen falta.

  PY=~/herramientas-videos/rastreador/bin/python
  $PY rastreador/tiktok.py extraer 2026-08 2026-09           # los vídeos en español de esos meses (unos 4 min por mes)
  $PY rastreador/tiktok.py nichos 2026-09 --antes 2026-08    # ranking de hashtags: aciertos, vistas, guardados, crecimiento
  $PY rastreador/tiktok.py tema 2026-09 negocio dinero emprend finanz --antes 2026-08   # un tema: subnichos y atípicos
  $PY rastreador/tiktok.py atipicos 2026-09 emprendimiento --n 20                       # los vídeos con más vistas del nicho

Cómo se mide (lo orgánico: sin anuncios ni colaboraciones pagadas, y solo vídeos de 7 a 31 días, porque las vistas son
las del día en que se midieron y un vídeo de 2 días aún no ha tenido su recorrido):
  acierto     la parte de los vídeos del nicho que llega a 100.000 vistas
  ×           ese acierto frente al de todo el idioma (2× = el doble de probabilidad de pasar de 100.000)
  guard/mil   guardados por cada mil vistas: lo útil se guarda (lo que buscan los vídeos educativos)
  comp/mil    compartidos por cada mil vistas: lo que se contagia
  cuota       con --antes, cuánto cambia la parte de los vídeos del mes que lleva el hashtag; y su × del mes anterior
              (el rastreo del dataset cambia de un mes a otro: solo valen las medidas relativas)
El dataset no trae quién publica cada vídeo: un nicho pequeño puede estar dominado por un solo creador, y los vídeos
destacados no se pueden medir frente a su canal (eso lo hace rastreador/youtube.py con los Shorts).

Los datos van a salidas/rastreador/tiktok/ (fuera del repositorio).
"""
import argparse
import os
import re
import time

import duckdb

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = os.environ.get('HERRAMIENTAS', os.path.expanduser('~/herramientas-videos'))
DATOS = os.path.join(REPO, 'salidas', 'rastreador', 'tiktok')
URL = 'https://huggingface.co/datasets/datasocial/tiktok-5.6B-videos/resolve/main/data/{}.parquet'
COLUMNAS = ('video_id, posted_at, country, type, duration_ms, hashtags, on_screen_text, views, likes, comments, shares, '
            'saves, is_ai_generated, is_ad, branded_content, not_recommended_for_fyp, stats_updated_at')
EXITO = 100_000
# Hashtags que no dicen de qué va el vídeo: los de alcance («fyp», «parati», «viral»), los de la app y los directos.
GENERICOS = (r'^(fy.*|f[iy]p+|foryou.*|foryourpage.*|fypage|4u|parat[ií]+.*|viral.*|.*viral|trend.*|trending.*|'
             r'tendencia.*|tiktok.*|.*tiktok|capcut.*|video|videos|contenido|creatorsearchinsights|paidpartnership|'
             r'sponsored|publicidad|xyz.*|explore.*|explorar.*|greenscreen|duet|duo|stitch|live|livehighlights|livegift|'
             r'liveincentiveprogram|lives?|parati)$')
# Lugares: dicen dónde, no de qué. Se apartan del ranking de nichos.
LUGARES = set('''mexico usa eeuu estadosunidos venezuela colombia chile ecuador argentina peru guatemala miami espana spain
cdmx honduras bolivia paraguay uruguay panama costarica elsalvador salvador puertorico republicadominicana rd nicaragua
cuba latinos latino latina latinas latinoamerica houston texas california losangeles la nyc newyork madrid barcelona
bogota lima medellin cali guadalajara monterrey culiacan sinaloa jalisco chihuahua sonora tijuana puebla oaxaca
michoacan veracruz guerrero florida chicago arizona phoenix dallas atlanta georgia carolina northcarolina
quito guayaquil caracas santiago buenosaires cordoba rosario sevilla valencia''' .split())


def conexion():
    con = duckdb.connect()
    httpfs = os.path.join(H, 'rastreador', 'httpfs.duckdb_extension')
    con.execute(f"INSTALL '{httpfs}'" if os.path.exists(httpfs) else 'INSTALL httpfs')
    con.execute('LOAD httpfs')
    proxy = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
    if proxy:
        con.execute(f"SET http_proxy='{proxy.split('://')[-1].rstrip('/')}'")
    ca = os.environ.get('SSL_CERT_FILE')
    if ca:
        con.execute(f"SET ca_cert_file='{ca}'")
    con.execute('SET threads=8')
    return con


def archivo(mes, idioma):
    return os.path.join(DATOS, f'{idioma}_{mes}.parquet')


def extraer(meses, idioma):
    os.makedirs(DATOS, exist_ok=True)
    con = conexion()
    for mes in meses:
        destino = archivo(mes, idioma)
        if os.path.exists(destino):
            print(f'{mes}: ya está ({destino})')
            continue
        t = time.time()
        con.execute(f"COPY (SELECT {COLUMNAS} FROM read_parquet('{URL.format(mes)}') WHERE language = '{idioma}') "
                    f"TO '{destino}.tmp' (FORMAT parquet, COMPRESSION zstd)")
        os.rename(destino + '.tmp', destino)
        n = con.execute(f"SELECT count(*) FROM '{destino}'").fetchone()[0]
        print(f'{mes}: {mil(n)} vídeos en «{idioma}» en {time.time() - t:.0f} s → {destino} '
              f'({os.path.getsize(destino) / 1e6:.0f} MB)')


def mil(n):
    return f'{int(round(n)):,}'.replace(',', '.')


def corto(n):
    n = float(n or 0)
    for lim, suf in ((1e6, ' M'), (1e3, ' k')):
        if n >= lim:
            return f'{n / lim:.1f}'.replace('.', ',').replace(',0', '') + suf
    return str(int(n))


def pct(x, dec=1):
    return f'{100 * (x or 0):.{dec}f} %'.replace('.', ',')


def num(x, dec=1):
    return f'{x or 0:.{dec}f}'.replace('.', ',')


def tabla(cab, filas):
    out = ['| ' + ' | '.join(cab) + ' |', '| ' + ' | '.join('---' for _ in cab) + ' |']
    out += ['| ' + ' | '.join(str(c) for c in f) + ' |' for f in filas]
    return '\n'.join(out)


def vistas_sql(con, mes, idioma, nombre):
    """Vista de los vídeos orgánicos de un mes, con un nicho por hashtag (sin tildes ni «#»)."""
    ruta = archivo(mes, idioma)
    if not os.path.exists(ruta):
        raise SystemExit(f'Falta {ruta}: rastreador/tiktok.py extraer {mes}')
    con.execute(f"""CREATE OR REPLACE TEMP VIEW {nombre} AS
        SELECT video_id, views, likes, comments, shares, saves, duration_ms, coalesce(is_ai_generated, 0) AS ia,
               country, on_screen_text,
               list_distinct(list_transform(hashtags, lambda h: strip_accents(ltrim(h, '#')))) AS nichos
        FROM '{ruta}'
        WHERE type = 'video' AND is_ad = 0 AND branded_content = ''
          AND date_diff('day', posted_at, stats_updated_at) BETWEEN 7 AND 31""")
    con.execute(f"""CREATE OR REPLACE TEMP VIEW {nombre}_n AS
        SELECT video_id, views, likes, comments, shares, saves, duration_ms, ia, unnest(nichos) AS nicho
        FROM {nombre}""")


def base(con, v):
    n, med, exito = con.execute(f"SELECT count(*), median(views), avg((views >= {EXITO})::INT) FROM {v}").fetchone()
    return n, med, exito


def metricas_sql(v, filtro=''):
    return f"""SELECT nicho, count(*) AS n, median(views) AS med, quantile_cont(views, 0.9) AS p90,
                      avg((views >= {EXITO})::INT) AS exito,
                      1000.0 * sum(saves) / greatest(sum(views), 1) AS guard,
                      1000.0 * sum(shares) / greatest(sum(views), 1) AS comp,
                      1000.0 * sum(comments) / greatest(sum(views), 1) AS coment,
                      median(duration_ms) / 1000.0 AS dur, avg(ia) AS ia
               FROM {v}_n {filtro} GROUP BY nicho"""


def ranking(con, mes, antes, idioma, minimo, top, lugares):
    vistas_sql(con, mes, idioma, 'm')
    n, med, exito = base(con, 'm')
    print(f'## TikTok en «{idioma}», {mes}: {mil(n)} vídeos orgánicos de 7 a 31 días\n')
    print(f'Mediana de vistas: {mil(med)}. Llegan a 100.000 vistas: {pct(exito)}.\n')
    con.execute(f"CREATE OR REPLACE TEMP TABLE r AS {metricas_sql('m')}")
    if antes:
        vistas_sql(con, antes, idioma, 'a')
        n_a, _, exito_a = base(con, 'a')
        con.execute(f"CREATE OR REPLACE TEMP TABLE ra AS {metricas_sql('a')}")
    excl = f"AND NOT regexp_matches(r.nicho, '{GENERICOS}')"
    if not lugares:
        excl += ' AND r.nicho NOT IN (' + ','.join(f"'{x}'" for x in sorted(LUGARES)) + ')'
    union = 'LEFT JOIN ra ON ra.nicho = r.nicho' if antes else ''
    cols_a = ', ra.n AS n_a, ra.exito AS exito_a' if antes else ', NULL AS n_a, NULL AS exito_a'
    filas = con.execute(f"""SELECT r.*{cols_a} FROM r {union}
        WHERE r.n >= {minimo} AND r.nicho <> '' {excl} ORDER BY r.exito DESC LIMIT {top}""").fetchall()
    cab = ['Nicho', 'Vídeos', 'Mediana', 'Acierto', '×', 'guard/mil', 'comp/mil', 'Duración', 'IA']
    if antes:
        cab += ['Cuota vs. ' + antes, '× en ' + antes]
    out = []
    for f in filas:
        nicho, nn, med_n, p90, ex, guard, comp, coment, dur, ia, nn_a, ex_a = f
        fila = [nicho, mil(nn), corto(med_n), pct(ex), num(ex / exito, 1) + '×', num(guard), num(comp), f'{dur:.0f} s',
                pct(ia, 0)]
        if antes:
            fila += ['—' if not nn_a else f'{100 * ((nn / n) / (nn_a / n_a) - 1):+.0f} %',
                     '—' if ex_a is None else num(ex_a / exito_a) + '×']
        out.append(fila)
    print(f'### Los {top} nichos con más acierto (al menos {minimo} vídeos)\n')
    print(tabla(cab, out))
    if antes:
        # El rastreo del dataset cambia de un mes a otro (cuántos vídeos recoge y cuándo los mide): se comparan la cuota
        # de cada nicho y su acierto relativo al de su mes, no las cifras absolutas.
        filas = con.execute(f"""SELECT r.nicho, r.n, ra.n, r.exito, ra.exito, r.guard FROM r JOIN ra ON ra.nicho = r.nicho
            WHERE r.n >= {minimo} AND ra.n >= {minimo // 2} AND r.nicho <> '' {excl} AND r.exito >= {exito}
            ORDER BY (r.n * 1.0 / {n}) / (ra.n * 1.0 / {n_a}) DESC LIMIT {top}""").fetchall()
        print(f'\n### Los que más ganan cuota frente a {antes} (con acierto por encima de la media)\n')
        print('Cuota: la parte de los vídeos del mes que lleva el hashtag. ×: su acierto frente al del total de su mes.\n')
        print(tabla(['Nicho', 'Vídeos', 'Cuota', '×', '× antes', 'guard/mil'],
                    [[a, mil(b), f'{100 * ((b / n) / (c / n_a) - 1):+.0f} %', num(d / exito) + '×',
                      num(e / exito_a) + '×', num(g)] for a, b, c, d, e, g in filas]))


def patron_tema(palabras):
    return '|'.join(re.escape(p.lower()) for p in palabras)


def filtro_tema(pat, texto):
    f = f"len(list_filter(nichos, lambda x: regexp_matches(x, '{pat}'))) > 0"
    if texto:
        f += f" OR regexp_matches(lower(array_to_string(on_screen_text, ' ')), '{pat}')"
    return f


def tema(con, mes, antes, idioma, palabras, minimo, top, texto):
    vistas_sql(con, mes, idioma, 'm')
    n_tot, med_tot, exito_tot = base(con, 'm')
    pat = patron_tema(palabras)
    con.execute(f'CREATE OR REPLACE TEMP VIEW t AS SELECT * FROM m WHERE {filtro_tema(pat, texto)}')
    con.execute('CREATE OR REPLACE TEMP VIEW t_n AS SELECT video_id, views, likes, comments, shares, saves, duration_ms, ia, '
                'unnest(nichos) AS nicho FROM t')
    n, med, exito = base(con, 't')
    g, c = con.execute('SELECT 1000.0 * sum(saves) / sum(views), 1000.0 * sum(shares) / sum(views) FROM t').fetchone()
    gt, ct = con.execute('SELECT 1000.0 * sum(saves) / sum(views), 1000.0 * sum(shares) / sum(views) FROM m').fetchone()
    print(f'## Tema «{" · ".join(palabras)}», TikTok en «{idioma}», {mes}\n')
    print(tabla(['', 'Vídeos', 'Mediana', 'Acierto (100.000)', 'guard/mil', 'comp/mil'],
                [['El tema', mil(n), mil(med), pct(exito), num(g), num(c)],
                 ['Todo el idioma', mil(n_tot), mil(med_tot), pct(exito_tot), num(gt), num(ct)]]))
    if antes:
        vistas_sql(con, antes, idioma, 'a')
        con.execute(f'CREATE OR REPLACE TEMP VIEW ta AS SELECT * FROM a WHERE {filtro_tema(pat, texto)}')
        na, meda, exa = base(con, 'ta')
        n_tot_a, _, exito_tot_a = base(con, 'a')
        print(f'\nFrente a {antes}: cuota del tema {100 * ((n / n_tot) / (na / n_tot_a) - 1):+.0f} %; acierto relativo '
              f'{num(exito / exito_tot)}× (antes, {num(exa / exito_tot_a)}×). El rastreo del dataset cambia cada mes: '
              'solo valen las medidas relativas.')
    filas = con.execute(f"""{metricas_sql('t')} HAVING count(*) >= {minimo}
        AND NOT regexp_matches(nicho, '{GENERICOS}') AND nicho <> '' ORDER BY exito DESC LIMIT {top}""").fetchall()
    filas = [f for f in filas if f[0] not in LUGARES]
    print(f'\n### Subnichos del tema con más acierto (al menos {minimo} vídeos)\n')
    print(tabla(['Subnicho', 'Vídeos', 'Mediana', 'Acierto', '×', 'guard/mil', 'comp/mil', 'Duración'],
                [[f[0], mil(f[1]), corto(f[2]), pct(f[4]), num(f[4] / exito_tot) + '×', num(f[5]), num(f[6]),
                  f'{f[8]:.0f} s'] for f in filas]))
    atipicos_de(con, 't', top, f'Los {top} vídeos del tema con más vistas')


def atipicos_de(con, v, top, titulo):
    filas = con.execute(f"""SELECT video_id, views, saves, shares, duration_ms / 1000, country, nichos, on_screen_text
        FROM {v} ORDER BY views DESC LIMIT {top}""").fetchall()
    print(f'\n### {titulo}\n')
    out = []
    for vid, views, saves, shares, dur, pais, nichos, texto in filas:
        nichos = [x for x in nichos if not re.match(GENERICOS, x)][:5]
        txt = ' / '.join(t.replace('\n', ' ').replace('|', '/') for t in (texto or [])[:2])[:90]
        out.append([corto(views), num(1000 * saves / max(views, 1)),
                    num(1000 * shares / max(views, 1)), f'{dur:.0f} s', pais, ' '.join('#' + x for x in nichos),
                    txt or '—', f'[ver](https://www.tiktok.com/@_/video/{vid})'])
    print(tabla(['Vistas', 'guard/mil', 'comp/mil', 'Duración', 'País', 'Hashtags', 'Texto en pantalla', ''],
                out))


def atipicos(con, mes, idioma, nicho, top):
    vistas_sql(con, mes, idioma, 'm')
    nicho = nicho.lower().lstrip('#')
    con.execute(f"CREATE OR REPLACE TEMP VIEW t AS SELECT * FROM m WHERE list_contains(nichos, strip_accents('{nicho}'))")
    n, med, exito = base(con, 't')
    print(f'## #{nicho}, TikTok en «{idioma}», {mes}: {mil(n)} vídeos, mediana {mil(med)}, acierto {pct(exito)}')
    atipicos_de(con, 't', top, f'Los {top} con más vistas del nicho')


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--idioma', default='es')
    sub = p.add_subparsers(dest='orden', required=True)
    e = sub.add_parser('extraer')
    e.add_argument('meses', nargs='+')
    r = sub.add_parser('nichos')
    r.add_argument('mes')
    r.add_argument('--antes')
    r.add_argument('--minimo', type=int, default=500)
    r.add_argument('--n', type=int, default=40)
    r.add_argument('--lugares', action='store_true', help='incluir hashtags de países y ciudades')
    t = sub.add_parser('tema')
    t.add_argument('mes')
    t.add_argument('palabras', nargs='+', help='raíces: «emprend» encuentra emprendimiento, emprendedor…')
    t.add_argument('--antes')
    t.add_argument('--minimo', type=int, default=60)
    t.add_argument('--n', type=int, default=25)
    t.add_argument('--texto', action='store_true', help='buscar las palabras también en el texto en pantalla')
    a = sub.add_parser('atipicos')
    a.add_argument('mes')
    a.add_argument('nicho')
    a.add_argument('--n', type=int, default=20)
    args = p.parse_args()
    if args.orden == 'extraer':
        extraer(args.meses, args.idioma)
        return
    con = duckdb.connect()
    con.execute('SET threads=4')
    if args.orden == 'nichos':
        ranking(con, args.mes, args.antes, args.idioma, args.minimo, args.n, args.lugares)
    elif args.orden == 'tema':
        tema(con, args.mes, args.antes, args.idioma, args.palabras, args.minimo, args.n, args.texto)
    else:
        atipicos(con, args.mes, args.idioma, args.nicho, args.n)


if __name__ == '__main__':
    main()
