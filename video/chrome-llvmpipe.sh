#!/usr/bin/env bash
# chrome-headless-shell para HyperFrames con el WebGL en llvmpipe (Mesa) y el resto de la página
# dibujado y compuesto en la CPU, como con SwiftShader. Lo usa video/hf.sh, en modo «hardware»
# (PRODUCER_BROWSER_GPU_MODE), cuando está el EGL de Mesa (libegl-mesa0, ./instalar.sh edicion).
#
# Medido en la sesión 2 (Xeon de 4 núcleos sin AMX), 10 s a 1080p30 con 2 Chromium:
#   estilo A 70 s (SwiftShader 94 s), estilo B 114 s (138 s), solo texto 24 s (igual).
# La imagen es la misma salvo el dibujo del grano: el azar del shader usa sin(), que cada motor
# calcula a su manera (misma textura, otro patrón). Con todo en llvmpipe, también el texto y el
# CSS, el texto iba un 45 % más lento: por eso se quita la rasterización por GPU y se compone en la CPU.
real=$(ls -d /opt/pw-browsers/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell 2>/dev/null | sort -V | tail -1)
args=()
for a in "$@"; do
  case "$a" in
    --enable-gpu-rasterization|--disable-software-rasterizer) ;;
    *) args+=("$a") ;;
  esac
done
exec "$real" "${args[@]}" --disable-gpu-compositing
