#!/usr/bin/env bash
# HyperFrames con la configuración de este entorno: sin telemetría ni avisos de versión, con el
# Chromium de Playwright y con Node pasando por el proxy (lo necesitan transcribe y el registro).
# Se usa igual que el comando hyperframes, desde la carpeta del proyecto:
#   ../../video/hf.sh check --json
#   ../../video/hf.sh render -o salida.mp4
H="${HERRAMIENTAS:-$HOME/herramientas-videos}"
export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1 HYPERFRAMES_SKIP_SKILLS=1 NODE_USE_ENV_PROXY=1
if [ -z "${HYPERFRAMES_BROWSER_PATH:-}" ]; then
  HYPERFRAMES_BROWSER_PATH=$(ls -d /opt/pw-browsers/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell 2>/dev/null | sort -V | tail -1)
  export HYPERFRAMES_BROWSER_PATH
fi
exec "$H/hyperframes/node_modules/.bin/hyperframes" "$@"
