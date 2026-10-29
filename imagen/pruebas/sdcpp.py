"""
Prueba un modelo con sd-cli (stable-diffusion.cpp) sobre los prompts de
prompts.json, a 512 px y semilla 42, y anota tiempo y RAM máxima de cada proceso.

Uso: python3 sdcpp.py ETIQUETA -- argumentos de sd-cli para el modelo
Ejemplo (FLUX.2 klein 4B; ./instalar.sh sdcpp descarga estos archivos):
  M=~/herramientas-videos/modelos/flux2-klein
  python3 sdcpp.py sdcpp-flux2klein -- --diffusion-model $M/flux-2-klein-4b-q4_0.gguf \
    --llm $M/Qwen3-4B-Q4_K_S.gguf --vae $M/flux2-vae.safetensors --cfg-scale 1.0 --steps 4
Deja las imágenes y los registros en la carpeta actual.
"""
import json
import os
import re
import subprocess
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.getcwd()
HERRAMIENTAS = os.environ.get('HERRAMIENTAS', os.path.expanduser('~/herramientas-videos'))
SD_CLI = os.path.join(HERRAMIENTAS, 'sdcpp', 'build', 'bin', 'sd-cli')
etiqueta = sys.argv[1]
extra = sys.argv[sys.argv.index('--') + 1:]
prompts = json.load(open(os.path.join(AQUI, 'prompts.json')))

for nombre, texto in prompts.items():
    base = os.path.join(SALIDA, f'{etiqueta}_{nombre}')
    with open(base + '.log', 'w') as registro:
        inicio = time.monotonic()
        proceso = subprocess.Popen(
            [SD_CLI, *extra, '-p', texto, '-o', base + '.png',
             '-W', '512', '-H', '512', '-s', '42', '-t', '4', '-v'],
            stdout=registro, stderr=subprocess.STDOUT,
        )
        # wait4 da el uso de recursos de este proceso en concreto.
        _, estado, uso = os.wait4(proceso.pid, 0)
        total = round(time.monotonic() - inicio, 1)
    log = open(base + '.log', errors='replace').read()
    datos = {
        'etiqueta': etiqueta, 'prompt': nombre, 'segundos': total,
        'ram_pico_gb': round(uso.ru_maxrss / 1024 / 1024, 2),
        'codigo': os.waitstatus_to_exitcode(estado),
        # Las líneas de tiempos internos de sd-cli (carga, muestreo, decodificación).
        'detalle': [l.strip()[-110:] for l in log.splitlines()
                    if re.search(r'(taking|completed|loaded in|load.*\d+\.\d+ ?s)', l)][-8:],
        'incluye_carga': True,
    }
    with open(os.path.join(SALIDA, 'resultados.jsonl'), 'a') as f:
        f.write(json.dumps(datos) + '\n')
    print(json.dumps({k: v for k, v in datos.items() if k != 'detalle'}), flush=True)
    for linea in datos['detalle']:
        print('   ', linea)
    if datos['codigo'] != 0:
        sys.exit(f'sd-cli falló con {nombre}; mira {base}.log')
