"""
Mezcla la narración con la música: la música baja cuando habla la voz y el
resultado se ajusta al volumen estándar de las plataformas (−14 LUFS por defecto).

Uso:
  python3 audio/mezclar.py --voz narracion.wav --musica musica.wav -o mezcla.wav
  python3 audio/mezclar.py --voz narracion.wav --musica musica.wav -o mezcla.wav --nivel-musica 0.4 --cola 3

La duración final es la de la voz más --cola segundos (2 por defecto); la música
se recorta con un fundido. Con el agache por defecto la voz queda unos 10 dB por
encima de la música (medido en el anuncio de prueba de la primera sesión).
"""
import argparse
import json
import os
import re
import subprocess
import tempfile
import wave

import numpy as np

SR = 48000


def leer(ruta):
    with wave.open(ruta, 'rb') as w:
        if w.getframerate() != SR or w.getsampwidth() != 2:
            raise SystemExit(f'{ruta}: hace falta WAV de 16 bits a 48 kHz')
        x = np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(float) / 32768
        return x.reshape(-1, w.getnchannels()).T


def agachar(musica, voz, cuanto=0.65):
    """Baja la música mientras suena la voz: ataque de 8 ms y liberación de 180 ms, en bloques de 1 ms."""
    bloque = SR // 1000
    n = len(voz) // bloque * bloque
    picos = np.abs(voz[:n]).reshape(-1, bloque).max(axis=1)
    nivel, envolvente = 0.0, np.zeros_like(picos)
    for i, p in enumerate(picos):
        nivel += (p - nivel) * (1 - np.exp(-1 / 8)) if p > nivel else -nivel * (1 - np.exp(-1 / 180))
        envolvente[i] = nivel
    ganancia = np.ones(musica.shape[1])
    ganancia[:n] = np.repeat(1 - cuanto * np.clip(envolvente / 0.15, 0, 1), bloque)
    return musica * ganancia


def normalizar_volumen(entrada, salida, lufs, pico=-1.5):
    """loudnorm de ffmpeg en dos pasadas (la segunda, lineal) para no alterar la dinámica."""
    filtro = f'loudnorm=I={lufs}:TP={pico}:LRA=11'
    medida = subprocess.run(['ffmpeg', '-hide_banner', '-i', entrada, '-af', filtro + ':print_format=json',
                             '-f', 'null', '-'], capture_output=True, text=True).stderr
    m = json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}', medida)[-1])
    filtro += (f':measured_I={m["input_i"]}:measured_TP={m["input_tp"]}:measured_LRA={m["input_lra"]}'
               f':measured_thresh={m["input_thresh"]}:offset={m["target_offset"]}:linear=true')
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', entrada, '-af', filtro,
                    '-ar', str(SR), '-c:a', 'pcm_s16le', salida], check=True)


def main():
    p = argparse.ArgumentParser(description='Mezcla narración y música con agache y volumen estándar.')
    p.add_argument('--voz', required=True)
    p.add_argument('--musica')
    p.add_argument('-o', '--salida', default='mezcla.wav')
    p.add_argument('--nivel-musica', type=float, default=0.5, help='respecto al pico de la voz')
    p.add_argument('--cola', type=float, default=2.0, help='segundos de música tras la última frase')
    p.add_argument('--lufs', type=float, default=-14)
    args = p.parse_args()

    voz = leer(args.voz).mean(axis=0)
    voz /= np.max(np.abs(voz))
    total = len(voz) + int(args.cola * SR)
    mezcla = np.zeros((2, total))
    mezcla[:, : len(voz)] += voz
    if args.musica:
        musica = leer(args.musica)
        if musica.shape[0] == 1:
            musica = np.repeat(musica, 2, axis=0)
        musica = np.pad(musica, ((0, 0), (0, max(total - musica.shape[1], 0))))[:, :total]
        t = np.arange(total) / SR
        musica *= np.minimum((total / SR - t) / max(args.cola, 0.1), 1)
        musica /= max(np.max(np.abs(musica)), 1e-9)
        mezcla += agachar(musica, np.pad(voz, (0, total - len(voz))), 0.65) * args.nivel_musica
    mezcla /= np.max(np.abs(mezcla))

    with tempfile.TemporaryDirectory() as tmp:
        bruto = os.path.join(tmp, 'bruto.wav')
        with wave.open(bruto, 'wb') as w:
            w.setnchannels(2)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes((mezcla.T * 0.95 * 32767).astype('<i2').tobytes())
        normalizar_volumen(bruto, args.salida, args.lufs)
    print(args.salida)


if __name__ == '__main__':
    main()
