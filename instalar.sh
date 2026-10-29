#!/usr/bin/env bash
# Instala las herramientas del proyecto FUERA del repositorio, en $HERRAMIENTAS
# (por defecto ~/herramientas-videos), porque pesan varios GB y no caben en git.
# Se puede repetir sin miedo: salta lo que ya está instalado.
#
#   ./instalar.sh                voz + imagen + edicion: lo necesario para hacer vídeos
#   ./instalar.sh voz            Piper y las voces en español
#   ./instalar.sh imagen         FastSD CPU (OpenVINO) con FLUX.3 Image Klein y SDXS
#   ./instalar.sh edicion        HyperFrames y los modelos de apoyo: profundidad (2.5D),
#                                recortes y música (necesita voz e imagen)
#   ./instalar.sh imagen-extra   además FLUX.2 klein 4B (licencia Apache 2.0)
#   ./instalar.sh sdcpp          stable-diffusion.cpp y sus modelos (opcional; aquí es lento)
#   ./instalar.sh comprobar      dice qué hay y qué falta, sin instalar nada
#
# Versiones fijadas: son las que se probaron y midieron el 29 de octubre de 2026.
set -euo pipefail

H="${HERRAMIENTAS:-$HOME/herramientas-videos}"
export HF_HOME="$H/hf" HF_HUB_DISABLE_TELEMETRY=1
export PATH="$HOME/.local/bin:$PATH"

HF=https://huggingface.co
FASTSD_REPO=https://github.com/rupeshs/fastsdcpu
FASTSD_COMMIT=0f64fd45cecd7fbac2a60540840f5f1d3141e229
SDCPP_REPO=https://github.com/leejet/stable-diffusion.cpp
SDCPP_COMMIT=37bc88b5e97a213821949732ea66c58ae8ffc784
PIPER_VERSION=1.8.0
HYPERFRAMES_VERSION=0.8.216
# Modelos de apoyo a la edición (Hugging Face): profundidad, recortes y música.
EXTRA_PROFUNDIDAD=onnx-community/depth-anything-v2-small
EXTRA_RECORTE=onnx-community/BiRefNet_lite-ONNX
EXTRA_MUSICA=facebook/musicgen-stereo-small
VOCES=(es/es_AR/daniela/high/es_AR-daniela-high es/es_MX/claude/high/es_MX-claude-high)
# Repositorio de Hugging Face y GB que ocupa.
MODELOS_IMAGEN=(rupeshs/flux3-image-klein-int4-ov:6 rupeshs/sdxs-512-0.9-openvino:3 rupeshs/taesd-ov:1)
MODELO_EXTRA=rupeshs/flux2-klein-4b-int4-ov:5
FLUX2_GGUF=manishdashsharma/flux2-klein-4b-gguf

paso() { printf '\n== %s\n' "$*"; }
falla() { printf '\nERROR: %s\n' "$*" >&2; exit 1; }

# Descarga reanudable; no hace nada si el archivo ya está.
bajar() {
  [ -s "$2" ] && return 0
  mkdir -p "$(dirname "$2")"
  echo "  bajando $(basename "$2")"
  curl -fsSL --retry 5 --retry-delay 3 -C - -o "$2.parcial" "$1"
  mv "$2.parcial" "$2"
}

comprobar_red() {
  curl -fsS -m 20 -o /dev/null "$HF/api/models/${MODELO_EXTRA%%:*}" \
    || falla "No llego a huggingface.co. Añádelo en la red del entorno (Allowed domains)."
  # Los archivos grandes salen de la CDN de Hugging Face, que es otro dominio.
  curl -fsSL -m 30 -r 0-1023 -o /dev/null "$HF/rhasspy/piper-voices/resolve/main/${VOCES[0]}.onnx" \
    || falla "huggingface.co responde pero su CDN no. Añade *.hf.co (o us.aws.cdn.hf.co) en Allowed domains."
}

comprobar_disco() {
  local libre
  libre=$(df -BG --output=avail "$HOME" | tail -1 | tr -dc 0-9)
  [ "$libre" -ge "$1" ] || falla "Hacen falta unos $1 GB libres y hay $libre GB."
}

python311() {
  command -v python3.11 && return 0
  uv python find 3.11 2>/dev/null && return 0
  uv python install 3.11 >&2 && uv python find 3.11
}

en_cache() {
  "$H/fastsdcpu/env/bin/python" -c \
    "import sys; from huggingface_hub import snapshot_download as s; s(sys.argv[1], local_files_only=True)" "$1" >/dev/null 2>&1
}

# modelo_hf REPO GB: descarga un modelo de Hugging Face si no está ya en la caché.
modelo_hf() {
  en_cache "$1" && return 0
  comprobar_disco "$2"
  "$H/fastsdcpu/env/bin/python" -c \
    "import sys; from huggingface_hub import snapshot_download; snapshot_download(sys.argv[1])" "$1" >/dev/null
}

