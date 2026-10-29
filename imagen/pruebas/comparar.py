"""
Compara modelos de FastSD con los prompts de prompts.json a través de
imagen/generar.py (el servidor local). Deja {etiqueta}_{prompt}.png y
resultados.jsonl en la carpeta actual, en el formato que lee hoja.py.

Uso, desde una carpeta de trabajo:
  python3 RUTA/imagen/pruebas/comparar.py flux3 flux2 sdxs
  python3 RUTA/imagen/pruebas/hoja.py comparativa.png "fastsd-flux3:FLUX.3 Image Klein|FastSD CPU" ...
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..'))
import generar  # noqa: E402

prompts = json.load(open(os.path.join(AQUI, 'prompts.json')))
generar.asegurar_servidor()
for modelo in sys.argv[1:] or ['flux3']:
    for nombre, texto in prompts.items():
        r = generar.generar(texto, f'fastsd-{modelo}_{nombre}.png', modelo=modelo)
        datos = {'etiqueta': f'fastsd-{modelo}', 'prompt': nombre, 'segundos': r['segundos'],
                 'incluye_carga': r['incluye_carga']}
        with open('resultados.jsonl', 'a') as f:
            f.write(json.dumps(datos) + '\n')
        print(json.dumps(datos), flush=True)
