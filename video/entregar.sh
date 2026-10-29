#!/usr/bin/env bash
# Versión de entrega de un vídeo: H.264 más ligero (el render de HyperFrames sale a CRF 16 y,
# con grano de película, pasa de 60 Mb/s) y el sonido normalizado a un volumen común, en dos
# pasadas de loudnorm, para que varios vídeos suenen igual de fuerte.
#   video/entregar.sh render.mp4 entrega.mp4 [LUFS] [CRF]     (por defecto −15 LUFS y CRF 20)
set -euo pipefail
entrada=$1 salida=$2 lufs=${3:--15} crf=${4:-20}
medida=$(ffmpeg -hide_banner -nostats -i "$entrada" -af "loudnorm=I=$lufs:TP=-1.5:LRA=11:print_format=json" -f null - 2>&1 \
  | sed -n '/^{/,/^}/p')
valor() { echo "$medida" | python3 -c "import json,sys; print(json.load(sys.stdin)['$1'])"; }
filtro="loudnorm=I=$lufs:TP=-1.5:LRA=11:measured_I=$(valor input_i):measured_TP=$(valor input_tp)"
filtro="$filtro:measured_LRA=$(valor input_lra):measured_thresh=$(valor input_thresh):offset=$(valor target_offset):linear=true"
ffmpeg -hide_banner -v error -y -i "$entrada" -c:v libx264 -preset slow -crf "$crf" -pix_fmt yuv420p \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 -af "$filtro,aresample=48000" \
  -c:a aac -b:a 192k -movflags +faststart "$salida"
final=$(ffmpeg -hide_banner -nostats -i "$salida" -af ebur128=peak=true -f null - 2>&1 | grep -A20 Summary)
echo "$salida: $(du -h "$salida" | cut -f1),$(echo "$final" | grep ' I:' | tr -s ' '), pico real$(echo "$final" | grep 'Peak:' | tail -1 | tr -s ' ' | cut -d: -f2)"
