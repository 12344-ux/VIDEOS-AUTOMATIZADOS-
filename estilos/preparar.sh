#!/usr/bin/env bash
# Prepara los recursos de las tres pruebas de estilo de «El faro» y, con --render, las
# renderiza. Los recursos (imágenes, voz, música, efectos y fuentes) no van en git: se
# regeneran aquí, en $TRABAJO, y se copian en la carpeta assets/ de cada proyecto.
#
#   estilos/preparar.sh            recursos (unos 17 min en una sesión nueva; lo hecho se salta)
#   estilos/preparar.sh --render   además renderiza los tres vídeos (unos 8 min) y sus entregas
#
# Necesita ./instalar.sh (voz, imagen y edicion). Tiempos medidos el 29-oct-2026: imágenes
# 2,5 min cada una, música 1 min por estilo, profundidad 3 s, recorte 27 s, render 2–3 min.
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
H="${HERRAMIENTAS:-$HOME/herramientas-videos}"
TRABAJO="${TRABAJO:-$REPO/salidas/estilos}"
PYF="$H/fastsdcpu/env/bin/python"   # torch, transformers, onnxruntime y OpenCV
PYP="$H/piper/bin/python"
RC="$REPO/estilos/recursos"
SFX_HF="$H/hyperframes/node_modules/hyperframes/dist/skills/media-use/audio/assets/sfx"
JSD=https://cdn.jsdelivr.net/npm
paso() { printf '\n== %s\n' "$*"; }
P="$TRABAJO/planchas" A="$TRABAJO/audio" X="$TRABAJO/sfx" F="$TRABAJO/fuentes"
mkdir -p "$P" "$A" "$X" "$F"

paso "Imágenes con FLUX.3 Image Klein (las que falten)"
python3 - "$RC/imagenes.json" "$P" > "$P/lote.json" <<'EOF'
import json, os, sys
lista, carpeta = json.load(open(sys.argv[1])), sys.argv[2]
pendientes = [dict(prompt=i['prompt'], salida=os.path.join(carpeta, i['nombre'] + '.png'),
                   ancho=i['ancho'], alto=i['alto'], semilla=i['semilla'])
              for i in lista if not os.path.exists(os.path.join(carpeta, i['nombre'] + '.png'))]
print(json.dumps(pendientes, ensure_ascii=False))
EOF
if [ "$(cat "$P/lote.json")" != "[]" ]; then
  python3 "$REPO/imagen/generar.py" --lote "$P/lote.json" --modelo flux3
fi
# El servidor de imágenes ocupa 8–9 GB: se apaga antes de cargar otros modelos (si no, falta RAM).
python3 "$REPO/imagen/generar.py" --parar >/dev/null 2>&1 || true

paso "Planchas a 1920 × 1080, profundidad, capas 2.5D y recorte de la brújula"
for n in faro manos haz; do
  [ -s "$P/$n.jpg" ] || "$PYF" -I - "$P/$n.png" "$P/$n.jpg" <<'EOF'
import sys
from PIL import Image, ImageFilter
im = Image.open(sys.argv[1]).convert('RGB').resize((1920, 1080), Image.LANCZOS)
im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=60, threshold=2)).save(sys.argv[2], quality=93)
EOF
  [ -s "$P/${n}_profundidad.png" ] || "$PYF" "$REPO/imagen/profundidad.py" "$P/$n.png" -o "$P/${n}_profundidad.png"
done
# Capas: <nombre>_fondo.jpg, <nombre>_frente.png y <nombre>_prof.png (la profundidad de cada capa).
[ -s "$P/faro_frente.png" ] || "$PYF" "$REPO/imagen/capas25d.py" "$P/faro.jpg" "$P/faro_profundidad.png" -o "$P/faro"
# --tapar borra una mancha naranja que FLUX dejó junto a la mano.
[ -s "$P/manos_frente.png" ] || "$PYF" "$REPO/imagen/capas25d.py" "$P/manos.jpg" "$P/manos_profundidad.png" -o "$P/manos" --tapar 1610,560,100
[ -s "$P/brujula.png" ] || "$PYF" "$REPO/imagen/recortar.py" "$P/brujula_blanco.png" -o "$P/brujula.png" --ajustar
[ -s "$P/carta.jpg" ] || "$PYF" -I -c "from PIL import Image; import sys; Image.open(sys.argv[1]).convert('RGB').save(sys.argv[2], quality=92)" "$P/carta.png" "$P/carta.jpg"

