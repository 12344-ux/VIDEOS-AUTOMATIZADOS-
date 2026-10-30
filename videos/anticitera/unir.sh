#!/usr/bin/env bash
# El vídeo completo de «El mecanismo de Anticitera»: une la apertura y los ocho capítulos renderizados.
#   videos/anticitera/unir.sh            renderiza lo que falte (en $TRABAJO/renders) y une
#   videos/anticitera/unir.sh --unir     solo une lo ya renderizado
# La imagen se copia tal cual (los renders salen ya a calidad de entrega: --quality high --crf 20). El sonido
# de cada parte se recorta o rellena a la duración exacta de su vídeo antes de unirlo, para que no se desfase
# (el AAC añade unas muestras de cebado en cada archivo), y el total se iguala a −15 LUFS en dos pasadas.
# Escribe también los subtítulos del vídeo entero y la lista de capítulos con sus minutos.
set -euo pipefail

REPO="$(cd "$(dirname "$0")/../.." && pwd)"
AQUI="$REPO/videos/anticitera"
H="${HERRAMIENTAS:-$HOME/herramientas-videos}"
TRABAJO="${TRABAJO:-$REPO/salidas/anticitera}"
R="$TRABAJO/renders"
PARTES=(apertura cap1 cap2 cap3 cap4 cap5 cap6 cap7 cap8)
mkdir -p "$R"
paso() { printf '\n== %s (%s)\n' "$*" "$(date +%H:%M:%S)"; }

if [ "${1:-}" != "--unir" ]; then
  for p in "${PARTES[@]}"; do
    [ -s "$R/$p.mp4" ] && continue
    paso "Render de $p"
    (cd "$AQUI/$p" && "$REPO/video/hf.sh" render -o "$R/$p.mp4" --quality high --crf 20 --quiet)
  done
fi

paso "Unir la imagen (sin recomprimir) y el sonido (ajustado a cada parte)"
T="$R/union"
mkdir -p "$T"
: > "$T/lista.txt"
for p in "${PARTES[@]}"; do
  printf "file '%s'\n" "$R/$p.mp4" >> "$T/lista.txt"
  dur=$(ffprobe -v error -select_streams v:0 -count_packets -show_entries stream=nb_read_packets -of csv=p=0 "$R/$p.mp4")
  ffmpeg -v error -y -i "$R/$p.mp4" -vn -af "apad,atrim=end_sample=$((dur * 48000 / 30))" -ar 48000 -ac 2 "$T/$p.wav"
done
ffmpeg -v error -y -f concat -safe 0 -i "$T/lista.txt" -c copy -an "$T/imagen.mp4"
ffmpeg -v error -y -f concat -safe 0 -i <(for p in "${PARTES[@]}"; do printf "file '%s'\n" "$T/$p.wav"; done) -c copy "$T/sonido.wav"
ffmpeg -v error -y -i "$T/imagen.mp4" -i "$T/sonido.wav" -map 0:v -map 1:a -c:v copy -c:a pcm_s16le "$T/completo.mov"
"$REPO/video/entregar.sh" "$T/completo.mov" "$TRABAJO/anticitera.mp4" -15 copiar

paso "Subtítulos y capítulos"
python3 - "$AQUI" "$TRABAJO" "$R" "${PARTES[@]}" <<'EOF'
import json, os, subprocess, sys
aqui, trabajo, r, partes = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
sys.path.insert(0, aqui)
import subtitulos
guion = {c['id']: c for c in json.load(open(os.path.join(aqui, 'recursos', 'guion.json')))['capitulos']}
t, pares, lista = 0.0, [], []
for p in partes:
    frames = int(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_packets', '-show_entries',
                                 'stream=nb_read_packets', '-of', 'csv=p=0', os.path.join(r, p + '.mp4')],
                                capture_output=True, text=True, check=True).stdout)
    if p == 'apertura':
        pares.append((os.path.join(trabajo, 'audio', 'voz_ajustada.json'), t + 1.2))
        lista.append((t, 'Apertura: el hallazgo'))
    else:
        pares.append((os.path.join(trabajo, 'voz', p + '.json'), t + 3.4))
        lista.append((t, f"{guion[p]['numero']}. {guion[p]['titulo']}"))
    t += frames / 30
with open(os.path.join(aqui, 'subtitulos.srt'), 'w', encoding='utf-8') as f:
    f.write(subtitulos.srt(pares))
with open(os.path.join(aqui, 'capitulos.txt'), 'w', encoding='utf-8') as f:
    for ts, nombre in lista:
        f.write(f'{int(ts // 60)}:{int(ts % 60):02d} {nombre}\n')
print(f'duración total: {int(t // 60)} min {t % 60:.1f} s')
EOF
printf '\nListo en %d min %d s: %s\n' $((SECONDS / 60)) $((SECONDS % 60)) "$TRABAJO/anticitera.mp4"
