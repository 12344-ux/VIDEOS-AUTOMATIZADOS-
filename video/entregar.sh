#!/usr/bin/env bash
# Versión de entrega de un vídeo: H.264 más ligero (el render de HyperFrames sale a CRF 16 y,
# con grano de película, pasa de 60 Mb/s) y el sonido normalizado a un volumen común, en dos
# pasadas de loudnorm, para que varios vídeos suenen igual de fuerte.
#   video/entregar.sh render.mp4 entrega.mp4 [LUFS] [CRF|copiar]   (por defecto −15 LUFS y CRF 20)
# Con «copiar», el vídeo pasa tal cual y solo se trata el sonido: es lo que conviene si el render ya
# salió con la calidad de entrega (hf.sh render --quality high --crf 20). Recomprimir es lo lento: con preset slow,
# 44 s por cada 10 s de vídeo en esta CPU (unos 40 min para 9 min); con medium, 27 s y la misma calidad.
# PICO cambia el pico real máximo (−1,5 dBTP por defecto; con −1,5 el AAC puede acabar en −0,9).
# GRAVES=-20 comprime la banda de subgraves (bajo 120 Hz, relación 4) antes de normalizar: los golpes de
# impact-bass son casi todo subgrave y, sin esto, subían 5 LU por encima de la voz (BusinessForMen, vídeo 1).
# loudnorm va con 3 s de silencio delante, que luego se quitan: en modo dinámico su limitador no alcanza el primer
# instante y un golpe en el fotograma 0 salía a +1,4 dBTP (corto 4 de BusinessForMen); con el silencio, −1,8.
# BUCLE=1 (un corto que se ve en bucle): el pico obliga a loudnorm a su modo dinámico, que sube lo flojo, y el final
# de un corto (la cola, con solo ambiente) quedaba 5–6 dB más alto que su principio: el bucle saltaba. Con BUCLE, el
# sonido se trata tres veces seguido y se queda el del medio: su principio y su final tienen el mismo contexto (el
# final y el principio del vídeo), reciben la misma ganancia y el bucle no salta (31-oct-2026).
set -euo pipefail
entrada=$1 salida=$2 lufs=${3:--15} crf=${4:-20} pico=${PICO:--1.5}
fuente=$entrada recorte="atrim=start=3,asetpts=PTS-STARTPTS"
previo="adelay=3000:all=1,"
if [ -n "${BUCLE:-}" ]; then
  tmp=$(mktemp -d)
  trap 'rm -rf "$tmp"' EXIT
  ffmpeg -hide_banner -v error -i "$entrada" -vn -ar 48000 -c:a pcm_f32le "$tmp/a.wav"
  n=$(ffprobe -v error -select_streams a:0 -show_entries stream=duration_ts -of csv=p=0 "$tmp/a.wav")
  ffmpeg -hide_banner -v error -i "$tmp/a.wav" -i "$tmp/a.wav" -i "$tmp/a.wav" \
    -filter_complex "[0:a][1:a][2:a]concat=n=3:v=0:a=1" -c:a pcm_f32le "$tmp/aaa.wav"
  fuente=$tmp/aaa.wav recorte="aresample=48000,atrim=start_sample=$n:end_sample=$((2 * n)),asetpts=PTS-STARTPTS" previo=""   # loudnorm sale a 192 kHz
fi
if [ -n "${GRAVES:-}" ]; then
  previo="acrossover=split=120:order=4th[g][r];[g]acompressor=threshold=${GRAVES}dB:ratio=4:attack=10:release=300[gc];[gc][r]amix=inputs=2:normalize=0,$previo"
fi
medida=$(ffmpeg -hide_banner -nostats -i "$fuente" -vn -af "${previo}loudnorm=I=$lufs:TP=$pico:LRA=11:print_format=json" -f null - 2>&1 \
  | sed -n '/^{/,/^}/p')
valor() { echo "$medida" | python3 -c "import json,sys; print(json.load(sys.stdin)['$1'])"; }
filtro="${previo}loudnorm=I=$lufs:TP=$pico:LRA=11:measured_I=$(valor input_i):measured_TP=$(valor input_tp)"
filtro="$filtro:measured_LRA=$(valor input_lra):measured_thresh=$(valor input_thresh):offset=$(valor target_offset):linear=true,$recorte"
if [ "$crf" = copiar ]; then
  video=(-c:v copy)
else
  video=(-c:v libx264 -preset medium -crf "$crf" -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709)
fi
ffmpeg -hide_banner -v error -y -i "$entrada" -i "$fuente" -map 0:v:0 -map 1:a:0 "${video[@]}" -af "$filtro,aresample=48000" \
  -c:a aac -b:a 192k -movflags +faststart "$salida"
final=$(ffmpeg -hide_banner -nostats -i "$salida" -vn -af ebur128=peak=true -f null - 2>&1 | grep -A20 Summary)
echo "$salida: $(du -h "$salida" | cut -f1),$(echo "$final" | grep ' I:' | tr -s ' '), pico real$(echo "$final" | grep 'Peak:' | tail -1 | tr -s ' ' | cut -d: -f2)"
