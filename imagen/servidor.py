"""
Servidor local de imágenes: carga FastSD CPU una vez y genera imágenes PNG sin
pérdida bajo demanda. Lo arranca imagen/generar.py; no hace falta lanzarlo a mano.

Existe porque la API propia de FastSD devuelve JPEG con pérdida, y para vídeo
queremos el PNG original. Usa el mismo camino interno que esa API (Context +
LCMDiffusionSetting), así que depende de la versión de FastSD que fija
instalar.sh.

Se ejecuta con el Python del entorno de FastSD:
  $HERRAMIENTAS/fastsdcpu/env/bin/python imagen/servidor.py PUERTO
Escucha solo en 127.0.0.1 y genera una imagen cada vez (la CPU no da para más), pero contesta a
/estado mientras genera: si no, generar.py --parar no lo encontraba y lo dejaba encendido con 8–12 GB.
"""
import json
import os
import sys
import threading
import time
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

FASTSD = os.environ['FASTSD']
sys.path.insert(0, os.path.join(FASTSD, 'src'))
os.chdir(FASTSD)

from backend.models.lcmdiffusion_setting import LCMDiffusionSetting  # noqa: E402
from context import Context  # noqa: E402
from models.interface_types import InterfaceType  # noqa: E402
from state import get_settings  # noqa: E402

ajustes_app = get_settings()
contexto = Context(InterfaceType.API_SERVER)
modelo_cargado = None
una_a_una = threading.Lock()


class Manejador(BaseHTTPRequestHandler):
    def responder(self, codigo, datos):
        cuerpo = json.dumps(datos).encode()
        self.send_response(codigo)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

    def do_GET(self):
        if self.path == '/estado':
            self.responder(200, {'ok': True, 'modelo': modelo_cargado, 'pid': os.getpid()})
        else:
            self.responder(404, {'error': 'ruta desconocida'})

    def do_POST(self):
        if self.path != '/generar':
            self.responder(404, {'error': 'ruta desconocida'})
            return
        with una_a_una:
            self.generar()

    def generar(self):
        global modelo_cargado
        try:
            pedido = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
            ajustes_app.settings.lcm_diffusion_setting = LCMDiffusionSetting(
                use_openvino=True,
                openvino_lcm_model_id=pedido['modelo'],
                prompt=pedido['prompt'],
                image_width=pedido['ancho'],
                image_height=pedido['alto'],
                inference_steps=pedido['pasos'],
                guidance_scale=1.0,
                seed=pedido['semilla'],
                use_seed=True,
                use_tiny_auto_encoder=pedido['taesd'],
                number_of_images=1,
            )
            inicio = time.monotonic()
            imagenes = contexto.generate_text_to_image(ajustes_app.settings)
            if not imagenes:
                self.responder(500, {'error': contexto.error or 'FastSD no devolvió ninguna imagen'})
                return
            os.makedirs(os.path.dirname(os.path.abspath(pedido['salida'])), exist_ok=True)
            imagenes[0].save(pedido['salida'])
            carga = modelo_cargado != pedido['modelo']
            modelo_cargado = pedido['modelo']
            self.responder(200, {
                'salida': pedido['salida'],
                'segundos': round(time.monotonic() - inicio, 1),
                # La primera imagen de cada modelo incluye cargarlo y compilarlo.
                'incluye_carga': carga,
            })
        except Exception as e:
            traceback.print_exc()
            self.responder(500, {'error': f'{type(e).__name__}: {e}'})

    def log_message(self, formato, *args):
        pass


ThreadingHTTPServer(('127.0.0.1', int(sys.argv[1])), Manejador).serve_forever()
