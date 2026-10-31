#!/usr/bin/env bash
# Recursos de los cortos verticales de BusinessForMen, en salidas/businessformen/cortos/<corto>/ (lo que ya exista no
# se repite): la base de la marca (fuentes y texturas), la voz de cada corto, la música, las imágenes y sus capas 2.5D.
#   canales/businessformen/cortos/preparar.sh                       todos los cortos
#   canales/businessformen/cortos/preparar.sh 04-el-ancla 05-el-perrito
# Orden pensado para la RAM: la voz y la música antes que FLUX (no caben a la vez con el servidor de imágenes); la
# profundidad, después de apagarlo.
set -euo pipefail

REPO="$(cd "$(dirname "$0")/../../.." && pwd)"
AQUI="$REPO/canales/businessformen/cortos"
H="${HERRAMIENTAS:-$HOME/herramientas-videos}"
S="$REPO/salidas/businessformen/cortos"
MARCA="$REPO/salidas/businessformen/marca"
PYP="$H/piper/bin/python"
PYF="$H/fastsdcpu/env/bin/python"
JSD=https://cdn.jsdelivr.net/npm
if [ $# -gt 0 ]; then CORTOS=("$@"); else mapfile -t CORTOS < <(cd "$AQUI" && ls -d [0-9][0-9]-*/ | tr -d /); fi
mkdir -p "$S/musica" "$MARCA"/{img,fuentes}
paso() { printf '\n== %s (%s)\n' "$*" "$(date +%H:%M:%S)"; }

paso "Marca: fuentes (OFL, de @fontsource) y texturas"
fuente() { [ -s "$MARCA/fuentes/$2" ] || curl -fsSL --retry 3 -o "$MARCA/fuentes/$2" "$JSD/$1"; }
fuente @fontsource/inter-tight/files/inter-tight-latin-500-normal.woff2 intertight-500.woff2
fuente @fontsource/inter-tight/files/inter-tight-latin-700-normal.woff2 intertight-700.woff2
fuente @fontsource/inter-tight/files/inter-tight-latin-800-normal.woff2 intertight-800.woff2
fuente @fontsource/ibm-plex-mono/files/ibm-plex-mono-latin-500-normal.woff2 plexmono-500.woff2
fuente @fontsource/bodoni-moda/files/bodoni-moda-latin-500-italic.woff2 bodoni-500-italic.woff2
fuente @fontsource/bodoni-moda/files/bodoni-moda-latin-700-normal.woff2 bodoni-700.woff2
# Las mismas texturas que las pruebas de marca (marca/preparar.sh), con la misma semilla.
[ -s "$MARCA/img/desgaste.png" ] || python3 - "$MARCA/img" <<'EOF'
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

for c in "${CORTOS[@]}"; do
  # recursos/velocidad (opcional): la duración relativa de la voz (1,04 = un 4 % más pausada).
  vel=$(cat "$AQUI/$c/recursos/velocidad" 2>/dev/null || echo 1.0)
  paso "Voz de $c: Supertonic-3 M1 (velocidad $vel), frase a frase y alineada"
  mkdir -p "$S/$c"/{voz,musica,img}
  [ -s "$S/$c/voz/voz.wav" ] || "$PYP" "$REPO/voz/narrar.py" --guion "$AQUI/$c/recursos/voz.json" -o "$S/$c/voz/voz.wav" --velocidad "$vel"
  # recursos/variantes.json (opcional): otras versiones del corto con otra voz, en voz-<variante>/ (montar.py --variante).
  [ -s "$AQUI/$c/recursos/variantes.json" ] && python3 -c "import json; [print(k, x['voz'], x.get('velocidad', 1.0)) for k, x in json.load(open('$AQUI/$c/recursos/variantes.json')).items() if not k.startswith('_')]" |
    while read -r var voz velv; do
      mkdir -p "$S/$c/voz-$var"
      [ -s "$S/$c/voz-$var/voz.wav" ] || "$PYP" "$REPO/voz/narrar.py" --guion "$AQUI/$c/recursos/voz.json" -o "$S/$c/voz-$var/voz.wav" --voz "$voz" --velocidad "$velv" </dev/null
    done
done

paso "Efectos: los de BigSoundBank (CC0) que piden los montajes"
mkdir -p "$S/sfx"
mapfile -t faltan < <(for c in "${CORTOS[@]}"; do grep -oE "sonido\('[0-9]{4}'" "$AQUI/$c/montaje.py" | grep -oE "[0-9]{4}"; done | sort -u |
  while read -r n; do [ -s "$S/sfx/$n.wav" ] || echo "$n"; done)
[ ${#faltan[@]} -eq 0 ] || python3 "$REPO/audio/efectos.py" bajar "${faltan[@]}" -d "$S/sfx"

paso "Música: MusicGen, tandas de cuatro candidatas de 30 s (musica.json)"
python3 "$REPO/imagen/generar.py" --parar >/dev/null 2>&1 || true
python3 -c "import json; [print(t['carpeta'] or '.', t['semilla']) for t in json.load(open('$AQUI/musica.json'))['tandas']]" |
  while read -r carpeta semilla; do
    [ -s "$S/musica/$carpeta/pieza_4.wav" ] && continue
    mkdir -p "$S/musica/$carpeta"
    mapfile -t desc < <(python3 -c "import json; [print(x) for t in json.load(open('$AQUI/musica.json'))['tandas'] if (t['carpeta'] or '.') == '$carpeta' for x in t['candidatas']]")
    "$PYF" "$REPO/audio/musica_ia.py" "${desc[@]}" -o "$S/musica/$carpeta/pieza.wav" --duracion 30 --semilla "$semilla" </dev/null
  done
python3 "$REPO/audio/graves.py" "$S"/musica/pieza_*.wav "$S"/musica/v*/pieza_*.wav
# Los lechos de cada corto, sin entrada (el bucle no puede empezar en silencio): ver «lechos» en musica.json.
python3 -c "import json; [print(k, v['pieza'], v['duracion'], v['entrada'], v['recorte']) for k, v in json.load(open('$AQUI/musica.json'))['lechos'].items()]" |
  while read -r destino pieza dura entrada recorte; do
    mkdir -p "$(dirname "$S/$destino")/musica"
    f="$S/$(dirname "$destino")/musica/$(basename "$destino").wav"
    [ -s "$f" ] || [ ! -s "$S/musica/$pieza.wav" ] || \
      python3 "$REPO/audio/lecho.py" "$S/musica/$pieza.wav" "$dura" -o "$f" --entrada "$entrada" --recorte "$recorte" --cruce 3
  done

paso "Imágenes: FLUX.3, 720 × 1280, ampliadas con EDSR a 1080 × 1920"
python3 - "$AQUI" "$S" "${CORTOS[@]}" > "$S/lote-imagenes.json" <<'EOF'
import json, os, sys
aqui, s, cortos = sys.argv[1], sys.argv[2], sys.argv[3:]
lote = []
for c in cortos:
    for p in json.load(open(os.path.join(aqui, c, 'recursos', 'imagenes.json')))['planchas']:
        if not os.path.exists(os.path.join(s, c, 'img', p['nombre'] + '.png')):
            lote.append({"prompt": p["prompt"], "salida": os.path.join(s, c, 'img', p['nombre'] + '.png'), "ancho": 720,
                         "alto": 1280, "semilla": p["semilla"], "modelo": "flux3"})
print(json.dumps(lote))
EOF
if [ "$(cat "$S/lote-imagenes.json")" != "[]" ]; then
  python3 "$REPO/imagen/generar.py" --lote "$S/lote-imagenes.json"
fi
python3 "$REPO/imagen/generar.py" --parar >/dev/null 2>&1 || true
for c in "${CORTOS[@]}"; do
  for f in "$S/$c"/img/*.png; do
    [ -e "$f" ] || continue
    case "$f" in *_1920.png|*_frente.png|*_prof.png|*_mapa.png) continue ;; esac
    j="${f%.png}.jpg"
    [ -s "$j" ] && continue
    "$PYF" "$REPO/imagen/ampliar.py" "$f" -o "${f%.png}_1920.png" --tamano 1080x1920
    python3 -c "from PIL import Image; Image.open('${f%.png}_1920.png').convert('RGB').save('$j', quality=93)"
  done
done

# «umbral» (opcional): la profundidad del corte entre frente y fondo, si la automática parte el objeto.
paso "2.5D: profundidad (Depth Anything V2 Small) y capas de las imágenes con «capas»"
for c in "${CORTOS[@]}"; do
  python3 -c "import json; [print(p['nombre'], p.get('umbral', '')) for p in json.load(open('$AQUI/$c/recursos/imagenes.json'))['planchas'] if p.get('capas')]" |
    while read -r n umbral; do
      i="$S/$c/img/$n.jpg"
      [ -s "$i" ] || continue
      [ -s "$S/$c/img/${n}_mapa.png" ] || "$PYF" "$REPO/imagen/profundidad.py" "$i" -o "$S/$c/img/${n}_mapa.png" </dev/null
      [ -s "$S/$c/img/${n}_frente.png" ] || "$PYF" "$REPO/imagen/capas25d.py" "$i" "$S/$c/img/${n}_mapa.png" -o "$S/$c/img/$n" \
        --suavidad 0.012 --margen 12 ${umbral:+--umbral "$umbral"} </dev/null
    done
done
printf '\nListo en %d min %d s: %s\n' $((SECONDS / 60)) $((SECONDS % 60)) "$S"
