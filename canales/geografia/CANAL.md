# Canal de geografía (Shorts de YouTube y Reels de Facebook)

Por qué este nicho: `rastreador/informes/2026-10-30-hueco.md`. Cómo se escribe y se monta: `../RETENCION.md`.

## Nombre (a elegir; comprobar que está libre en YouTube y Facebook)

- **Atlas Curioso**: dice el tema y la promesa.
- **El Porqué del Mapa**: dice el formato («¿por qué…?»).
- **Meridiano**: corto y propio; la promesa la dan los vídeos.

## Identidad

- **Color:** océano azul noche `#081521`, tierra pizarra `#1d3347`, el país protagonista en amarillo mapa `#FFC531`
  con el texto oscuro encima. El amarillo, solo para lo que importa.
- **Tipografía:** Archivo (900 los titulares, 800 los rótulos) e IBM Plex Mono para coordenadas y notas.
- **Voz:** Supertonic-3 **F4** (femenina, clara y rápida: unas 3,2 palabras por segundo). Distinta de la M1 de
  BusinessForMen y de la M2 de supervivencia.
- **Mapas:** Natural Earth (dominio público) en proyecciones locales; medidas propias con `kit/geo.py`.
- **Formato:** 1080 × 1920, 60–90 s, la pregunta escrita sobre el mapa en el fotograma 0, una razón por mundo (el mapa
  de cerca, un corte, una foto) y bucle al primer plano.

## Cómo se hace un vídeo

```bash
canales/preparar-corto.sh geografia cortos/01-chile                         # voz, música e imágenes
python3 canales/geografia/cortos/01-chile/mapa.py                           # los mapas del vídeo
python3 canales/businessformen/kit/montar.py --canal canales/geografia cortos/01-chile
cd canales/geografia/cortos/01-chile/proyecto && ../../../../../video/hf.sh check --json
../../../../../video/hf.sh render -o salida.mp4 --quality high --crf 20 --quiet
```
