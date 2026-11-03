# Canal de incidentes sin resolver (Shorts de YouTube y Reels de Facebook)

Lo pidió el usuario el 3-nov-2026, con el canal de supervivencia funcionando: «otro tipo de vídeos que atraiga a más
población… incidentes, cosas extrañas que no se resolvieron, por ejemplo un avistamiento de un objeto volador… bien
extrañas, inquietantes e interesantes». Cómo se escribe y se monta: `../RETENCION.md`.

## Por qué este nicho (medido)

- **TikTok en español** (septiembre de 2026, `rastreador/informes/2026-10-30-hueco.md`): «terror y paranormal» llega a
  100.000 vistas 2,4 veces más que la media del idioma, con 4.638 vídeos al mes; «misterios», 2,2 veces, con 2.670. No es
  un hueco (en español hay oferta), pero atrae a mucha gente: la diferencia tiene que estar en la edición y en el rigor.
- **Shorts de YouTube** (3-nov, `rastreador/youtube.py buscar`, 10 años): los casos clásicos funcionan en canales pequeños
  en los dos idiomas. Valentich, 273.000 vistas en español en un canal de 4.700 suscriptores (30 veces su mediana, hace
  2 meses) y 766.000 en inglés; el «Tic Tac» del Nimitz, 1,5 M en inglés en un canal nuevo de 1.400 («Case File #001») y
  casi nada en español (el hueco); el Mary Celeste, 635.000 y 162.000 en español; las luces de Phoenix, 2,4 M en inglés y
  18.000 como mucho en español; la señal Wow!, 20 M en inglés y 2,1 M en español (pero en 2024 se propuso una explicación
  natural: no es un caso «sin resolver» limpio).
- **El formato que funciona ahora**: el expediente («Archivo», «Expediente», «Case File #001»). Aquí, cada vídeo es un
  expediente numerado.

## Elección de casos

Como en supervivencia: casos conocidos en todo el mundo, medidos en inglés y en español, y por cada tanda uno con
**demanda probada en español** y otro con **hueco** (mucho en inglés, poco en español). Primero los que tienen un
documento detrás (una transcripción, un informe, un vídeo oficial, testigos con nombre), porque permiten enseñar la
prueba en pantalla. Candidatos medidos: el «Tic Tac» del Nimitz (2004, el hueco), las luces de Phoenix (1997), el Mary
Celeste (1872), el vuelo 19 (1945) y el caso Manises (1979, España).

## Nombre (a elegir; comprobar que está libre en YouTube y Facebook)

- **Expediente Abierto**: el formato y la promesa (no está resuelto).
- **Sin Explicación**: directo, para buscar.
- **Caso Sin Cerrar**: intriga.

## Identidad

- **Color:** negro de noche `#06090c`, blanco frío `#e8eef0` y el verde fósforo de una pantalla de radar `#62f59b`, solo
  en lo que importa (la hora, lo que no se explica, el dato clave). Sobre papel, el verde oscuro `#0f5c3c`.
- **Tipografía:** Big Shoulders Display (800) para los golpes y los sellos, Space Grotesk (700) para los subtítulos y el
  texto, y JetBrains Mono para el expediente: horas, transcripciones, fichas y fechas.
- **El visor:** cuatro esquinas finas sobre cada plano (el vídeo es un expediente que se mira); `visor: false` lo quita.
- **Voz:** Supertonic-3 **M5**, la más grave y pausada de las voces masculinas: 97 Hz de tono mediano y 2,9 palabras por
  segundo, frente a 105–140 Hz y 3,1–3,6 de las demás (medido el 3-nov con la misma frase).
- **Imágenes:** ilustraciones semirrealistas de FLUX.3, de noche, en azules fríos con un brillo verde; las personas reales,
  nunca de cara. Lo dibujado (radar, radio, mapas) es una recreación y no imita grabaciones reales.
- **Formato:** 1080 × 1920, 60–90 s; el gancho es la frase o el dato que nadie explica, escrito en grande en el fotograma 0;
  el secreto, tapado en el expediente y revelado al 60–75 %; las hipótesis al final, sin decidir por el espectador, y
  bucle al primer plano.

## Esqueleto (unos 75–85 s)

| Tramo | Tiempo | Qué pasa |
| --- | --- | --- |
| Gancho | 0–4 s | la frase o el dato imposible, en grande, con la imagen que lo enseña |
| Expediente (bucle abierto) | 4–7 s | lo que se tapa: «lo que se oyó después», «lo que encontraron» |
| El lugar y quién | 7–15 s | mapa, fecha, nombre y edad |
| Minuto a minuto | 15–45 s | la hora en pantalla, la transcripción o los testigos; cada paso, más raro que el anterior |
| La revelación | 45–55 s | lo tapado, con el momento visual más grande |
| Lo que vino después | 55–68 s | la búsqueda, las pruebas, el informe oficial |
| Las hipótesis | 68–75 s | las explicaciones que se han dado, como preguntas; «nadie lo sabe» |
| Bucle | 75–80 s | la última frase empalma con la primera |

## Sonido

Las reglas de supervivencia (`../supervivencia/CANAL.md`): la voz manda, cada efecto al menos 8 LU bajo ella mientras habla
(`python3 audio/revisar_mezcla.py <proyecto>` con 0 avisos) y la música 16–20 LU por debajo. Lo propio de este canal: la
radio (chasquidos, interferencias) es parte de la identidad, pero con la misma regla: pocos efectos, cada uno con su golpe
en pantalla; nada de sonidos de interfaz ni de sustos baratos.

## Ética

Casos reales, con personas reales: datos contrastados en dos fuentes, sin inventar diálogos ni detalles (lo que se dijo
por radio, traducido de la transcripción oficial), sin morbo y con respeto por quien desapareció o murió. **No se
afirma lo que no se sabe**: ni extraterrestres ni conspiraciones; las explicaciones se cuentan como hipótesis, con la
oficial siempre. Las imágenes son ilustraciones y la descripción lo dice; las recreaciones dibujadas no se presentan como
grabaciones.

## Cómo se hace un vídeo

Como en supervivencia (`../supervivencia/CANAL.md`, «Cómo se hace un vídeo»), con la marca de este canal y sus
plantillas comunes en `cortos/comun/`: `gancho` (la frase en grande; modos inicio y vuelta), `foto` (la de supervivencia
con esta marca, el visor y `apagones` para «desaparece… y vuelve») y `expediente` (la hoja: oculta, revela e informe, con
su sello).

```bash
canales/preparar-corto.sh incidentes cortos/01-valentich
python3 canales/incidentes/cortos/01-valentich/mapa.py
python3 canales/businessformen/kit/montar.py --canal canales/incidentes cortos/01-valentich
cd canales/incidentes/cortos/01-valentich/proyecto && ../../../../../video/hf.sh check --json
../../../../../video/hf.sh render -o salida.mp4 --quality high --crf 20 --quiet
```
