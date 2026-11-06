# Canal de historias reales de supervivencia (Shorts de YouTube y Reels de Facebook)

Por qué este nicho: `rastreador/informes/2026-10-30-hueco.md` (en inglés, mediana de 18.900 vistas en Shorts; en español,
1.300). Cómo se escribe y se monta: `../RETENCION.md`.

## Audiencia y elección de historias (lo que vio el usuario en las estadísticas, 1 y 2 de noviembre)

Más del 50 % es de **Colombia** y la mayoría tiene **50–60 años**. «Los 33» pegó bien, seguramente por ser una historia
conocida. Con eso se probaron dos historias colombianas medidas con el rastreador en `--region CO`: los niños de la selva
del Guaviare (2023) y el náufrago Luis Alejandro Velasco (1955, el «Relato de un náufrago»).

**2-nov: los dos colombianos no funcionaron** (lo vio el usuario en las estadísticas; no dio cifras). Se vuelve a **la
fórmula de los cortos 1–8**: historias conocidas en todo el mundo, medidas con `rastreador/youtube.py buscar` en inglés y
en español (10 años, por vistas por hora; sin `--region`), y por cada tanda una con **hueco** (mucho en inglés, poco en
español) y otra con **la demanda probada en español**, cambiando de escenario respecto a las anteriores. Así salieron el
11 (la cueva de Tailandia: 62 M en inglés, 430 k como mucho en español) y el 12 (Apolo 13: 2,1 M en español; 8 M y 4,5 M en
inglés en canales pequeños), y después el 13 (Aron Ralston, «127 horas»: 4,1 M en español, la demanda probada) y el 14
(Alexander Selkirk, el Robinson Crusoe real: 524 k en inglés y, en español, un solo Short sobre él, de 14 k; los demás
cuentan a Pedro Serrano). Si la historia toca a Colombia sin ser colombiana, se dice (el barco de Selkirk se hundió frente
a la actual Colombia). El 15 y el 16 (3-nov): los Andes de 1972 (la demanda más grande medida en español: 14 M en un Short,
y 45 de 53 vídeos pasan de 3 veces su canal) y Yossi Ghinsberg en la Amazonía boliviana (el hueco de oferta: 16 Shorts en
español en diez años frente a 80 en inglés, y los que hay llegan a 2,3 M). El 17 y el 18 (6-nov), sin medir de nuevo (la
sesión no tenía la clave de YouTube), de las candidatas que midió la sesión 11: Poon Lim, 133 días en una balsa en el
Atlántico (la demanda: 4,1 M en un Short en español) y la expedición del Endurance de Shackleton (183.000 como mucho en
español y el inglés en alza; la Antártida, y al final los salva un barco de la Armada de Chile).

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

## Sonido

El usuario avisó de los efectos tras el primer corto, y con razón: medidos con `audio/revisar_mezcla.py`, sonaban en
conjunto +1,4 LU **por encima** de la voz (el trueno y los golpes graves, hasta 15 LU más que ella), había 39 en 70 s y
algunos (las teclas, un «whoosh») ni se oían. Las reglas desde el 31-oct:

- **La voz manda.** Mientras se habla, cada efecto queda al menos 8 LU por debajo de ella; en una pausa, no más de 3 LU
  bajo su nivel medio. Se comprueba antes de renderizar: `python3 audio/revisar_mezcla.py <proyecto>` con 0 avisos (la
  columna «vol que cabe» da el volumen que entra).
- **Un ambiente por lugar**, bajo y continuo, con fundidos largos (la selva, el mar, la tormenta, bajo el agua), en vez
  de un efecto por palabra. El paso de un mundo a otro (de la superficie a bajo el agua) es el efecto.
- **Golpes, solo donde algo golpea en pantalla** (un martillo, el agua, un trueno con su destello) y un único golpe
  grave por vídeo, muy bajo (`impact-bass` es subgrave puro).
- **Nada de sonidos de interfaz** en este canal (pop, click, riser, whoosh): rompen la seriedad de una historia real. Las
  teclas de la máquina de escribir, solo para una fecha que se escribe en pantalla.
- **Desde el corto 3 (31-oct), más estricto**, porque el usuario pidió «a la próxima utiliza solo los efectos de sonido
  como el rayo y bájale más a la música»: solo efectos fuertes con su golpe en pantalla (el rayo con su destello, el
  martillo contra el casco), sin ambientes de fondo; 2–4 por corto. La música, 16–20 LU bajo la voz.

## Ética

Historias reales de personas reales: datos contrastados en dos fuentes, sin inventar diálogos ni detalles, sin morbo y
con respeto por quienes murieron. Las imágenes son ilustraciones y la descripción lo dice.

## Cómo se hace un vídeo

La música elegida (tras medir las candidatas con `audio/graves.py`) se apunta en `recursos/musica.json` como `lecho`
(`pieza`, `duracion`, `entrada` 0 para el bucle y, si la pieza tiene valles muy hondos que dejan huecos bajo la voz,
`comprimir` 3) y `preparar-corto.sh` la alarga a la duración del vídeo; si una tanda se descarta, se sustituye en ese
archivo y se anota en `_descartada`. Al mirar las imágenes: una sola persona cuando la voz dice «solo» (FLUX añade
gente: pedir «only one person in the whole image, no other people») y nadie de cara («his back to the camera, no face
visible»; «seen from behind» no basta). Los efectos de BigSoundBank que pida el montaje los baja
`montar.py` si faltan (en `salidas/supervivencia/cortos/sfx/`). Mejor grabaciones sin procesar: los sonidos procesados
de Okene (`bajoagua`, `golpecasco`, `gemido`) no tienen guardado cómo se hicieron.

```bash
canales/preparar-corto.sh supervivencia cortos/01-juliane
python3 canales/supervivencia/cortos/01-juliane/mapa.py
python3 canales/businessformen/kit/montar.py --canal canales/supervivencia cortos/01-juliane
cd canales/supervivencia/cortos/01-juliane/proyecto && ../../../../../video/hf.sh check --json
../../../../../video/hf.sh render -o salida.mp4 --quality high --crf 20 --quiet
```
