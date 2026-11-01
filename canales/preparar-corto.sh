#!/usr/bin/env bash
# Recursos de un corto de los canales nuevos (geografía, supervivencia…), en salidas/<canal>/<corto>/: lo que ya exista
# no se repite. La voz, las fuentes y las músicas salen de canales/<canal>/marca/canal.json y de los recursos/ del corto.
#   canales/preparar-corto.sh geografia cortos/01-chile                 todo
#   canales/preparar-corto.sh supervivencia cortos/01-juliane voz musica  solo esas etapas (marca, voz, musica, imagenes)
# Orden pensado para la RAM: la voz y la música antes que FLUX (no caben a la vez con el servidor de imágenes).
# PARAR=0 deja el servidor de imágenes encendido al acabar (para encadenar otro corto sin volver a cargar FLUX).
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
CANAL="$1"; CORTO="$2"; shift 2
ETAPAS="${*:-marca voz musica imagenes}"
AQUI="$REPO/canales/$CANAL/$CORTO"
CONF="$REPO/canales/$CANAL/marca/canal.json"
H="${HERRAMIENTAS:-$HOME/herramientas-videos}"
S="$REPO/salidas/$CANAL"
T="$S/$CORTO"
PYP="$H/piper/bin/python"
PYF="$H/fastsdcpu/env/bin/python"
mkdir -p "$S/marca"/{img,fuentes} "$T"/{voz,musica,img}
paso() { printf '\n== %s: %s (%s)\n' "$CANAL/$CORTO" "$*" "$(date +%H:%M:%S)"; }
etapa() { [[ " $ETAPAS " == *" $1 "* ]]; }

if etapa marca; then
  paso "Marca: fuentes (OFL, de @fontsource) y texturas"
  python3 -c "import json; [print(k, v) for k, v in json.load(open('$CONF'))['fuentes'].items()]" |
    while read -r nombre ruta; do
      [ -s "$S/marca/fuentes/$nombre" ] || curl -fsSL --retry 3 -o "$S/marca/fuentes/$nombre" "https://cdn.jsdelivr.net/npm/$ruta"
    done
  # Las mismas texturas que BusinessForMen (grano y desgaste), con la misma semilla.
  [ -s "$S/marca/img/desgaste.png" ] || python3 - "$S/marca/img" <<'PY'
import sys
import numpy as np
from PIL import Image, ImageFilter
M, rng = sys.argv[1], np.random.default_rng(5)
g = np.clip(128 + rng.normal(0, 46, (512, 512)), 0, 255).astype(np.uint8)
Image.fromarray(g, 'L').save(f'{M}/grano.png')
a = np.array(Image.fromarray((rng.random((360, 360)) * 255).astype(np.uint8), 'L').filter(ImageFilter.GaussianBlur(1.6))).astype(np.float32)
a = (a - a.mean()) / a.std()
alfa = np.where(a > 1.25, 0, np.where(a > 0.9, 110, 255)).astype(np.uint8)
Image.fromarray(np.dstack([np.full_like(alfa, 255)] * 3 + [alfa]), 'RGBA').save(f'{M}/desgaste.png')
PY
fi

if etapa voz; then
  VOZ=$(python3 -c "import json; print(json.load(open('$CONF'))['voz'])")
  paso "Voz: $VOZ, frase a frase y alineada"
  [ -s "$T/voz/voz.wav" ] || "$PYP" "$REPO/voz/narrar.py" --guion "$AQUI/recursos/voz.json" -o "$T/voz/voz.wav" --voz "$VOZ"
fi

if etapa musica; then
  paso "Música: MusicGen, candidatas de 30 s en un lote"
  python3 "$REPO/imagen/generar.py" --parar >/dev/null 2>&1 || true
  if [ ! -s "$T/musica/pieza_1.wav" ]; then
    mapfile -t desc < <(python3 -c "import json; [print(x) for x in json.load(open('$AQUI/recursos/musica.json'))['candidatas']]")
    "$PYF" "$REPO/audio/musica_ia.py" "${desc[@]}" -o "$T/musica/pieza.wav" --duracion 30 \
      --semilla "$(python3 -c "import json; print(json.load(open('$AQUI/recursos/musica.json'))['semilla'])")"
  fi
  python3 "$REPO/audio/graves.py" "$T"/musica/pieza_*.wav
  # «lecho» en recursos/musica.json (opcional): la pieza elegida tras medirla, alargada a la duración del vídeo; sin
  # fundido de entrada si el corto va en bucle (entrada 0). Sin esto, el lecho se hacía a mano y no quedaba guardado.
  # «comprimir» (opcional, p. ej. 3): compresión suave antes de normalizar, para una pieza con valles muy hondos que
  # bajo la voz dejaba huecos casi en silencio (el piano del corto 8 de supervivencia).
  python3 -c "import json; l = json.load(open('$AQUI/recursos/musica.json')).get('lecho'); l and print(l['pieza'], l['duracion'], l.get('entrada', 0), l.get('recorte', 1.5), l.get('comprimir', 0))" |
    while read -r pieza dura entrada recorte comprimir; do
      [ -s "$T/musica/lecho.wav" ] || python3 "$REPO/audio/lecho.py" "$T/musica/$pieza.wav" "$dura" -o "$T/musica/lecho.wav" \
        --entrada "$entrada" --recorte "$recorte" --cruce 3 --comprimir "$comprimir"
    done
fi

if etapa imagenes; then
  paso "Imágenes: FLUX.3, 720 × 1280, ampliadas con EDSR a 1080 × 1920"
  python3 - "$AQUI/recursos/imagenes.json" "$T/img" > "$T/img/lote.json" <<'PY'
import json, os, sys
d, carpeta = json.load(open(sys.argv[1])), sys.argv[2]
print(json.dumps([{"prompt": p["prompt"] + ", " + d["sufijo"], "salida": os.path.join(carpeta, p["nombre"] + ".png"), "ancho": 720,
                   "alto": 1280, "semilla": p["semilla"], "modelo": "flux3"} for p in d["planchas"]
                  if not os.path.exists(os.path.join(carpeta, p["nombre"] + ".jpg"))]))
PY
  if [ "$(cat "$T/img/lote.json")" != "[]" ]; then
    python3 "$REPO/imagen/generar.py" --lote "$T/img/lote.json"
    [ "${PARAR:-1}" = 0 ] || python3 "$REPO/imagen/generar.py" --parar >/dev/null 2>&1 || true
  fi
  for f in "$T"/img/*.png; do
    [ -e "$f" ] || continue
    case "$f" in *_1920.png) continue ;; esac
    j="${f%.png}.jpg"
    [ -s "$j" ] && continue
    "$PYF" "$REPO/imagen/ampliar.py" "$f" -o "${f%.png}_1920.png" --tamano 1080x1920
    python3 -c "from PIL import Image; Image.open('${f%.png}_1920.png').convert('RGB').save('$j', quality=93)"
  done
fi
printf '\nListo en %d min %d s: %s\n' $((SECONDS / 60)) $((SECONDS % 60)) "$T"
