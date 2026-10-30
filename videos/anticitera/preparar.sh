#!/usr/bin/env bash
# Recursos de los capítulos de «El mecanismo de Anticitera» (la apertura tiene su preparar-apertura.sh).
# No van en git: se regeneran en $TRABAJO a partir de recursos/ (guion, prompts y semillas, música).
# Lo hecho se salta. Orden pensado para la RAM: FLUX no cabe a la vez que MusicGen.
#
#   videos/anticitera/preparar.sh voz         narración de cada capítulo (Supertonic-3 M1, con tiempos)
#   videos/anticitera/preparar.sh planchas    FLUX.3 en un lote, luego EDSR, profundidad y capas 2.5D
#   videos/anticitera/preparar.sh musica      una pieza por capítulo (MusicGen, en lotes de 4) y su lecho
#   videos/anticitera/preparar.sh fuentes     fuentes y efectos de sonido
#   videos/anticitera/preparar.sh             todo, en ese orden
set -euo pipefail

REPO="$(cd "$(dirname "$0")/../.." && pwd)"
AQUI="$REPO/videos/anticitera"
H="${HERRAMIENTAS:-$HOME/herramientas-videos}"
TRABAJO="${TRABAJO:-$REPO/salidas/anticitera}"
PYF="$H/fastsdcpu/env/bin/python"
PYP="$H/piper/bin/python"
RC="$AQUI/recursos"
JSD=https://cdn.jsdelivr.net/npm
paso() { printf '\n== %s (%s)\n' "$*" "$(date +%H:%M:%S)"; }
P="$TRABAJO/planchas" V="$TRABAJO/voz" M="$TRABAJO/musica" X="$TRABAJO/sfx" F="$TRABAJO/fuentes"
mkdir -p "$P" "$V" "$M" "$X" "$F"
CAPS=$(python3 -c "import json,sys; print(' '.join(c['id'] for c in json.load(open(sys.argv[1]))['capitulos']))" "$RC/guion.json")

voz() {
  paso "Voz de los capítulos (Supertonic-3 M1, semilla fija por frase)"
  for c in $CAPS; do
    [ -s "$V/$c.wav" ] && continue
    python3 -c "import json,sys; c=[x for x in json.load(open(sys.argv[1]))['capitulos'] if x['id']==sys.argv[2]][0]; json.dump(c['frases'], open(sys.argv[3],'w'), ensure_ascii=False)" \
      "$RC/guion.json" "$c" "$V/$c-guion.json"
    "$PYP" "$REPO/voz/narrar.py" --guion "$V/$c-guion.json" -o "$V/$c.wav"
  done
}

planchas() {
  paso "Planchas con FLUX.3 Image Klein, 4 pasos, 1280 × 720 (las que falten)"
  python3 - "$RC/imagenes.json" "$P" > "$P/lote-capitulos.json" <<'EOF'
import json, os, sys
d, carpeta = json.load(open(sys.argv[1])), sys.argv[2]
print(json.dumps([dict(prompt=i['prompt'] + ', ' + d['sufijo'], salida=os.path.join(carpeta, i['nombre'] + '.png'),
                       ancho=1280, alto=720, semilla=i['semilla'])
                  for i in d['planchas'] if not os.path.exists(os.path.join(carpeta, i['nombre'] + '.png'))],
                 ensure_ascii=False))
EOF
  if [ "$(cat "$P/lote-capitulos.json")" != "[]" ]; then
    python3 "$REPO/imagen/generar.py" --lote "$P/lote-capitulos.json" --modelo flux3
  fi
  python3 "$REPO/imagen/generar.py" --parar >/dev/null 2>&1 || true
  posproceso
}

posproceso() {
  paso "Planchas a 1920 × 1080 (EDSR), profundidad y capas 2.5D"
  for n in $(python3 -c "import json,sys; print(' '.join(i['nombre'] for i in json.load(open(sys.argv[1]))['planchas']))" "$RC/imagenes.json"); do
    [ -s "$P/$n.png" ] || continue
    if [ ! -s "$P/$n.jpg" ]; then
      "$PYF" "$REPO/imagen/ampliar.py" "$P/$n.png" -o "$P/${n}_1080.png"
      "$PYF" -I -c "from PIL import Image; import sys; Image.open(sys.argv[1]).convert('RGB').save(sys.argv[2], quality=93)" "$P/${n}_1080.png" "$P/$n.jpg"
    fi
    [ -s "$P/${n}_profundidad.png" ] || "$PYF" "$REPO/imagen/profundidad.py" "$P/$n.png" -o "$P/${n}_profundidad.png"
    # Poco paralaje (unos 10 px): borde estrecho y poco margen, como en la apertura (ver capas25d.py).
    [ -s "$P/${n}_frente.png" ] || "$PYF" "$REPO/imagen/capas25d.py" "$P/$n.jpg" "$P/${n}_profundidad.png" -o "$P/$n" \
      --suavidad 0.012 --margen 12
  done
}

