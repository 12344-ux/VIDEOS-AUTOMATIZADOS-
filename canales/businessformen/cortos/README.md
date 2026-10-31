# BusinessForMen · cortos verticales (Reels, TikTok y Facebook)

Vídeos de 45–55 s en 9:16 para Instagram, TikTok y Facebook, con el mismo archivo para las tres: sin logos ni marcas
de agua de ninguna app y sin «sígueme» al final. Usan el kit del canal (`../kit/`) con su modo vertical y la marca
Consejo.

| | Corto | Tema | Formato | Gancho (fotograma 0) |
| --- | --- | --- | --- | --- |
| 1 | `01-la-clausula` | Negociación | El error de un gigante | «IBM firmó esto.» sobre el contrato |
| 2 | `02-la-cuerda` | Organización interna | Antes y después, con giro | «La peor fábrica de EE. UU.» |
| 3 | `03-para-siempre` | Marca | El mito desmontado | «1.500 años de tradición» sobre el anillo |
| 4 | `04-el-ancla` | Precios y negociación | Un caso famoso y el experimento que lo explica | «999 $» en la pantalla del auditorio |
| 5 | `05-el-perrito` | Modelo de negocio | La paradoja y su respuesta | «El mismo precio desde 1985» sobre el perrito |
| 6 | `06-la-pizza` | Marketing y honestidad | El giro contra la intuición | «Lo dijo en la tele: su pizza era mala» |
| 7 | `07-el-sueldo` | Gestión de equipos | La paradoja y su respuesta | «Pagó el doble · para ahorrar» sobre la cadena de montaje |
| 8 | `08-la-formula` | Marca | El error contra la intuición | «Ganó 200.000 catas · y fue un desastre» sobre la lata |
| 9 | `09-la-camara` | Estrategia | La empresa que inventó su propio final | «Kodak inventó esto · en 1975» sobre el prototipo |

Los cortos 4–6 se hicieron para que **se entiendan más y con mejor edición**: temas cotidianos y una sola idea, menos
fechas y nombres, la voz un 4 % más pausada, un dibujo que explica cada mecanismo (la regla del ancla, las dos barras
de las cuotas, la columna de ventas), el 2.5D por capas en las fotos donde el objeto se recorta sobre un fondo liso (en las demás, acercamiento), el texto dentro de las pantallas de las fotos y
transiciones que solapan las escenas (`entrada=` en `escena()`: la cortina roja de la marca, barridos con filo rojo,
subidas e iris desde un objeto). Ninguna escena empieza vacía.

```bash
canales/businessformen/cortos/preparar.sh [corto…]             # marca, voces, música, imágenes y capas 2.5D (en salidas/…/cortos/)
python3 canales/businessformen/kit/montar.py cortos/01-la-clausula
cd canales/businessformen/cortos/01-la-clausula/proyecto && ../../../../../video/hf.sh check --json
../../../../../video/hf.sh render -o salida.mp4 --quality high --crf 20 --quiet
```

## Reglas del formato corto

Sacadas de la investigación del 30-oct-2026 (búsquedas web; casi todo son guías de marketing y de herramientas, sin
datos de las plataformas, así que son orientativas) y de la guía de vídeo vertical de HyperFrames. Se suman a
`../EDICION.md`.

1. **El gancho está en el fotograma 0.** Es la miniatura y lo que decide si se quedan: una frase en grande ya en
   pantalla, sobre la imagen, nunca negro ni logo. La voz entra a los 0,1 s y la tensión llega en la primera frase
   (las guías hablan de 1–3 s; la mitad de los que se van, se van ahí).
2. **Más rápido que en horizontal:** algo cambia cada 1–3 s y cada escena dura 2–6 s con movimiento dentro.
3. **Se entiende sin sonido.** Muchos lo ven en silencio: subtítulos quemados en grupos de 1–4 palabras, la palabra
   que suena en un bloque rojo. Se quitan donde la pantalla ya escribe en grande lo que dice la voz.
4. **Zona segura de las tres apps.** Lo que se lee va entre x 80–940 e y 200–1130; los subtítulos, de 1168 a 1320.
   Arriba está la barra del móvil; a la derecha, los botones; abajo, el texto, la cuenta y la música de cada app
   (ahí solo imagen o textura). Las guías no coinciden en los márgenes exactos: esta es la más conservadora.
