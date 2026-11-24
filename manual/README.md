# Documentos del taller

Los PDF del taller, escritos en Quarto con motor **Typst**: la guía paso a paso, la agenda y la
propuesta del Reto Mini-Me.

## Compilar

```bash
quarto render
```

Compila los tres documentos en `_output/`: `guia_taller.pdf`, `agenda.pdf` y `reto_mini_me.pdf`.
Para uno solo: `quarto render guia_taller.qmd`. Typst viene incluido con Quarto: no hay que
instalarlo aparte.

Para revisar el diseño página por página sin abrir el PDF:

```bash
quarto typst compile guia_taller.typ paginas/p{p}.png --ppi 110
```

## Colores

Los seis colores de la marca están al principio de `_brand.typ` y **son provisionales**:
son marcadores de posición elegidos para que el documento se vea coherente, no los códigos
oficiales de CIP. Antes de imprimir hay que pedirle el manual de marca a Comunicaciones y
reemplazarlos. Todo el documento sale de ahí, así que es un cambio de seis líneas.

## Estructura

| Archivo | Qué es |
|---|---|
| `guia_taller.qmd` | Guía paso a paso del ejercicio para los asistentes, acorde a `presentacion/taller.qmd` |
| `agenda.qmd` | Agenda de una página del 24 de noviembre, con el QR del Mentimeter |
| `reto_mini_me.qmd` | Propuesta del Reto Mini-Me: preguntas por temática, cronograma, pitch, voto, pistas para facilitadores y hoja del reto |
| `img/qr-mentimeter-pre.svg`, `img/qr-mentimeter-post.svg` | QR de los Mentimeter pre (menti.com/al2sww8pf7ik) y post (menti.com/alhuo61h2cfn). Se regeneran con `qrencode -t SVG` |
| `img/taller/` | Copia de las capturas de `../presentacion/img/taller` que usa la guía. Typst no lee imágenes fuera de esta carpeta, y un enlace simbólico no funciona en Windows: si cambia una captura en la presentación, hay que copiarla aquí también |
| `_brand.typ` | Paleta, tipografía, estilos de título y tabla, y las cajas |

## Los cuatro elementos de diseño

En un bloque ` ```{=typst} `:

```typst
#prueba[ Una acción que el participante puede hacer ahora. ]
#ojo[ Algo que se rompe, o un resultado que engaña. ]
#nota[ El porqué de algo. ]
#prompt("nombre_del_subagente")[ El texto que se copia y se pega. ]
```

## Dos cosas que rompen la compilación

- **Los signos `<` y `>`** dentro de un bloque Typst se interpretan como etiquetas. Para
  marcadores de posición usar `«así»`.
- **La configuración del formato va en el front matter de cada `.qmd`**, no en
  `_quarto.yml`: al renderizar un archivo suelto, el `_quarto.yml` no se aplica.

## Tipografía

`Segoe UI` y `Cascadia Mono`, ambas de Windows. En Linux hay que cambiar `mainfont` y
`monofont` en el front matter por algo instalado, o Typst avisa y usa su tipografía por
defecto.
