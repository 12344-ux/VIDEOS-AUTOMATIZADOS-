#!/usr/bin/env bash
# Recursos del vídeo 1 de BusinessForMen («Por qué quiebran empresas que ganan dinero»), en
# salidas/businessformen/01-flujo-de-caja/: lo que ya exista no se repite.
#   canales/businessformen/videos/01-flujo-de-caja/preparar.sh
# Orden pensado para la RAM: la voz y la música antes que FLUX (no caben a la vez con el servidor de imágenes).
set -euo pipefail

REPO="$(cd "$(dirname "$0")/../../../.." && pwd)"
AQUI="$REPO/canales/businessformen/videos/01-flujo-de-caja"
H="${HERRAMIENTAS:-$HOME/herramientas-videos}"
T="${TRABAJO:-$REPO/salidas/businessformen/01-flujo-de-caja}"
MARCA="$REPO/salidas/businessformen/marca"
PYP="$H/piper/bin/python"
PYF="$H/fastsdcpu/env/bin/python"
mkdir -p "$T"/{voz,musica,img}
paso() { printf '\n== %s (%s)\n' "$*" "$(date +%H:%M:%S)"; }

paso "Voz: Supertonic-3 M1, frase a frase y alineada"
[ -s "$T/voz/voz.wav" ] || "$PYP" "$REPO/voz/narrar.py" --guion "$AQUI/recursos/voz.json" -o "$T/voz/voz.wav"

paso "Música: MusicGen, cuatro candidatas de 20 s, y los lechos de cada tramo"
python3 "$REPO/imagen/generar.py" --parar >/dev/null 2>&1 || true
# Las candidatas y cuál va a cada tramo están en recursos/musica.json (las primeras, con «pulse» o cuerdas
# punteadas, salieron con casi toda la energía bajo 150 Hz: no se oyen en un móvil).
if [ ! -s "$T/musica/v2/pieza_4.wav" ]; then
  mkdir -p "$T/musica/v2"
  mapfile -t desc < <(python3 -c "import json; [print(x) for x in json.load(open('$AQUI/recursos/musica.json'))['candidatas']]")
  "$PYF" "$REPO/audio/musica_ia.py" "${desc[@]}" -o "$T/musica/v2/pieza.wav" --duracion 20 --semilla 11
fi
[ -s "$T/musica/gancho.wav" ] || python3 "$REPO/audio/lecho.py" "$T/musica/v2/pieza_4.wav" 30 -o "$T/musica/gancho.wav" --cruce 2.5
[ -s "$T/musica/ladrones.wav" ] || python3 "$REPO/audio/lecho.py" "$T/musica/v2/pieza_3.wav" 56 -o "$T/musica/ladrones.wav" --cruce 3
# La de los tramos que explican es la de la marca (Consejo); si falta, la rehace preparar.sh de la marca.
[ -s "$T/musica/explica.wav" ] || python3 "$REPO/audio/lecho.py" "$MARCA/musica/consejo/pieza_1.wav" 60 -o "$T/musica/explica.wav" --cruce 3
# La segunda parte (la historia, Carillion, Amazon y el cierre): otras cuatro candidatas, semilla 13.
if [ ! -s "$T/musica/v3/pieza_4.wav" ]; then
  mkdir -p "$T/musica/v3"
  mapfile -t desc < <(python3 -c "import json; [print(x) for x in json.load(open('$AQUI/recursos/musica.json'))['candidatas_2']]")
  "$PYF" "$REPO/audio/musica_ia.py" "${desc[@]}" -o "$T/musica/v3/pieza.wav" --duracion 20 --semilla 13
fi
python3 -c "import json; [print(k, *v) for k, v in json.load(open('$AQUI/recursos/musica.json'))['lechos_2'].items()]" |
  while read -r nombre pieza dura; do
    [ -s "$T/musica/$nombre.wav" ] || python3 "$REPO/audio/lecho.py" "$T/musica/v3/pieza_$pieza.wav" "$dura" -o "$T/musica/$nombre.wav" --cruce 3
  done

paso "Imágenes: FLUX.3, 1280 × 720, ampliadas con EDSR"
python3 - "$AQUI/recursos/imagenes.json" "$T/img" > "$T/img/lote.json" <<'EOF'
import json, os, sys
d, carpeta = json.load(open(sys.argv[1])), sys.argv[2]
print(json.dumps([{"prompt": p["prompt"], "salida": os.path.join(carpeta, p["nombre"] + ".png"), "ancho": 1280, "alto": 720,
                   "semilla": p["semilla"], "modelo": "flux3"} for p in d["planchas"] if not os.path.exists(os.path.join(carpeta, p["nombre"] + ".jpg"))]))
EOF
if [ "$(cat "$T/img/lote.json")" != "[]" ]; then
  python3 "$REPO/imagen/generar.py" --lote "$T/img/lote.json"
  python3 "$REPO/imagen/generar.py" --parar >/dev/null 2>&1 || true
fi
for f in "$T"/img/*.png; do
  case "$f" in *_1080.png) continue ;; esac
  j="${f%.png}.jpg"
  [ -s "$j" ] && continue
  "$PYF" "$REPO/imagen/ampliar.py" "$f" -o "${f%.png}_1080.png"
  python3 -c "from PIL import Image; Image.open('${f%.png}_1080.png').convert('RGB').save('$j', quality=93)"
done
printf '\nListo en %d min %d s: %s\n' $((SECONDS / 60)) $((SECONDS % 60)) "$T"
