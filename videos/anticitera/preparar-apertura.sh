#!/usr/bin/env bash
# Recursos de la apertura de «El mecanismo de Anticitera» (unos 33 s, estilo A). No van en git: se
# regeneran aquí, en $TRABAJO, a partir de recursos/ (guion, prompts y semillas, música) y se copian en
# apertura/assets/. Lo hecho se salta.
#
#   videos/anticitera/preparar-apertura.sh            recursos
#   videos/anticitera/preparar-apertura.sh --render   además el vídeo y su versión de entrega
#
# Orden pensado para la RAM: voz y música antes de FLUX (no caben a la vez con el servidor de imágenes).
set -euo pipefail

REPO="$(cd "$(dirname "$0")/../.." && pwd)"
AQUI="$REPO/videos/anticitera"
H="${HERRAMIENTAS:-$HOME/herramientas-videos}"
TRABAJO="${TRABAJO:-$REPO/salidas/anticitera}"
PYF="$H/fastsdcpu/env/bin/python"   # torch, transformers, onnxruntime y OpenCV
PYP="$H/piper/bin/python"
RC="$AQUI/recursos"
SFX_HF="$H/hyperframes/node_modules/hyperframes/dist/skills/media-use/audio/assets/sfx"
JSD=https://cdn.jsdelivr.net/npm
paso() { printf '\n== %s\n' "$*"; }
P="$TRABAJO/planchas" A="$TRABAJO/audio" X="$TRABAJO/sfx" F="$TRABAJO/fuentes"
mkdir -p "$P" "$A" "$X" "$F"

paso "Voz (Supertonic-3 M1, con el tiempo de cada palabra)"
[ -s "$A/voz.wav" ] || "$PYP" "$REPO/voz/narrar.py" --guion "$RC/guion-apertura.json" -o "$A/voz.wav"

