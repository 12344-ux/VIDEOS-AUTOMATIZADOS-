# BusinessForMen · pruebas de marca

Tres identidades para el canal, cada una en un vídeo de 19 s a 1920 × 1080 y 30 fps con su logo animado y una
miniatura. Las tres cuentan lo mismo, con la misma voz y los mismos tiempos; cambian el rojo, la tipografía, el
movimiento, el tratamiento de la imagen, la música y el sonido. Sirven para que el usuario elija la marca.

Texto (Supertonic-3 M1, 13,6 s): *«En una negociación, gana quien puede levantarse de la mesa. En Harvard lo llaman
tu MAAN: tu mejor alternativa a un acuerdo negociado. Si no la conoces, no estás negociando. Estás pidiendo.»*
En el guion, «Járvard» y «maan», para que la voz los pronuncie bien.

| | 1 · Sastre | 2 · Consejo | 3 · Lacre |
| --- | --- | --- | --- |
| Idea | La sastrería clásica: lenta, fina, segura | La sala de juntas moderna: rápida, precisa | Editorial y contundente |
| Rojo | Burdeos `#8E1B2C` | Carmesí `#B0122F` | Lacre `#B3261E` |
| Fondo y texto | Negro cálido `#0E0C0C`, marfil `#EFE8DD` | Grafito `#0A0B0D`, blanco `#F4F3F0` | Negro `#0B0A0A`, papel `#F1EBE1` |
| Tipografía | Bodoni Moda y Jost | Inter Tight e IBM Plex Mono | Archivo Narrow e Instrument Serif |
| Movimiento | Máscaras que suben, líneas finas, fundidos; raya diplomática de fondo | Palabra a palabra, bloques rojos, cortina roja, cortes secos; retícula | Palabras que golpean, letras que se encienden, sello que se estampa |
| La MAAN | Iniciales en Bodoni y el resto de cada palabra, que se abre | Cuatro cuadros rojos y la palabra que sale de cada uno | Cuatro letras enormes que se encienden en rojo con su palabra |
| «Estás pidiendo» | Banda roja a todo lo ancho | Corte a pantalla roja | Sello rojo estampado, con temblor |
| Logo | Etiqueta de sastre «BfM» y «Business*For*Men» | Cuadro rojo «BFM» y «BUSINESS**FOR**MEN» | Sello de lacre «BfM» y «BUSINESSFORMEN» |
| Música (MusicGen) | Piano y violonchelo, 80 BPM | Electrónica limpia, 100 BPM | Cuerdas en ostinato y percusión, 90 BPM |

## Repetirlas

```bash
canales/businessformen/marca/preparar.sh            # voz, música, imagen, texturas y fuentes, y montar
canales/businessformen/marca/preparar.sh --render   # además los vídeos, la entrega a −15 LUFS, las miniaturas y la hoja
```

Las plantillas están en `plantillas/`, fuera de los proyectos: HyperFrames toma cada HTML con `data-composition-id`
de la raíz de un proyecto por otra composición. `montar.py` les pone los tiempos de las palabras y escribe
`<ruta>/index.html` y `miniaturas/<ruta>/index.html`; `hoja.py` hace la hoja comparativa a partir de los renders.

## Medido (sesión 3, Xeon con AMX)

- Voz: 1 min 47 s (casi todo, la carga de los modelos). Música: tres piezas de 20 s en 207 s, más 49 s de carga.
  Imagen: 113 s con la carga de FLUX; EDSR, 6,8 s.
- Render: de 30 a 32 s cada vídeo de 18,8 s (todo CSS, sin WebGL): 1,7 s por segundo de vídeo.
- Entrega: de −15,0 a −15,5 LUFS, pico por debajo de −1,6 dB; de 2,7 a 3,5 MB.