musica() {
  paso "Música: una pieza de 30 s por capítulo (MusicGen, en lotes de 4) y su lecho a la duración del capítulo"
  python3 "$REPO/imagen/generar.py" --parar >/dev/null 2>&1 || true
  if [ ! -s "$M/pieza_1.wav" ]; then
    mapfile -t piezas < <(python3 -c "import json,sys; [print(p) for p in json.load(open(sys.argv[1]))['piezas']]" "$RC/musica.json")
    read -r duracion semilla < <(python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print(d['duracion'], d['semilla'])" "$RC/musica.json")
    "$PYF" "$REPO/audio/musica_ia.py" "${piezas[@]}" -o "$M/pieza.wav" --duracion "$duracion" --semilla "$semilla"
  fi
  # Las piezas que salieron con casi toda la energía en los graves se rehacen aparte (ver musica.json).
  if [ ! -e "$M/sustituidas" ]; then
    mapfile -t nums < <(python3 -c "import json,sys; [print(k) for k in json.load(open(sys.argv[1]))['sustituir']['piezas']]" "$RC/musica.json")
    mapfile -t desc < <(python3 -c "import json,sys; [print(v) for v in json.load(open(sys.argv[1]))['sustituir']['piezas'].values()]" "$RC/musica.json")
    semilla=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['sustituir']['semilla'])" "$RC/musica.json")
    mkdir -p "$M/sust"
    "$PYF" "$REPO/audio/musica_ia.py" "${desc[@]}" -o "$M/sust/pieza.wav" --duracion 30 --semilla "$semilla"
    for i in "${!nums[@]}"; do cp -f "$M/sust/pieza_$((i + 1)).wav" "$M/pieza_${nums[$i]}.wav"; done
    touch "$M/sustituidas"
  fi
  python3 "$AQUI/kit/lechos.py"
}

fuentes() {
  paso "Fuentes (Google Fonts vía jsDelivr, OFL) y efectos de sonido (BigSoundBank, CC0)"
  fuente() { [ -s "$F/$2" ] || curl -fsSL --retry 3 -o "$F/$2" "$JSD/$1"; }
  fuente @fontsource/cormorant-garamond/files/cormorant-garamond-latin-500-normal.woff2 cormorant-500.woff2
  fuente @fontsource/cormorant-garamond/files/cormorant-garamond-latin-500-italic.woff2 cormorant-500-italic.woff2
  fuente @fontsource/hanken-grotesk/files/hanken-grotesk-latin-500-normal.woff2 hanken-500.woff2
  fuente @fontsource/hanken-grotesk/files/hanken-grotesk-latin-600-normal.woff2 hanken-600.woff2
  fuente @fontsource/gfs-didot/files/gfs-didot-greek-400-normal.woff2 didot-griego.woff2
  faltan=()
  for n in 0740 0146 2444 3113 2570 1801 1796 2138 2655 2816 2841 0425 1880 0194 0987 2857 2212 0221 1267 3061 \
           0052 2118 0086 1515 0155 2470 3590 2728 1800 3060; do
    [ -s "$X/$n.wav" ] || faltan+=("$n")
  done
  [ ${#faltan[@]} -eq 0 ] || python3 "$REPO/audio/efectos.py" bajar "${faltan[@]}" -d "$X"
}

pasos=("${@:-voz planchas musica fuentes}")
read -r -a pasos <<< "${pasos[*]}"
for p in "${pasos[@]}"; do
  case "$p" in
    voz|planchas|posproceso|musica|fuentes) "$p" ;;
    *) echo "Paso desconocido: $p (voz, planchas, posproceso, musica o fuentes)"; exit 2 ;;
  esac
done
printf '\nListo en %d min %d s. Recursos en %s\n' $((SECONDS / 60)) $((SECONDS % 60)) "$TRABAJO"