paso "Voz (Piper, es_AR-daniela-high, con el tiempo de cada palabra)"
[ -s "$A/voz.wav" ] || "$PYP" "$REPO/voz/narrar.py" --guion "$RC/guion.json" -o "$A/voz.wav" --voz es_AR-daniela-high --velocidad 1.08

paso "Música (MusicGen, una por estilo)"
if [ ! -s "$A/musica_3.wav" ]; then
  mapfile -t descripciones < <(python3 -c "import json,sys; d=json.load(open(sys.argv[1])); [print(d['estilos'][e]) for e in 'abc']" "$RC/musica.json")
  "$PYF" "$REPO/audio/musica_ia.py" "${descripciones[@]}" -o "$A/musica.wav" --duracion 12 --semilla 7
fi

paso "Efectos de sonido reales (BigSoundBank, CC0) y recortes"
faltan=()
for n in 0004 1049 1796 1799 2570 2212 0298 0297 1410 0221 2844 2841; do [ -s "$X/$n.wav" ] || faltan+=("$n"); done
[ ${#faltan[@]} -eq 0 ] || python3 "$REPO/audio/efectos.py" bajar "${faltan[@]}" -d "$X"
recortar() { [ -s "$X/$2" ] || ffmpeg -v error -y -i "$X/$1.wav" -af "$3" "$X/$2"; }
recortar 0004 cerilla.wav "atrim=0.10:2.40,asetpts=PTS-STARTPTS,afade=t=out:st=1.8:d=0.5"
recortar 2570 olas.wav "atrim=20:32,asetpts=PTS-STARTPTS"
recortar 2212 papel.wav "atrim=0.45:1.40,asetpts=PTS-STARTPTS,afade=t=out:st=0.75:d=0.2"
recortar 0298 cinta.wav "atrim=1.30:1.95,asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st=0.5:d=0.15"
recortar 0297 cinta2.wav "atrim=2.70:3.30,asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st=0.45:d=0.15"
recortar 1410 sello.wav "atrim=0.32:1.17,asetpts=PTS-STARTPTS"
recortar 0221 lapiz.wav "atrim=0.0:1.4,asetpts=PTS-STARTPTS,afade=t=out:st=1.1:d=0.3"
# Mismas letras y tiempos que la animación de la máquina de escribir en estilo-c.
[ -s "$X/tecleo.wav" ] || python3 "$REPO/audio/tecleo.py" "$X/2841.wav" -o "$X/tecleo.wav" --duracion 10 \
  --texto "CABO NORTE" --desde 0.8 --paso 0.053 --texto "LIBRO DE GUARDIA · 1891–2026" --desde 7.45 --paso 0.05

paso "Fuentes (Google Fonts vía jsDelivr, licencia OFL)"
fuente() { [ -s "$F/$2" ] || curl -fsSL --retry 3 -o "$F/$2" "$JSD/$1"; }
fuente @fontsource/cormorant-garamond/files/cormorant-garamond-latin-500-normal.woff2 cormorant-500.woff2
fuente @fontsource/cormorant-garamond/files/cormorant-garamond-latin-500-italic.woff2 cormorant-500-italic.woff2
fuente @fontsource/hanken-grotesk/files/hanken-grotesk-latin-500-normal.woff2 hanken-500.woff2
fuente @fontsource/hanken-grotesk/files/hanken-grotesk-latin-600-normal.woff2 hanken-600.woff2
fuente @fontsource-variable/archivo@5.2.8/files/archivo-latin-standard-normal.woff2 archivo-var.woff2
fuente @fontsource/im-fell-english/files/im-fell-english-latin-400-normal.woff2 imfell-400.woff2
fuente @fontsource/im-fell-english/files/im-fell-english-latin-400-italic.woff2 imfell-400-italic.woff2
fuente @fontsource/special-elite/files/special-elite-latin-400-normal.woff2 special-elite.woff2
fuente @fontsource/la-belle-aurore/files/la-belle-aurore-latin-400-normal.woff2 mano-la-belle-aurore.woff2

paso "Copia en cada proyecto"
copiar() { mkdir -p "$(dirname "$2")"; cp -f "$1" "$2"; }
i=1
for e in a b c; do
  copiar "$A/voz.wav" "$REPO/estilos/estilo-$e/assets/audio/voz.wav"
  copiar "$A/musica_$i.wav" "$REPO/estilos/estilo-$e/assets/audio/musica.wav"
  i=$((i + 1))
done
d="$REPO/estilos/estilo-a/assets"
for f in faro_fondo.jpg faro_frente.png faro_prof.png manos_fondo.jpg manos_frente.png manos_prof.png haz.jpg; do copiar "$P/$f" "$d/img/$f"; done
"$PYF" -I -c "from PIL import Image; import sys; Image.open(sys.argv[1]).convert('L').resize((960, 540), Image.BILINEAR).save(sys.argv[2])" "$P/haz_profundidad.png" "$d/img/haz_prof.png"
for f in cormorant-500.woff2 cormorant-500-italic.woff2 hanken-500.woff2 hanken-600.woff2; do copiar "$F/$f" "$d/fonts/$f"; done
copiar "$X/1049.wav" "$d/sfx/sirena.wav"; copiar "$X/1796.wav" "$d/sfx/barrido.wav"; copiar "$X/cerilla.wav" "$d/sfx/cerilla.wav"
copiar "$X/olas.wav" "$d/sfx/olas.wav"; copiar "$SFX_HF/whoosh-cinematic.mp3" "$d/sfx/oleada.mp3"; copiar "$SFX_HF/impact-bass-1.mp3" "$d/sfx/golpe.mp3"
d="$REPO/estilos/estilo-b/assets"
for f in faro.jpg manos.jpg haz.jpg; do copiar "$P/$f" "$d/img/$f"; done
copiar "$F/archivo-var.woff2" "$d/fonts/archivo-var.woff2"
copiar "$SFX_HF/key-press.mp3" "$d/sfx/tecla.mp3"; copiar "$SFX_HF/click-soft.mp3" "$d/sfx/clic.mp3"
copiar "$SFX_HF/whoosh-short.mp3" "$d/sfx/barrido-1.mp3"; copiar "$X/1799.wav" "$d/sfx/barrido-2.wav"; copiar "$X/1796.wav" "$d/sfx/barrido-3.wav"
copiar "$SFX_HF/impact-bass-1.mp3" "$d/sfx/golpe.mp3"; copiar "$SFX_HF/pop.mp3" "$d/sfx/pop.mp3"
d="$REPO/estilos/estilo-c/assets"
for f in faro.jpg manos.jpg haz.jpg carta.jpg brujula.png; do copiar "$P/$f" "$d/img/$f"; done
for f in imfell-400.woff2 imfell-400-italic.woff2 special-elite.woff2 mano-la-belle-aurore.woff2; do copiar "$F/$f" "$d/fonts/$f"; done
for f in papel.wav cinta.wav cinta2.wav sello.wav lapiz.wav tecleo.wav; do copiar "$X/$f" "$d/sfx/$f"; done
copiar "$X/2844.wav" "$d/sfx/campana.wav"
cp -f "$X/CREDITOS.md" "$TRABAJO/CREDITOS-sonido.md" 2>/dev/null || true

if [ "${1:-}" = "--render" ]; then
  for e in a b c; do
    paso "Render del estilo $e"
    # Ya con la calidad de entrega (CRF 20): entregar.sh solo trata el sonido y copia el vídeo.
    (cd "$REPO/estilos/estilo-$e" && "$REPO/video/hf.sh" render -o "$TRABAJO/estilo-$e.mp4" --crf 20 --workers auto --quiet)
    "$REPO/video/entregar.sh" "$TRABAJO/estilo-$e.mp4" "$TRABAJO/estilo-$e-entrega.mp4" -15 copiar
  done
fi
printf '\nListo en %d min %d s. Recursos en %s\n' $((SECONDS / 60)) $((SECONDS % 60)) "$TRABAJO"
