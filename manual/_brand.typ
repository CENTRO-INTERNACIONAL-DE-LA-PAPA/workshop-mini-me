// ---------------------------------------------------------------------------
// Identidad visual del manual del workshop Mini-Me.
//
// PALETA PROVISIONAL. Estos valores son marcadores de posicion elegidos para que
// el documento se vea coherente, NO son los codigos oficiales de CIP. Antes de
// imprimir hay que pedirle a Comunicaciones el manual de marca y reemplazar los
// seis colores de abajo. Todo el documento sale de aqui, asi que es un cambio de
// seis lineas y nada mas.
// ---------------------------------------------------------------------------

#let cip-azul   = rgb("#0B5A8A")  // titulos y acentos principales
#let cip-verde  = rgb("#5C9A3C")  // "haz esto", pasos que funcionan
#let cip-tierra = rgb("#C4622D")  // advertencias, cosas que se rompen
#let cip-gris   = rgb("#3F464C")  // texto corrido
#let cip-suave  = rgb("#EEF4F8")  // fondos de caja
#let cip-borde  = rgb("#CBD9E3")  // filetes y bordes

#set text(fill: cip-gris)

// Jerarquia: el nivel 1 abre bloque con un filete de color, el resto es sobrio.
#show heading.where(level: 1): it => block(
  width: 100%,
  inset: (top: 10pt, bottom: 6pt),
  stroke: (bottom: 1.5pt + cip-azul),
  text(fill: cip-azul, weight: "bold", size: 16pt, it.body),
)
#show heading.where(level: 2): it => block(
  inset: (top: 8pt, bottom: 2pt),
  text(fill: cip-azul, weight: "bold", size: 13pt, it.body),
)
#show heading.where(level: 3): it => block(
  inset: (top: 6pt, bottom: 1pt),
  text(fill: cip-gris, weight: "bold", size: 11pt, it.body),
)

#show link: it => text(fill: cip-azul, underline(it))
#show raw.where(block: false): it => box(
  fill: cip-suave,
  inset: (x: 3pt, y: 1pt),
  outset: (y: 2pt),
  radius: 2pt,
  text(fill: cip-azul, it),
)

#set table(stroke: (x, y) => (
  top: if y <= 1 { 0.6pt + cip-borde } else { 0pt },
  bottom: 0.6pt + cip-borde,
))
#show table.cell.where(y: 0): set text(weight: "bold", fill: cip-azul)

// --- cajas ------------------------------------------------------------------

#let caja(color, etiqueta, cuerpo) = block(
  width: 100%,
  // Una caja partida por un salto de pagina deja la etiqueta huerfana al pie.
  breakable: false,
  fill: cip-suave,
  stroke: (left: 3pt + color),
  inset: (left: 10pt, rest: 8pt),
  radius: (right: 3pt),
  spacing: 10pt,
  [
    #text(fill: color, weight: "bold", size: 8.5pt, upper(etiqueta))
    #v(-4pt)
    #cuerpo
  ],
)

#let prueba(cuerpo) = caja(cip-verde, "prueba esto", cuerpo)
#let ojo(cuerpo) = caja(cip-tierra, "ojo con esto", cuerpo)
#let nota(cuerpo) = caja(cip-azul, "para entender", cuerpo)

// Tarjeta de prompt: lo que el participante copia y pega tal cual.
// El grid pega las dos filas sin el espacio entre bloques que deja el flujo normal.
#let prompt(agente, texto) = block(
  width: 100%,
  stroke: 0.8pt + cip-borde,
  radius: 4pt,
  clip: true,
  breakable: false,
  spacing: 10pt,
  grid(
    columns: 1,
    block(
      width: 100%,
      fill: cip-azul,
      inset: (x: 10pt, y: 5pt),
      text(fill: white, weight: "bold", size: 9pt, raw(agente)),
    ),
    block(
      width: 100%,
      inset: (x: 10pt, y: 8pt),
      text(size: 9.5pt, style: "italic", texto),
    ),
  ),
)