# Clona un repositorio en un commit exacto, sin historial.
clonar_en() {
  [ -d "$1/.git" ] && return 0
  git init -q "$1"
  git -C "$1" fetch -q --depth 1 "$2" "$3"
  git -C "$1" checkout -q FETCH_HEAD
}

instalar_voz() {
  paso "Voz: Piper $PIPER_VERSION y voces en español"
  if ! "$H/piper/bin/python" -c 'import piper' 2>/dev/null; then
    [ -e "$H/piper" ] && falla "$H/piper existe pero no funciona; bórralo y vuelve a ejecutar."
    comprobar_disco 1
    command -v uv >/dev/null || python3 -m pip install --user -q uv
    uv venv -q --python "$(command -v python3)" "$H/piper"
    uv pip install -q --python "$H/piper/bin/python" "piper-tts==$PIPER_VERSION" numpy
  fi
  for v in "${VOCES[@]}"; do
    for ext in onnx onnx.json; do
      bajar "$HF/rhasspy/piper-voices/resolve/main/$v.$ext" "$H/voces/$(basename "$v").$ext"
    done
  done
}

instalar_imagen() {
  paso "Imagen: FastSD CPU (commit ${FASTSD_COMMIT:0:7}) con OpenVINO"
  clonar_en "$H/fastsdcpu" "$FASTSD_REPO" "$FASTSD_COMMIT"
  if ! "$H/fastsdcpu/env/bin/python" -c 'import openvino, diffusers, optimum.intel' 2>/dev/null; then
    [ -e "$H/fastsdcpu/env" ] && falla "$H/fastsdcpu/env existe pero no funciona; bórralo y vuelve a ejecutar."
    comprobar_disco 4
    command -v uv >/dev/null || python3 -m pip install --user -q uv
    # FastSD fija versiones (numpy 1.26, Pillow 9.4) que solo existen hasta Python 3.11.
    uv venv -q --python "$(python311)" "$H/fastsdcpu/env"
    uv pip install -q --python "$H/fastsdcpu/env/bin/python" torch==2.8.0 torchvision==0.23.0 \
      --index-url https://download.pytorch.org/whl/cpu
    # Igual que su install.sh --disable-gui: todo menos la interfaz de escritorio (PyQt5).
    local requisitos="$H/requisitos-fastsd.txt"
    grep -v '^ *#\|^PyQt5' "$H/fastsdcpu/requirements.txt" | grep . > "$requisitos"
    uv pip install -q --python "$H/fastsdcpu/env/bin/python" -r "$requisitos"
  fi
  paso "Imagen: modelos (${MODELOS_IMAGEN[*]%%:*})"
  for m in "${MODELOS_IMAGEN[@]}"; do modelo_hf "${m%%:*}" "${m##*:}"; done
}

instalar_imagen_extra() {
  paso "Imagen: FLUX.2 klein 4B INT4 (Apache 2.0)"
  modelo_hf "${MODELO_EXTRA%%:*}" "${MODELO_EXTRA##*:}"
}

instalar_sdcpp() {
  paso "stable-diffusion.cpp (commit ${SDCPP_COMMIT:0:7}), compilado para esta CPU"
  if [ ! -x "$H/sdcpp/build/bin/sd-cli" ]; then
    comprobar_disco 2
    clonar_en "$H/sdcpp" "$SDCPP_REPO" "$SDCPP_COMMIT"
    git -C "$H/sdcpp" submodule update -q --init --recursive --depth 1
    cmake -S "$H/sdcpp" -B "$H/sdcpp/build" -DCMAKE_BUILD_TYPE=Release -DGGML_NATIVE=ON >/dev/null
    cmake --build "$H/sdcpp/build" --config Release -j "$(nproc)" >/dev/null
  fi
  paso "stable-diffusion.cpp: FLUX.2 klein 4B (GGUF) y SDXS"
  local m="$H/modelos/flux2-klein"
  [ -s "$m/Qwen3-4B-Q4_K_S.gguf" ] || comprobar_disco 6
  for f in flux2-vae.safetensors flux-2-klein-4b-q4_0.gguf Qwen3-4B-Q4_K_S.gguf SHA256SUMS.txt; do
    bajar "$HF/$FLUX2_GGUF/resolve/main/$f" "$m/$f"
  done
  (cd "$m" && grep -E 'q4_0.gguf|Q4_K_S.gguf|vae.safetensors' SHA256SUMS.txt | sha256sum -c --quiet -) \
    || falla "Las sumas SHA256 de FLUX.2 klein no coinciden; borra $m y repite."
  bajar "$HF/akleine/sdxs-512/resolve/main/sdxs.safetensors" "$H/modelos/sdxs/sdxs.safetensors"
}

