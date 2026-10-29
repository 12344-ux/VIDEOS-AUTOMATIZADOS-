"""
Efectos de sonido reales (grabados, no sintetizados) de BigSoundBank, una fonoteca con
licencia CC0 (dominio público): se pueden usar en cualquier proyecto, también comercial,
sin atribución. El script comprueba la licencia en la página de cada sonido antes de bajarlo.

Freesound y Pixabay están bloqueados por la red del entorno, y la API de Openverse no
responde; BigSoundBank sí llega.

  python3 audio/efectos.py buscar "match" "adhesive tape"        # busca (en inglés)
  python3 audio/efectos.py bajar 0004 0298 -d salidas/sfx        # baja WAV 48 kHz estéreo
  python3 audio/efectos.py bajar 0004 --recorte 1.2:2.0 -o cerilla.wav

--recorte INICIO:FIN se queda con ese tramo (en segundos) y lo funde 5 ms en los bordes.
Cada descarga se apunta en CREDITOS.md, en la carpeta de destino.
"""
import argparse
import html
import os
import re
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request

WEB = 'https://bigsoundbank.com'
AGENTE = 'Mozilla/5.0 (X11; Linux x86_64) VideosAutomatizados/0.1'


def pedir(url, binario=False):
    req = urllib.request.Request(url, headers={'User-Agent': AGENTE})
    with urllib.request.urlopen(req, timeout=60) as r:
        datos = r.read()
    return datos if binario else datos.decode('utf-8', 'ignore')


def buscar(consulta):
    pagina = pedir(f'{WEB}/search?q={urllib.parse.quote(consulta)}')
    return [(num, html.unescape(titulo).strip(), f'{WEB}/{ruta}-s{num}.html')
            for ruta, num, titulo in re.findall(r"<h2[^>]*><a href='/([^']+)-s(\d+)\.html'>([^<]+)<span", pagina)]


def ficha(num):
    """Título, duración y licencia leídos de la página del sonido."""
    url = f'{WEB}/s{num}.html'  # la web acepta la página sin el nombre del sonido
    pagina = pedir(url)
    texto = html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', pagina)))
    titulo = re.search(r'<h1[^>]*>(.*?)</h1>', pagina, re.S)
    licencia = re.search(r'License\s+(.{0,60}?):', texto)
    return {
        'num': num, 'url': url,
        'titulo': html.unescape(re.sub(r'<[^>]+>', '', titulo.group(1))).strip() if titulo else num,
        'licencia': licencia.group(1).strip() if licencia else '?',
    }


def bajar(num, salida, recorte=None):
    datos = ficha(num)
    if 'CC0' not in datos['licencia']:
        sys.exit(f"{num}: la licencia es «{datos['licencia']}», no CC0. No lo bajo.")
    with tempfile.TemporaryDirectory() as tmp:
        origen = os.path.join(tmp, f'{num}.aiff')
        with open(origen, 'wb') as f:
            f.write(pedir(f'{WEB}/UPLOAD/aiff/{num}.aiff', binario=True))
        filtros = []
        if recorte:
            a, b = (float(v) for v in recorte.split(':'))
            filtros = [f'atrim={a}:{b}', 'asetpts=PTS-STARTPTS', 'afade=t=in:d=0.005',
                       f'afade=t=out:st={max(b - a - 0.005, 0)}:d=0.005']
        orden = ['ffmpeg', '-v', 'error', '-y', '-i', origen, '-ar', '48000', '-ac', '2']
        if filtros:
            orden += ['-af', ','.join(filtros)]
        subprocess.run(orden + [salida], check=True)
    creditos = os.path.join(os.path.dirname(os.path.abspath(salida)), 'CREDITOS.md')
    linea = f"- `{os.path.basename(salida)}`: «{datos['titulo']}» (#{num}), BigSoundBank, {datos['licencia']}. {datos['url']}\n"
    previas = open(creditos, encoding='utf-8').read() if os.path.exists(creditos) else \
        '# Créditos de sonido\n\nSonidos de BigSoundBank con licencia CC0: no exigen atribución.\n\n'
    if linea not in previas:
        with open(creditos, 'w', encoding='utf-8') as f:
            f.write(previas + linea)
    print(f"{salida}  «{datos['titulo']}» ({datos['licencia']})")


def main():
    p = argparse.ArgumentParser(description='Efectos de sonido CC0 de BigSoundBank.')
    sub = p.add_subparsers(dest='orden', required=True)
    b = sub.add_parser('buscar')
    b.add_argument('consultas', nargs='+')
    d = sub.add_parser('bajar')
    d.add_argument('numeros', nargs='+')
    d.add_argument('-d', '--carpeta', default='.')
    d.add_argument('-o', '--salida', help='nombre del archivo (con un solo número)')
    d.add_argument('--recorte', help='INICIO:FIN en segundos')
    args = p.parse_args()

    if args.orden == 'buscar':
        for consulta in args.consultas:
            resultados = buscar(consulta)
            print(f'== {consulta}: {len(resultados)}')
            for num, titulo, _ in resultados[:15]:
                print(f'   {num}  {titulo}')
    else:
        os.makedirs(args.carpeta, exist_ok=True)
        for num in args.numeros:
            salida = args.salida if args.salida and len(args.numeros) == 1 else os.path.join(args.carpeta, f'{num}.wav')
            bajar(num, salida, args.recorte)


if __name__ == '__main__':
    main()
