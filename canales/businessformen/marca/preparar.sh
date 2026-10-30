#!/usr/bin/env bash
# Recursos de las pruebas de marca de BusinessForMen, en salidas/businessformen/marca/ (lo que ya exista no se
# repite). Luego montar.py los pone en cada proyecto y --render los renderiza y deja la entrega a −15 LUFS.
#   canales/businessformen/marca/preparar.sh            voz, música, imagen, texturas y fuentes; y montar
#   canales/businessformen/marca/preparar.sh --render   además los tres vídeos, las miniaturas y la hoja comparativa
# Orden pensado para la RAM: la voz y la música antes que FLUX (no caben a la vez con el servidor de imágenes).
set -euo pipefail

REPO="$(cd "$(dirname "$0")/../../.." && pwd)"
AQUI="$REPO/canales/businessformen/marca"
H="${HERRAMIENTAS:-$HOME/herramientas-videos}"
M="${TRABAJO:-$REPO/salidas/businessformen/marca}"
PYP="$H/piper/bin/python"
PYF="$H/fastsdcpu/env/bin/python"
JSD=https://cdn.jsdelivr.net/npm
mkdir -p "$M"/{voz,musica/consejo,img,fuentes,renders,miniaturas,entrega}
paso() { printf '\n== %s (%s)\n' "$*" "$(date +%H:%M:%S)"; }

paso "Voz: Supertonic-3 M1"
[ -s "$M/voz/prueba.wav" ] || "$PYP" "$REPO/voz/narrar.py" --guion "$AQUI/recursos/guion.json" -o "$M/voz/prueba.wav"

paso "Música: MusicGen, una pieza de 20 s por ruta y su lecho de 18,4 s"
python3 "$REPO/imagen/generar.py" --parar >/dev/null 2>&1 || true
if [ ! -s "$M/musica/pieza_3.wav" ]; then
  mapfile -t desc < <(python3 -c "import json; d=json.load(open('$AQUI/recursos/musica.json')); [print(d['piezas'][k]) for k in ('sastre', 'consejo', 'lacre')]")
  "$PYF" "$REPO/audio/musica_ia.py" "${desc[@]}" -o "$M/musica/pieza.wav" --duracion 20 --semilla 7
fi
# La primera de «Consejo» salió con el 90 % de la energía bajo 150 Hz (no se oye en un móvil): se rehízo con dos
# descripciones más brillantes y se quedó la primera (las dos, en recursos/musica.json, «consejo_bis»).
if [ ! -s "$M/musica/consejo/pieza_1.wav" ]; then
  mapfile -t desc < <(python3 -c "import json; [print(x) for x in json.load(open('$AQUI/recursos/musica.json'))['consejo_bis']]")
  "$PYF" "$REPO/audio/musica_ia.py" "${desc[@]}" -o "$M/musica/consejo/pieza.wav" --duracion 20 --semilla 7
fi
[ -s "$M/musica/sastre.wav" ] || python3 "$REPO/audio/lecho.py" "$M/musica/pieza_1.wav" 18.4 -o "$M/musica/sastre.wav"
[ -s "$M/musica/consejo.wav" ] || python3 "$REPO/audio/lecho.py" "$M/musica/consejo/pieza_1.wav" 18.4 -o "$M/musica/consejo.wav"
[ -s "$M/musica/lacre.wav" ] || python3 "$REPO/audio/lecho.py" "$M/musica/pieza_3.wav" 18.4 -o "$M/musica/lacre.wav"

paso "Imagen: FLUX.3, 1280 × 720, ampliada con EDSR"
if [ ! -s "$M/img/mesa.jpg" ]; then
  python3 - "$AQUI/recursos/imagen.json" "$M/img/mesa.png" > "$M/lote-imagen.json" <<'EOF'
import json, sys
r = json.load(open(sys.argv[1]))
print(json.dumps([{"prompt": r["prompt"], "salida": sys.argv[2], "ancho": 1280, "alto": 720, "semilla": r["semilla"], "modelo": "flux3"}]))
EOF
  python3 "$REPO/imagen/generar.py" --lote "$M/lote-imagen.json"
  python3 "$REPO/imagen/generar.py" --parar >/dev/null 2>&1 || true
  "$PYF" "$REPO/imagen/ampliar.py" "$M/img/mesa.png" -o "$M/img/mesa_1080.png"
  python3 -c "from PIL import Image; Image.open('$M/img/mesa_1080.png').convert('RGB').save('$M/img/mesa.jpg', quality=93)"
fi

paso "Texturas: grano de película y desgaste de sello"
[ -s "$M/img/desgaste.png" ] || python3 - "$M/img" <<'EOF'
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
EOF

paso "Fuentes (licencia OFL, de @fontsource)"
fuente() { [ -s "$M/fuentes/$2" ] || curl -fsSL --retry 3 -o "$M/fuentes/$2" "$JSD/$1"; }
fuente @fontsource/bodoni-moda/files/bodoni-moda-latin-500-normal.woff2 bodoni-500.woff2
fuente @fontsource/bodoni-moda/files/bodoni-moda-latin-500-italic.woff2 bodoni-500-italic.woff2
fuente @fontsource/bodoni-moda/files/bodoni-moda-latin-700-normal.woff2 bodoni-700.woff2
fuente @fontsource/jost/files/jost-latin-400-normal.woff2 jost-400.woff2
fuente @fontsource/jost/files/jost-latin-500-normal.woff2 jost-500.woff2
fuente @fontsource/inter-tight/files/inter-tight-latin-500-normal.woff2 intertight-500.woff2
fuente @fontsource/inter-tight/files/inter-tight-latin-700-normal.woff2 intertight-700.woff2
fuente @fontsource/inter-tight/files/inter-tight-latin-800-normal.woff2 intertight-800.woff2
fuente @fontsource/ibm-plex-mono/files/ibm-plex-mono-latin-500-normal.woff2 plexmono-500.woff2
fuente @fontsource/archivo-narrow/files/archivo-narrow-latin-700-normal.woff2 archivonarrow-700.woff2
fuente @fontsource/archivo/files/archivo-latin-500-normal.woff2 archivo-500.woff2
fuente @fontsource/archivo/files/archivo-latin-600-normal.woff2 archivo-600.woff2
fuente @fontsource/instrument-serif/files/instrument-serif-latin-400-italic.woff2 instrument-400-italic.woff2
fuente @fontsource/instrument-serif/files/instrument-serif-latin-400-normal.woff2 instrument-400.woff2

paso "Montar las tres rutas y sus miniaturas"
python3 "$AQUI/montar.py"

if [ "${1:-}" = "--render" ]; then
  for r in sastre consejo lacre; do
    paso "Render de $r"
    (cd "$AQUI/$r" && "$REPO/video/hf.sh" render -o "$M/renders/$r.mp4" --quality high --crf 20 --quiet)
    PICO=-2 "$REPO/video/entregar.sh" "$M/renders/$r.mp4" "$M/entrega/businessformen-$r.mp4" -15 copiar
    (cd "$AQUI/miniaturas/$r" && "$REPO/video/hf.sh" snapshot --at 0.5 --no-end -o "$M/miniaturas/$r")
    python3 -c "from PIL import Image; Image.open('$M/miniaturas/$r/frame-00-at-0.5s.png').convert('RGB').resize((1280, 720), Image.LANCZOS).save('$M/miniaturas/$r.jpg', quality=92)"
  done
  python3 "$AQUI/hoja.py" "$M/entrega/hoja-marca.jpg"
fi
printf '\nListo en %d min %d s: %s\n' $((SECONDS / 60)) $((SECONDS % 60)) "$M"
