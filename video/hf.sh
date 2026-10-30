#!/usr/bin/env bash
# HyperFrames con la configuración de este entorno: sin telemetría ni avisos de versión, con el
# Chromium de Playwright y con Node pasando por el proxy (lo necesitan transcribe y el registro).
# Se usa igual que el comando hyperframes, desde la carpeta del proyecto:
#   ../../video/hf.sh check --json
#   ../../video/hf.sh render -o salida.mp4 --quality high --crf 20   (preset fast: misma calidad que medium)
# Si está el EGL de Mesa, el WebGL va por llvmpipe en vez de SwiftShader (video/chrome-llvmpipe.sh:
# el estilo A renderiza un 26 % más rápido). HF_SWIFTSHADER=1 vuelve a SwiftShader.
H="${HERRAMIENTAS:-$HOME/herramientas-videos}"
AQUI="$(cd "$(dirname "$0")" && pwd)"
export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1 HYPERFRAMES_SKIP_SKILLS=1 NODE_USE_ENV_PROXY=1
if [ -z "${HYPERFRAMES_BROWSER_PATH:-}" ]; then
  if [ -z "${HF_SWIFTSHADER:-}" ] && ldconfig -p 2>/dev/null | grep -q libEGL_mesa; then
    HYPERFRAMES_BROWSER_PATH="$AQUI/chrome-llvmpipe.sh"
    export PRODUCER_BROWSER_GPU_MODE="${PRODUCER_BROWSER_GPU_MODE:-hardware}"
  else
    HYPERFRAMES_BROWSER_PATH=$(ls -d /opt/pw-browsers/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell 2>/dev/null | sort -V | tail -1)
  fi
  export HYPERFRAMES_BROWSER_PATH
fi
# En render, 2 Chromium por cada 4 núcleos si no se pide otro número: la calibración automática mide
# un primer cuadro lento y se queda en 1 (estilo A: 85 s frente a 70 s con 2; con 3 o 4 no mejora).
if [ "${1:-}" = render ] && ! printf '%s\n' "$@" | grep -qE '^(-w|--workers)(=|$)|^-w[0-9]'; then
  n=$(( $(nproc) / 2 ))
  set -- "$@" --workers "$(( n > 0 ? n : 1 ))"
fi
exec "$H/hyperframes/node_modules/.bin/hyperframes" "$@"