instalar_edicion() {
  paso "Edición: HyperFrames $HYPERFRAMES_VERSION (vídeo hecho con HTML y GSAP)"
  if [ ! -x "$H/hyperframes/node_modules/.bin/hyperframes" ]; then
    comprobar_disco 1
    mkdir -p "$H/hyperframes"
    [ -f "$H/hyperframes/package.json" ] || echo '{"private": true}' > "$H/hyperframes/package.json"
    (cd "$H/hyperframes" && HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_SKIP_SKILLS=1 PUPPETEER_SKIP_DOWNLOAD=1 \
      npm install --silent --no-fund --no-audit "hyperframes@$HYPERFRAMES_VERSION" >/dev/null)
  fi
  [ -x "$H/fastsdcpu/env/bin/python" ] || falla "Falta ./instalar.sh imagen: su Python ejecuta estos modelos."
  paso "Edición: Depth Anything V2 Small, BiRefNet lite y MusicGen estéreo"
  local e="$H/extra" f
  for f in onnx/model.onnx config.json preprocessor_config.json; do
    bajar "$HF/$EXTRA_PROFUNDIDAD/resolve/main/$f" "$e/depth-anything-v2-small/$(basename "$f")"
    bajar "$HF/$EXTRA_RECORTE/resolve/main/$f" "$e/birefnet-lite/$(basename "$f")"
  done
  [ -s "$e/musicgen-stereo-small/model.safetensors" ] || comprobar_disco 2
  for f in config.json generation_config.json preprocessor_config.json special_tokens_map.json \
    tokenizer.json tokenizer_config.json model.safetensors; do
    bajar "$HF/$EXTRA_MUSICA/resolve/main/$f" "$e/musicgen-stereo-small/$f"
  done
  if [ -x "$H/piper/bin/python" ] && ! "$H/piper/bin/python" -c 'import onnx' 2>/dev/null; then
    paso "Voz: paquete onnx, para sacar el tiempo de cada palabra"
    uv pip install -q --python "$H/piper/bin/python" onnx
  fi
}

comprobar() {
  estado() { if eval "$2" >/dev/null 2>&1; then printf '  ok     %s\n' "$1"; else printf '  falta  %s\n' "$1"; fi; }
  local py="$H/fastsdcpu/env/bin/python"
  echo "Herramientas en $H"
  estado "Piper (voz)" "'$H/piper/bin/python' -c 'import piper'"
  for v in "${VOCES[@]}"; do estado "voz $(basename "$v")" "test -s '$H/voces/$(basename "$v").onnx'"; done
  estado "FastSD CPU (imagen)" "'$py' -c 'import openvino, diffusers, optimum.intel'"
  for m in "${MODELOS_IMAGEN[@]%%:*}" "${MODELO_EXTRA%%:*}"; do
    estado "modelo $m" "'$py' -c \"from huggingface_hub import snapshot_download as s; s('$m', local_files_only=True)\""
  done
  estado "HyperFrames (edición)" "test -x '$H/hyperframes/node_modules/.bin/hyperframes'"
  estado "Depth Anything V2 Small (2.5D)" "test -s '$H/extra/depth-anything-v2-small/model.onnx'"
  estado "BiRefNet lite (recortes)" "test -s '$H/extra/birefnet-lite/model.onnx'"
  estado "MusicGen estéreo small (música)" "test -s '$H/extra/musicgen-stereo-small/model.safetensors'"
  estado "onnx en Piper (tiempo de cada palabra)" "'$H/piper/bin/python' -c 'import onnx'"
  estado "stable-diffusion.cpp (opcional)" "test -x '$H/sdcpp/build/bin/sd-cli'"
  estado "Chromium de Playwright (vídeo)" "node -e \"require('playwright')\""
  estado "ffmpeg (vídeo)" "command -v ffmpeg"
  echo "Disco libre: $(df -h --output=avail "$HOME" | tail -1 | tr -d ' ')"
}

mkdir -p "$H"
componentes=("${@:-voz imagen edicion}")
read -r -a componentes <<< "${componentes[*]}"
for c in "${componentes[@]}"; do
  case "$c" in
    comprobar) comprobar; exit 0 ;;
    voz) comprobar_red; instalar_voz ;;
    imagen) comprobar_red; instalar_imagen ;;
    imagen-extra) comprobar_red; [ -x "$H/fastsdcpu/env/bin/python" ] || instalar_imagen; instalar_imagen_extra ;;
    edicion) comprobar_red; instalar_edicion ;;
    sdcpp) comprobar_red; instalar_sdcpp ;;
    *) falla "Componente desconocido: $c (usa voz, imagen, edicion, imagen-extra, sdcpp o comprobar)" ;;
  esac
done
printf '\nListo en %d min %d s.\n' $((SECONDS / 60)) $((SECONDS % 60))
comprobar
