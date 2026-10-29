"""
Tiempo de cada palabra de una narración de la que ya se sabe el texto: alineación forzada CTC
con un modelo de reconocimiento en español (wav2vec2 XLSR-53 de jonatasgrosman, Apache 2.0).
Sirve para cualquier voz; Piper da sus tiempos por su cuenta, Supertonic no.

Se ejecuta con el Python del entorno de FastSD (trae torch y transformers):
  PY=$HERRAMIENTAS/fastsdcpu/env/bin/python
  $PY voz/alinear.py narracion.wav "El texto exacto que dice la voz." -o tiempos.json

Medido contra la alineación exacta de Piper (19 palabras): ver docs/bitacora.md. Whisper con DTW
quedó a 135 ms de media y llegaba siempre tarde.
"""
import argparse
import json
import os
import re
import sys
import unicodedata
import wave

import numpy as np

HERRAMIENTAS = os.environ.get('HERRAMIENTAS', os.path.expanduser('~/herramientas-videos'))
MODELO = os.path.join(HERRAMIENTAS, 'extra', 'alineador-es')
SEGUNDOS_POR_CUADRO = 320 / 16000  # wav2vec2: un vector cada 20 ms


def leer_wav(ruta):
    with wave.open(ruta) as w:
        sr, canales, ancho = w.getframerate(), w.getnchannels(), w.getsampwidth()
        datos = np.frombuffer(w.readframes(w.getnframes()), dtype={2: '<i2', 4: '<i4'}[ancho])
    x = datos.reshape(-1, canales).mean(1).astype(np.float32) / (2 ** (8 * ancho - 1))
    return x, sr


def a_16k(x, sr):
    if sr == 16000:
        return x
    n = round(len(x) * 16000 / sr)
    espectro = np.fft.rfft(x)
    salida = np.zeros(n // 2 + 1, dtype=complex)
    m = min(len(espectro), len(salida))
    salida[:m] = espectro[:m]
    return (np.fft.irfft(salida, n) * n / len(x)).astype(np.float32)


def letras(palabra, vocab):
    """La palabra en minúsculas, solo con letras del vocabulario (quita tildes que no tenga)."""
    salida = []
    for ch in palabra.lower():
        if ch in vocab:
            salida.append(ch)
        else:
            base = unicodedata.normalize('NFKD', ch)[0]
            if base in vocab and base.isalpha():
                salida.append(base)
    return ''.join(c for c in salida if c not in "|'-")


def ctc_forzado(logp, fichas, vacio):
    """Camino más probable que emite las fichas en orden (Viterbi sobre el enrejado CTC).
    Devuelve, para cada ficha, el primer y el último cuadro en que suena."""
    T, J = logp.shape[0], len(fichas)
    enrejado = np.full((T + 1, J + 1), -np.inf)
    enrejado[0, 0] = 0
    enrejado[1:, 0] = np.cumsum(logp[:, vacio])
    for t in range(T):
        quedarse = enrejado[t, 1:] + logp[t, vacio]
        avanzar = enrejado[t, :-1] + logp[t, fichas]
        # Repetir la misma ficha sin pasar por el vacío también vale (CTC la fusiona).
        repetir = enrejado[t, 1:] + logp[t, fichas]
        enrejado[t + 1, 1:] = np.maximum(np.maximum(quedarse, avanzar), repetir)
    # Vuelta atrás desde el final.
    t, j = T, J
    cuadros = [[] for _ in range(J)]
    while t > 0 and j > 0:
        quedarse = enrejado[t - 1, j] + logp[t - 1, vacio]
        avanzar = enrejado[t - 1, j - 1] + logp[t - 1, fichas[j - 1]]
        repetir = enrejado[t - 1, j] + logp[t - 1, fichas[j - 1]]
        mejor = max(quedarse, avanzar, repetir)
        if mejor == avanzar:
            cuadros[j - 1].append(t - 1)
            j -= 1
        elif mejor == repetir:
            cuadros[j - 1].append(t - 1)
        t -= 1
    return [(min(c), max(c)) if c else None for c in cuadros]


def alinear(x, sr, texto):
    """[{"texto", "inicio", "fin"}] para cada palabra del texto, en segundos."""
    import torch
    from transformers import Wav2Vec2ForCTC

    vocab = json.load(open(os.path.join(MODELO, 'vocab.json')))
    modelo = Wav2Vec2ForCTC.from_pretrained(MODELO).eval()
    audio = a_16k(x, sr)
    audio = (audio - audio.mean()) / (audio.std() + 1e-7)
    with torch.inference_mode():
        logp = torch.log_softmax(modelo(torch.from_numpy(audio)[None]).logits[0], -1).numpy()

    palabras = texto.split()
    fichas, dueño = [], []
    for i, p in enumerate(palabras):
        if fichas:
            fichas.append(vocab['|'])
            dueño.append(None)
        for ch in letras(p, vocab):
            fichas.append(vocab[ch])
            dueño.append(i)
    spans = ctc_forzado(logp, np.array(fichas), vocab['<pad>'])

    tiempos = [None] * len(palabras)
    for i in range(len(palabras)):
        propios = [s for s, d in zip(spans, dueño) if d == i and s]
        if propios:
            tiempos[i] = [min(a for a, _ in propios) * SEGUNDOS_POR_CUADRO,
                          (max(b for _, b in propios) + 1) * SEGUNDOS_POR_CUADRO]
    # Palabras sin letras alineables (por ejemplo, cifras): entre sus vecinas.
    for i, t in enumerate(tiempos):
        if t is None:
            antes = next((tiempos[k][1] for k in range(i - 1, -1, -1) if tiempos[k]), 0.0)
            despues = next((tiempos[k][0] for k in range(i + 1, len(tiempos)) if tiempos[k]), len(x) / sr)
            tiempos[i] = [antes, max(antes, despues)]
    return [{'texto': p, 'inicio': round(a, 3), 'fin': round(b, 3)} for p, (a, b) in zip(palabras, tiempos)]


def main():
    p = argparse.ArgumentParser(description='Tiempo de cada palabra por alineación forzada.')
    p.add_argument('audio')
    p.add_argument('texto')
    p.add_argument('-o', '--salida')
    args = p.parse_args()
    x, sr = leer_wav(args.audio)
    resultado = alinear(x, sr, args.texto)
    texto = json.dumps(resultado, ensure_ascii=False, indent=1)
    if args.salida:
        open(args.salida, 'w', encoding='utf-8').write(texto)
    else:
        print(texto)


if __name__ == '__main__':
    sys.exit(main())
