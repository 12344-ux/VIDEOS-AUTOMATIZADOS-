#!/usr/bin/env bash
# Las dos miniaturas del vídeo 1 (miniatura/index.html), a 1280 × 720, en salidas/businessformen/01-flujo-de-caja/entrega/.
#   canales/businessformen/videos/01-flujo-de-caja/miniatura.sh
set -euo pipefail
REPO="$(cd "$(dirname "$0")/../../../.." && pwd)"
AQUI="$REPO/canales/businessformen/videos/01-flujo-de-caja"
T="$REPO/salidas/businessformen/01-flujo-de-caja"
mkdir -p "$AQUI/miniatura/assets/fonts" "$AQUI/miniatura/assets/img" "$T/entrega"
cp "$REPO/salidas/businessformen/marca/fuentes/"{intertight-800,plexmono-500}.woff2 "$AQUI/miniatura/assets/fonts/"
cp "$T/img/grant-cerrada.jpg" "$AQUI/miniatura/assets/img/"
cd "$AQUI/miniatura"
rm -rf "$T/miniaturas"
"$REPO/video/hf.sh" snapshot --at 0.5,1.5 --no-end -o "$T/miniaturas" >/dev/null 2>&1
python3 - "$T" <<'EOF'
import glob, sys
from PIL import Image
t = sys.argv[1]
for f, n in zip(sorted(glob.glob(t + '/miniaturas/frame-*.png')), 'ab'):
    Image.open(f).convert('RGB').resize((1280, 720), Image.LANCZOS).save(f'{t}/entrega/miniatura-{n}.jpg', quality=92)
    print(f'{t}/entrega/miniatura-{n}.jpg')
EOF
