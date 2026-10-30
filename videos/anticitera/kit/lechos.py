"""Lecho de música de cada capítulo a su duración: la pieza N (MusicGen, en el orden de guion.json) extendida con
audio/lecho.py. Lo llama preparar.sh tras generar las piezas.
  python3 videos/anticitera/kit/lechos.py [cap1 ...]"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import montar  # noqa: E402

ids = [c['id'] for c in json.load(open(os.path.join(montar.RAIZ, 'recursos', 'guion.json')))['capitulos']]
M = os.path.join(montar.TRABAJO, 'musica')
for i, cid in enumerate(ids):
    if len(sys.argv) > 1 and cid not in sys.argv[1:]:
        continue
    dur = montar.cargar(cid).dur
    subprocess.run([sys.executable, os.path.join(montar.REPO, 'audio', 'lecho.py'), os.path.join(M, f'pieza_{i + 1}.wav'),
                    str(dur + 0.5), '-o', os.path.join(M, cid + '.wav')], check=True)
