"""
Genera imágenes a partir de un prompt con FastSD CPU (OpenVINO), en local.

La primera llamada arranca imagen/servidor.py en segundo plano y lo deja con el
modelo cargado, así las siguientes imágenes no pagan la carga.

Uso:
  python3 imagen/generar.py "a red fox in the snow, digital illustration" -o zorro.png
  python3 imagen/generar.py "..." -o x.png --modelo sdxs        # boceto en medio segundo
  python3 imagen/generar.py --lote escenas.json                 # varias de una vez
  python3 imagen/generar.py --parar                             # apaga el servidor

escenas.json es una lista de objetos con "prompt" y "salida", y opcionalmente
"modelo", "ancho", "alto" y "semilla".

Escribe una línea JSON por imagen con la ruta y los segundos que tardó.
Los prompts funcionan mejor en inglés y descriptivos (sujeto, lugar, luz, estilo).
"""
import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request

HERRAMIENTAS = os.environ.get('HERRAMIENTAS', os.path.expanduser('~/herramientas-videos'))
FASTSD = os.path.join(HERRAMIENTAS, 'fastsdcpu')
PUERTO = int(os.environ.get('PUERTO_IMAGEN', '8124'))
AQUI = os.path.dirname(os.path.abspath(__file__))

# Modelo de OpenVINO, pasos y si usa el decodificador rápido TAESD.
# Tiempos medidos en el Xeon de 4 núcleos del entorno, 512 px, con el modelo cargado.
MODELOS = {
    'flux3': ('rupeshs/flux3-image-klein-int4-ov', 4, False),  # ~37 s, la mejor calidad
    'flux2': ('rupeshs/flux2-klein-4b-int4-ov', 4, False),     # ~40 s, licencia Apache 2.0
    'sdxs': ('rupeshs/sdxs-512-0.9-openvino', 1, True),         # ~0,5 s, bocetos; solo 512x512
}


def pedir(ruta, datos=None, espera=10):
    req = urllib.request.Request(
        f'http://127.0.0.1:{PUERTO}{ruta}',
        data=json.dumps(datos).encode() if datos is not None else None,
        headers={'Content-Type': 'application/json'},
    )
    try:
        with urllib.request.urlopen(req, timeout=espera) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        return json.load(e)


def servidor_activo():
    try:
        return pedir('/estado', espera=3).get('ok')
    except OSError:
        return False


def asegurar_servidor():
    if servidor_activo():
        return
    python = os.path.join(FASTSD, 'env', 'bin', 'python')
    if not os.path.exists(python):
        sys.exit(f'FastSD CPU no está instalado en {FASTSD}. Ejecuta: ./instalar.sh imagen')
    registro = open(os.path.join(HERRAMIENTAS, 'servidor-imagen.log'), 'a')
    entorno = dict(os.environ, FASTSD=FASTSD, HF_HOME=os.path.join(HERRAMIENTAS, 'hf'),
                   HF_HUB_DISABLE_TELEMETRY='1')
    proceso = subprocess.Popen(
        [python, os.path.join(AQUI, 'servidor.py'), str(PUERTO)],
        env=entorno, stdout=registro, stderr=subprocess.STDOUT, start_new_session=True,
    )
    for _ in range(240):
        if servidor_activo():
            return
        if proceso.poll() is not None:
            sys.exit(f'El servidor de imágenes se cerró al arrancar; mira {registro.name}')
        time.sleep(0.5)
    sys.exit(f'El servidor de imágenes no respondió en 2 minutos; mira {registro.name}')


def generar(prompt, salida, modelo='flux3', ancho=512, alto=512, semilla=42):
    if modelo not in MODELOS:
        sys.exit(f'Modelo desconocido: {modelo}. Usa uno de: {", ".join(MODELOS)}')
    if ancho % 16 or alto % 16:
        sys.exit('El ancho y el alto tienen que ser múltiplos de 16')
    id_modelo, pasos, taesd = MODELOS[modelo]
    respuesta = pedir('/generar', {
        'prompt': prompt, 'salida': os.path.abspath(salida), 'modelo': id_modelo,
        'pasos': pasos, 'taesd': taesd, 'ancho': ancho, 'alto': alto, 'semilla': semilla,
    }, espera=3600)
    if 'error' in respuesta:
        sys.exit(f'Error generando {salida}: {respuesta["error"]}')
    return dict(respuesta, modelo=modelo)


def main():
    p = argparse.ArgumentParser(description='Genera imágenes en local con FastSD CPU.')
    p.add_argument('prompt', nargs='?')
    p.add_argument('-o', '--salida', default='imagen.png')
    p.add_argument('--modelo', default='flux3', choices=list(MODELOS))
    p.add_argument('--ancho', type=int, default=512)
    p.add_argument('--alto', type=int, default=512)
    p.add_argument('--semilla', type=int, default=42)
    p.add_argument('--lote', help='JSON con una lista de {"prompt", "salida", ...}')
    p.add_argument('--parar', action='store_true', help='apaga el servidor de imágenes')
    args = p.parse_args()

    if args.parar:
        if servidor_activo():
            os.kill(pedir('/estado')['pid'], 15)
            print('servidor de imágenes apagado')
        return
    if args.lote:
        pedidos = json.load(open(args.lote))
    elif args.prompt:
        pedidos = [{'prompt': args.prompt, 'salida': args.salida}]
    else:
        p.error('falta el prompt o --lote')

    asegurar_servidor()
    for pedido in pedidos:
        resultado = generar(
            pedido['prompt'], pedido['salida'],
            modelo=pedido.get('modelo', args.modelo),
            ancho=pedido.get('ancho', args.ancho), alto=pedido.get('alto', args.alto),
            semilla=pedido.get('semilla', args.semilla),
        )
        print(json.dumps(resultado, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
