"""
Cuánto suena cada efecto de un proyecto de HyperFrames frente a la voz, sin renderizar: rehace las pistas (voz, música
y efectos) desde el index.html del proyecto, con sus volúmenes, recortes y fundidos, y mide su sonoridad momentánea
(EBU R128, ventanas de 400 ms) con ffmpeg.

  python3 audio/revisar_mezcla.py canales/supervivencia/cortos/01-juliane/proyecto [--margen 8] [--wav carpeta]

Por cada efecto: su pico momentáneo, la voz en ese momento y la diferencia (LU). Un efecto que suena mientras se habla
debería quedar al menos --margen LU por debajo de la voz; en una pausa, no pasar de 3 LU bajo el nivel medio de la
voz. Al final, la música frente a la voz por tramos y los efectos por minuto.
"""
import argparse
import html
import json
import os
import re
import subprocess
import sys
import wave

import numpy as np

SR = 48000


def leer(ruta):
    """Un archivo de audio cualquiera, en mono y a 48 kHz (float32)."""
    datos = subprocess.run(['ffmpeg', '-v', 'error', '-i', ruta, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                           capture_output=True, check=True).stdout
    return np.frombuffer(datos, np.float32).astype(np.float64)


def pistas(proyecto):
    s = open(os.path.join(proyecto, 'index.html')).read()
    out = []
    for m in re.finditer(r'<audio ([^>]*)>', s):
        at = {k: html.unescape(v) for k, v in re.findall(r'([\w-]+)="([^"]*)"', m.group(1))}
        out.append(dict(id=at['id'], src=os.path.join(proyecto, at['src']), t=float(at['data-start']),
                        dur=float(at['data-duration']), vol=float(at.get('data-volume', 1)),
                        ini=float(at.get('data-media-start', 0)), fi=float(at.get('data-fade-in', 0)),
                        fo=float(at.get('data-fade-out', 0)),
                        auto=json.loads(at['data-automation']) if 'data-automation' in at else None))
    return out


def colocar(p, total, cache):
    if p['src'] not in cache:
        cache[p['src']] = leer(p['src'])
    x = cache[p['src']]
    a = int(round(p['ini'] * SR))
    n = min(int(round(p['dur'] * SR)), max(0, len(x) - a))
    y = x[a:a + n].copy()
    tt = np.arange(n) / SR
    g = np.full(n, p['vol'])
    if p['auto']:
        pts = sorted((q['t'], q['v']) for q in p['auto']['lanes'][0]['points'])
        g = np.interp(tt, [q[0] for q in pts], [q[1] for q in pts])
    if p['fi'] > 0:
        g *= np.clip(tt / p['fi'], 0, 1)
    if p['fo'] > 0:
        g *= np.clip((p['dur'] - tt) / p['fo'], 0, 1)
    pista = np.zeros(total)
    i = int(round(p['t'] * SR))
    m = max(0, min(n, total - i))
    pista[i:i + m] = (y * g)[:m]
    return pista


def guardar(ruta, x):
    with wave.open(ruta, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype('<i2').tobytes())


def momentanea(x, tmp):
    """Sonoridad momentánea (LUFS, cada 100 ms) e integrada de una pista, con el ebur128 de ffmpeg."""
    guardar(tmp, x)
    r = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-v', 'verbose', '-i', tmp, '-af', 'ebur128=metadata=1', '-f', 'null', '-'],
                       capture_output=True, text=True).stderr
    m = np.array([float(v) for v in re.findall(r'\bM:\s*(-?[\d.]+|-inf)', r.replace('-inf', '-120'))])
    i = re.findall(r'I:\s+(-?[\d.]+) LUFS', r)
    return m, (float(i[-1]) if i else -70.0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('proyecto')
    ap.add_argument('--margen', type=float, default=8.0, help='LU que un efecto debe quedar bajo la voz mientras se habla')
    ap.add_argument('--pausa', type=float, default=3.0, help='LU bajo el nivel medio de la voz para un efecto en una pausa')
    ap.add_argument('--habla', type=float, default=6.0,
                    help='una ventana es voz si suena a menos de estos LU de su nivel medio (las colas de las palabras, no)')
    ap.add_argument('--wav', help='carpeta donde guardar las tres pistas (voz, música y efectos)')
    a = ap.parse_args()
    ps = pistas(a.proyecto)
    total = int((max(p['t'] + p['dur'] for p in ps) + 0.5) * SR)
    cache = {}
    voz = sum(colocar(p, total, cache) for p in ps if p['id'] == 'voz')
    musica = sum((colocar(p, total, cache) for p in ps if p['id'].startswith('musica')), np.zeros(total))
    efectos = [(p, colocar(p, total, cache)) for p in ps if p['id'].startswith('sfx')]
    sfx = sum((e for _, e in efectos), np.zeros(total))
    tmp = os.path.join(os.environ.get('TMPDIR', '/tmp'), f'revisar_mezcla_{os.getpid()}.wav')
    mv, iv = momentanea(voz, tmp)
    mm, im = momentanea(musica, tmp)
    ms, isfx = momentanea(sfx, tmp)
    print(f'Integrada: voz {iv:.1f} LUFS · música {im:.1f} ({im - iv:+.1f} LU) · efectos {isfx:.1f} ({isfx - iv:+.1f} LU)')
    habla = mv > iv - a.habla                  # se está hablando (M[k]: los 400 ms que acaban en (k + 1) / 10 s)
    print(f'Efectos: {len(efectos)} en {total / SR:.1f} s ({60 * len(efectos) / (total / SR):.0f} por minuto)\n')
    print('  t (s)  efecto                  vol    peor momento: efecto  voz    dif   límite   vol que cabe')
    malos = 0
    for p, e in efectos:
        # Solo el tramo del efecto (más 0,4 s antes y después), empezando en una décima exacta para casar las ventanas.
        k0 = max(0, int(p['t'] * 10) - 4)
        k1 = min(len(mv), int((p['t'] + p['dur']) * 10) + 5)
        me, _ = momentanea(e[k0 * SR // 10:k1 * SR // 10], tmp)
        peor = None
        for j, m in enumerate(me):
            k = k0 + j
            if k >= len(mv) or m < -70:
                continue
            d, lim = (m - mv[k], -a.margen) if habla[k] else (m - iv, -a.pausa)
            if peor is None or d - lim > peor[0]:
                peor = (d - lim, k, m, d, lim)
        if peor is None:
            continue
        exceso, k, m, d, lim = peor
        nota = ''
        if exceso > 0:
            malos += 1
            nota = f'  ← ALTO: {p["vol"]:.2f} → {p["vol"] * 10 ** (-exceso / 20):.2f}'
        elif d < -22:
            nota = '  (casi no se oye)'
        nombre = os.path.basename(p['src'])
        donde = 'con voz' if lim == -a.margen else 'en pausa'
        print(f'  {p["t"]:5.1f}  {nombre[:22]:22s}  {p["vol"]:.2f}   {k / 10:5.1f} s {m:6.1f}  {mv[k]:6.1f}  {d:+5.1f}  {lim:+4.0f} {donde}{nota}')
    print(f'\n{malos} de {len(efectos)} efectos por encima de lo permitido (con voz, {a.margen:.0f} LU bajo ella; en pausa, '
          f'{a.pausa:.0f} LU bajo su nivel medio).')
    # La música frente a la voz, por tramos de 5 s en los que se habla.
    print('\nMúsica frente a la voz (mediana por tramos de 5 s con voz, LU):')
    n = min(len(mv), len(mm))
    fila = []
    for i in range(0, n, 50):
        h = habla[i:min(i + 50, n)]
        if h.sum() > 10:
            fila.append(f'{i / 10:.0f}s {np.median(mm[i:i + len(h)][h] - mv[i:i + len(h)][h]):+.0f}')
    print('  ' + ' · '.join(fila))
    if a.wav:
        os.makedirs(a.wav, exist_ok=True)
        for n, x in (('voz', voz), ('musica', musica), ('efectos', sfx)):
            guardar(os.path.join(a.wav, n + '.wav'), x)
    os.remove(tmp)


if __name__ == '__main__':
    sys.exit(main())
