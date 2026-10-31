# Canal de historias reales de supervivencia (Shorts de YouTube y Reels de Facebook)

Por qué este nicho: `rastreador/informes/2026-10-30-hueco.md` (en inglés, mediana de 18.900 vistas en Shorts; en español,
1.300). Cómo se escribe y se monta: `../RETENCION.md`.

## Nombre (a elegir; comprobar que está libre en YouTube y Facebook)

- **Contra Todo Pronóstico**: la promesa de cada historia.
- **Los que Volvieron**: intriga y dice el tema.
- **Sobrevivientes**: directo, para buscar.

## Identidad

- **Color:** negro carbón `#0b0a09`, blanco hueso `#f2ede4` y el naranja de una bengala `#FF5E1A`, solo en lo que
  importa (lo que salva, lo que se pierde).
- **Tipografía:** Barlow Condensed (800) para los golpes, Barlow para el texto y Special Elite (máquina de escribir)
  para el cuaderno de días, fichas y fechas.
- **Voz:** Supertonic-3 **M2** (masculina, la más grave: de documental).
- **Imágenes:** ilustraciones semirrealistas de FLUX.3; las personas reales, nunca de cara.
- **Formato:** 1080 × 1920, 60–90 s; el final en la primera frase («cayó 3.000 metros… y sobrevivió»), la historia en
  presente y contada por días, una regla o un secreto tachado que se revela al final, y bucle al primer plano.

## Ética

Historias reales de personas reales: datos contrastados en dos fuentes, sin inventar diálogos ni detalles, sin morbo y
con respeto por quienes murieron. Las imágenes son ilustraciones y la descripción lo dice.

## Cómo se hace un vídeo

```bash
canales/preparar-corto.sh supervivencia cortos/01-juliane
python3 canales/supervivencia/cortos/01-juliane/mapa.py
python3 canales/businessformen/kit/montar.py --canal canales/supervivencia cortos/01-juliane
cd canales/supervivencia/cortos/01-juliane/proyecto && ../../../../../video/hf.sh check --json
../../../../../video/hf.sh render -o salida.mp4 --quality high --crf 20 --quiet
```