paso "Música (MusicGen, las variantes en un lote)"
if [ ! -s "$A/musica_1.wav" ]; then
  mapfile -t variantes < <(python3 -c "import json,sys; [print(v) for v in json.load(open(sys.argv[1]))['variantes']]" "$RC/musica-apertura.json")
  read -r duracion semilla < <(python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print(d['duracion'], d['semilla'])" "$RC/musica-apertura.json")
  "$PYF" "$REPO/audio/musica_ia.py" "${variantes[@]}" -o "$A/musica.wav" --duracion "$duracion" --semilla "$semilla"
fi

paso "Planchas con FLUX.3 Image Klein, 4 pasos (las que falten)"
python3 - "$RC/imagenes-apertura.json" "$P" > "$P/lote.json" <<'EOF'
import json, os, sys
lista, carpeta = json.load(open(sys.argv[1])), sys.argv[2]
print(json.dumps([dict(prompt=i['prompt'], salida=os.path.join(carpeta, i['nombre'] + '.png'),
                       ancho=i['ancho'], alto=i['alto'], semilla=i['semilla'])
                  for i in lista if not os.path.exists(os.path.join(carpeta, i['nombre'] + '.png'))],
                 ensure_ascii=False))
EOF
if [ "$(cat "$P/lote.json")" != "[]" ]; then
  python3 "$REPO/imagen/generar.py" --lote "$P/lote.json" --modelo flux3
fi
python3 "$REPO/imagen/generar.py" --parar >/dev/null 2>&1 || true

paso "Planchas a 1920 × 1080 (EDSR), profundidad y capas 2.5D"
for n in $(python3 -c "import json,sys; print(' '.join(i['nombre'] for i in json.load(open(sys.argv[1]))))" "$RC/imagenes-apertura.json"); do
  if [ ! -s "$P/$n.jpg" ]; then
    "$PYF" "$REPO/imagen/ampliar.py" "$P/$n.png" -o "$P/${n}_1080.png"
    "$PYF" -I -c "from PIL import Image; import sys; Image.open(sys.argv[1]).convert('RGB').save(sys.argv[2], quality=93)" "$P/${n}_1080.png" "$P/$n.jpg"
  fi
  [ -s "$P/${n}_profundidad.png" ] || "$PYF" "$REPO/imagen/profundidad.py" "$P/$n.png" -o "$P/${n}_profundidad.png"
  # Poco paralaje (unos 10 px): borde estrecho y poco margen, para que el relleno no asome (ver capas25d.py).
  [ -s "$P/${n}_frente.png" ] || "$PYF" "$REPO/imagen/capas25d.py" "$P/$n.jpg" "$P/${n}_profundidad.png" -o "$P/$n" \
    --suavidad 0.012 --margen 12
done
# Los contornos de la rueda que revela el escáner salen de la propia plancha.
[ -s "$P/fragmento_lineas.png" ] || "$PYF" -I "$AQUI/lineas_rueda.py" "$P" "$TRABAJO"

paso "Efectos de sonido (BigSoundBank, CC0; y la biblioteca de HyperFrames)"
faltan=()
for n in 0740 0146 2444 3113 2570 1521 1818 1801 1796 2138; do [ -s "$X/$n.wav" ] || faltan+=("$n"); done
[ ${#faltan[@]} -eq 0 ] || python3 "$REPO/audio/efectos.py" bajar "${faltan[@]}" -d "$X"

paso "Fuentes (Google Fonts vía jsDelivr, licencia OFL)"
fuente() { [ -s "$F/$2" ] || curl -fsSL --retry 3 -o "$F/$2" "$JSD/$1"; }
fuente @fontsource/cormorant-garamond/files/cormorant-garamond-latin-500-normal.woff2 cormorant-500.woff2
fuente @fontsource/cormorant-garamond/files/cormorant-garamond-latin-500-italic.woff2 cormorant-500-italic.woff2
fuente @fontsource/hanken-grotesk/files/hanken-grotesk-latin-500-normal.woff2 hanken-500.woff2
fuente @fontsource/hanken-grotesk/files/hanken-grotesk-latin-600-normal.woff2 hanken-600.woff2

paso "Copia en apertura/assets"
d="$AQUI/apertura/assets"
mkdir -p "$d/img" "$d/audio" "$d/sfx" "$d/fonts"
for n in tormenta isla buzo estatuas fragmento; do
  for s in _fondo.jpg _frente.png _prof.png; do cp -f "$P/$n$s" "$d/img/$n$s"; done
done
cp -f "$P/fragmento_lineas.png" "$d/img/"
cp -f "$P/fragmento.jpg" "$d/img/"            # el fragmento no tiene paralaje: va sin capas
cp -f "$A/voz.wav" "$d/audio/voz.wav"
cp -f "$A/musica_1.wav" "$d/audio/musica.wav"      # la variante elegida: ver la bitácora
copiar() { cp -f "$1" "$d/sfx/$2"; }
copiar "$X/0740.wav" lluvia.wav; copiar "$X/0146.wav" viento.wav; copiar "$X/2444.wav" jarcias.wav
copiar "$X/3113.wav" trueno.wav; copiar "$X/2570.wav" olas.wav; copiar "$X/1521.wav" chapuzon.wav
copiar "$X/1818.wav" cuerda.wav; copiar "$X/1801.wav" barrido.wav; copiar "$X/1796.wav" escaner.wav
copiar "$X/2138.wav" tictac.wav
copiar "$SFX_HF/whoosh-cinematic.mp3" travesia.mp3; copiar "$SFX_HF/impact-bass-1.mp3" golpe.mp3
for f in cormorant-500.woff2 cormorant-500-italic.woff2 hanken-500.woff2 hanken-600.woff2; do cp -f "$F/$f" "$d/fonts/$f"; done
cp -f "$X/CREDITOS.md" "$TRABAJO/CREDITOS-sonido.md" 2>/dev/null || true

if [ "${1:-}" = "--render" ]; then
  paso "Render (calidad de entrega) y versión de entrega"
  (cd "$AQUI/apertura" && "$REPO/video/hf.sh" render -o "$TRABAJO/apertura.mp4" --quality high --crf 20 --quiet)
  "$REPO/video/entregar.sh" "$TRABAJO/apertura.mp4" "$TRABAJO/apertura-entrega.mp4" -15 copiar
fi
printf '\nListo en %d min %d s. Recursos en %s\n' $((SECONDS / 60)) $((SECONDS % 60)) "$TRABAJO"
