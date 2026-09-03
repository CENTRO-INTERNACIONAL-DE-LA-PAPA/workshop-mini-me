# Manual del workshop

PDF del participante, escrito en Quarto con motor **Typst**.

## Compilar

```bash
quarto render manual.qmd
```

Sale en `_output/manual.pdf`. Typst viene incluido con Quarto: no hay que instalarlo aparte.

Para revisar el diseño página por página sin abrir el PDF:

```bash
quarto typst compile manual.typ paginas/p{p}.png --ppi 110
```

## Colores

Los seis colores de la marca están al principio de `_brand.typ` y **son provisionales**:
son marcadores de posición elegidos para que el documento se vea coherente, no los códigos
oficiales de CIP. Antes de imprimir hay que pedirle el manual de marca a Comunicaciones y
reemplazarlos. Todo el documento sale de ahí, así que es un cambio de seis líneas.

## Estructura

| Archivo | Qué es |
|---|---|
| `manual.qmd` | Portada, configuración del formato y los `include` de las secciones |
| `_brand.typ` | Paleta, tipografía, estilos de título y tabla, y las cajas |
| `secciones/*.qmd` | Una sección por archivo, en orden |

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
- **La configuración del formato va en el front matter de `manual.qmd`**, no en
  `_quarto.yml`: al renderizar un archivo suelto, el `_quarto.yml` no se aplica.

## Tipografía

`Segoe UI` y `Cascadia Mono`, ambas de Windows. En Linux hay que cambiar `mainfont` y
`monofont` en el front matter por algo instalado, o Typst avisa y usa su tipografía por
defecto.
