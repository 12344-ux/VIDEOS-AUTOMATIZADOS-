"""Resumen del check de HyperFrames de un proyecto (videos/anticitera/<parte>):
  python3 videos/anticitera/kit/revisar.py cap1 [cap2 ...]
Errores y avisos en una línea cada uno. Los «dead_stretch» se cuentan aparte: check no ve el movimiento de la
cámara ni de los dibujos (WebGL y hf-seek), así que en estas composiciones son falsos (ver la apertura)."""
import json
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HF = os.path.join(AQUI, '..', '..', 'video', 'hf.sh')
for parte in sys.argv[1:]:
    r = subprocess.run([HF, 'check', '--json'], cwd=os.path.join(AQUI, parte), capture_output=True, text=True)
    try:
        d = json.loads(r.stdout[r.stdout.index('{'):])
    except ValueError:
        print(parte, 'check falló:', (r.stderr or r.stdout)[-500:])
        continue
    muertos, lineas = 0, []
    for seccion in ('lint', 'runtime', 'layout', 'motion', 'contrast', 'craft', 'audio'):
        for f in (d.get(seccion) or {}).get('findings', []):
            if f.get('code') == 'dead_stretch':
                muertos += 1
                continue
            t = f.get('time')
            lineas.append(f"  {f.get('severity', '?')[:4]} {f.get('code')} {'' if t is None else f't={t:.1f} '}{(f.get('message') or '')[:150]}")
    print(f"{parte}: ok={d.get('ok')} · {len(lineas)} avisos · {muertos} dead_stretch (falsos)")
    print('\n'.join(lineas[:25]))