5. **Sin final de «sígueme», sin tarjeta de cierre.** El último plano vuelve al primero: el bucle hace que se vea dos
   veces sin darse cuenta (las guías coinciden en que el visionado repetido cuenta). La firma BFM va dentro del
   golpe rojo de la lección, no en una tarjeta aparte.
6. **Sin marcas de otras apps.** Instagram dejó de recomendar Reels con marca de agua de TikTok (Adam Mosseri, 2021);
   el logo propio está bien. Por eso cada corto sale limpio del render y se sube el mismo archivo a las tres.
7. **Un solo golpe rojo por corto, como mucho dos:** el de la lección (y en el 3, el «por un anuncio» del gancho).
8. **Pocos efectos, y fuertes** (31-oct-2026, el usuario: «utiliza solo los efectos de sonido como el rayo»): 2–4 por
   corto, grabaciones reales con su golpe en pantalla (las monedas que caen, el teléfono que suena, el disparo de una
   cámara, un portazo) y el golpe rojo de la lección. Nada de silbidos de transición, pops, clicks, risers ni ambientes
   de fondo. Efectos de BigSoundBank (CC0, `CREDITOS.md` en `salidas/…/cortos/sfx/`), medidos con
   `audio/revisar_mezcla.py`: con la voz encima, al menos 8 LU por debajo de ella.
9. **Volumen para móvil:** −14 LUFS en la entrega y la música medida (`audio/graves.py`): nada que tenga la mayoría de
   su energía bajo 150 Hz. **La música, baja** (31-oct, «bájale más a la música que acompaña»): 16–20 LU por debajo de
   la voz, medido con `audio/revisar_mezcla.py`.
10. **Duración:** 45–55 s. Las guías ponen lo educativo en 30–60 s; por debajo de un minuto vale igual en las tres
    apps (Facebook ya no tiene un límite fijo; Instagram admite hasta 3 min).
11. **La imagen, a pantalla completa** (31-oct): el velo del kit es ligero (oscurece la barra del móvil y los titulares
    de arriba y una franja suave detrás de los subtítulos); con el de antes, oscuro de la mitad hacia abajo, «la imagen
    se veía como la mitad». Los prompts piden que el motivo llene el encuadre.
12. **La versión sin música, solo con efectos** (31-oct, el usuario, en el corto 7: «la voz del canal de supervivencia,
    sin música de fondo y solo efectos de sonido, como transiciones o efectos adicionales»; `montar.py --variante m2`).
    El ambiente de cada sitio, bajo y nunca callado del todo: la fábrica a unos 15 LU bajo la voz donde se ve, más baja en
    lo demás, y bajo la lección el aire de la nave vacía (callado del todo, las pausas de la voz son silencios). Un whoosh
    distinto en cada corte, con los cortes que abren frase 0,38 s antes de ella para que caiga en la pausa; y el golpe de
    cada acción (las monedas, los sellos, el interruptor, las teclas del contador) un fotograma después de su imagen.
    Con `audio/revisar_mezcla.py`, 0 avisos y ningún hueco antes de renderizar.

## Publicar

- El mismo MP4 (1080 × 1920, 30 fps, H.264, AAC) en las tres. La portada, el fotograma 0.
- La entrega, a −14 LUFS y en bucle: `BUCLE=1 GRAVES=-20 PICO=-2 video/entregar.sh render.mp4 entrega.mp4 -14 copiar`.
  Sin `BUCLE`, loudnorm (que pasa a su modo dinámico) dejaba el final 5–6 dB más alto que el principio, el bucle
  saltaba y el gancho sonaba 2–4 dB más bajo que el resto.
- **Etiqueta de IA activada** en cada app (la voz es sintética y las imágenes, generadas): en TikTok, «Contenido
  generado por IA»; en Instagram y Facebook, «Información de IA». Y en la descripción, el aviso de la voz que exige la
  licencia de Supertonic. La música es de MusicGen: solo vale mientras el canal no se monetice.
- La ficha de cada corto (texto, etiquetas y fuentes) está en su `PUBLICACION.md`.
