"""
Sintetiza una lista de frases con Supertonic-3 y deja un WAV por frase. Lo llama voz/narrar.py
con el Python del entorno de Supertonic ($HERRAMIENTAS/supertonic); no hace falta usarlo a mano.

Entrada (JSON por la entrada estándar): {"voz": "M1", "velocidad": 1.0, "pasos": 12,
"carpeta": "...", "frases": ["...", ...]}. Salida: la lista de WAV, en JSON.
"""
import json
import os
import sys

from supertonic import TTS

pedido = json.load(sys.stdin)
tts = TTS(auto_download=True)
estilo = tts.get_voice_style(voice_name=pedido['voz'])
rutas = []
for i, frase in enumerate(pedido['frases']):
    # En Supertonic «speed» mayor es más rápido; en narrar.py la velocidad es la duración relativa.
    wav, _ = tts.synthesize(text=frase, voice_style=estilo, total_steps=pedido.get('pasos', 12),
                            speed=1 / pedido.get('velocidad', 1.0), lang='es')
    ruta = os.path.join(pedido['carpeta'], f'{i:04d}.wav')
    tts.save_audio(wav, ruta)
    rutas.append(ruta)
print(json.dumps(rutas))
