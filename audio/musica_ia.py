"""
Música de fondo generada en local con MusicGen (Meta, licencia CC BY-NC 4.0: solo uso
no comercial). Escribe un WAV estéreo a 32 kHz a partir de una descripción en inglés.

Se ejecuta con el Python del entorno de FastSD (trae torch y transformers):
  PY=$HERRAMIENTAS/fastsdcpu/env/bin/python
  $PY audio/musica_ia.py "slow cinematic ambient, soft piano, 70 bpm" -o musica.wav --duracion 12

Consejos medidos aquí: describir sensación, instrumentos y tempo, no el tema del vídeo;
pedir 1–2 s más de lo necesario porque el final suele cortarse en seco. No cargarlo a
la vez que el servidor de imágenes: entre los dos se acaba la RAM.

Varias descripciones salen en lotes (--lote, 4 por defecto): cuatro pistas de 10 s a la vez
tardaron 123 s, frente a 53,5 s una sola (1,7 veces más rápido por pista). Por eso conviene
pedir todas las piezas de un vídeo en la misma llamada.
"""
import argparse
import os
import time
import wave

import numpy as np
import torch
from transformers import AutoProcessor, MusicgenForConditionalGeneration

HERRAMIENTAS = os.environ.get('HERRAMIENTAS', os.path.expanduser('~/herramientas-videos'))
MODELO = os.path.join(HERRAMIENTAS, 'extra', 'musicgen-stereo-small')
TOKENS_POR_SEGUNDO = 50


def main():
    p = argparse.ArgumentParser(description='Música de fondo con MusicGen.')
    p.add_argument('descripcion', nargs='+', help='una o varias descripciones (una pista por cada una)')
    p.add_argument('-o', '--salida', default='musica.wav', help='con varias descripciones se numeran: musica_1.wav…')
    p.add_argument('--duracion', type=float, default=12)
    p.add_argument('--semilla', type=int, default=1)
    p.add_argument('--guia', type=float, default=3.0, help='cuánto se ciñe a la descripción')
    p.add_argument('--lote', type=int, default=4, help='pistas que se generan a la vez')
    args = p.parse_args()

    torch.set_num_threads(os.cpu_count())
    inicio = time.time()
    procesador = AutoProcessor.from_pretrained(MODELO)
    modelo = MusicgenForConditionalGeneration.from_pretrained(MODELO, torch_dtype=torch.float32).eval()
    carga = time.time() - inicio
    sr = modelo.config.audio_encoder.sampling_rate

    for desde in range(0, len(args.descripcion), args.lote):
        grupo = args.descripcion[desde:desde + args.lote]
        torch.manual_seed(args.semilla + desde)
        t = time.time()
        entrada = procesador(text=grupo, padding=True, return_tensors='pt')
        with torch.inference_mode():
            audio = modelo.generate(**entrada, do_sample=True, guidance_scale=args.guia,
                                    max_new_tokens=int(args.duracion * TOKENS_POR_SEGUNDO))
        segundos = time.time() - t
        for j in range(len(grupo)):
            salida = args.salida
            if len(args.descripcion) > 1:
                base, ext = os.path.splitext(args.salida)
                salida = f'{base}_{desde + j + 1}{ext}'
            x = audio[j].float().numpy()            # (canales, muestras)
            x = x / max(np.max(np.abs(x)), 1e-6) * 0.89  # pico a −1 dBFS
            with wave.open(salida, 'wb') as w:
                w.setnchannels(x.shape[0])
                w.setsampwidth(2)
                w.setframerate(sr)
                w.writeframes((x.T * 32767).astype('<i2').tobytes())
            print(f'{salida}  {x.shape[1] / sr:.1f} s de audio, {len(grupo)} a la vez en {segundos:.0f} s '
                  f'(carga {carga:.0f} s)')


if __name__ == '__main__':
    main()
