// Gemeinsame Gestaltung und kleine Zeichenbausteine, ohne externe Pakete.
#let ink = rgb("#263446")
#let accent = rgb("#2563a6")
#let pale = rgb("#edf4fb")
#let muted = rgb("#64748b")

#let diagram(width: 420, height: 140, body) = {
  set page(width: (width + 24) * 1pt, height: (height + 24) * 1pt,
           margin: 12pt, fill: white)
  set text(font: "DejaVu Sans", size: 10pt, fill: ink)
  set par(leading: 0.4em)
  box(width: width * 1pt, height: height * 1pt, body)
}

#let label(x, y, body, width: 100, size: 10, color: ink) = place(
  top + left, dx: x * 1pt, dy: y * 1pt,
  block(width: width * 1pt)[#align(center)[#text(size: size * 1pt, fill: color, body)]],
)

#let segment(x1, y1, x2, y2, color: ink, thickness: 1.2, dashed: false) = place(
  top + left,
  line(start: (x1 * 1pt, y1 * 1pt), end: (x2 * 1pt, y2 * 1pt),
       stroke: (paint: color, thickness: thickness * 1pt,
                dash: if dashed { "dashed" } else { "solid" })),
)

#let arrow(x1, y, x2, color: accent) = {
  segment(x1, y, x2, y, color: color)
  segment(x2 - 5, y - 3, x2, y, color: color)
  segment(x2 - 5, y + 3, x2, y, color: color)
}

#let frame(x, y, width, height, fill: pale, radius: 5, dashed: false) = place(
  top + left, dx: x * 1pt, dy: y * 1pt,
  rect(width: width * 1pt, height: height * 1pt, fill: fill,
       radius: radius * 1pt,
       stroke: (paint: accent, thickness: 1pt,
                dash: if dashed { "dashed" } else { "solid" })),
)

// Rechteckige IEC-Gattersymbole. XOR wird hier ausschließlich mit zwei Eingängen verwendet.
#let gate(x, y, symbol, inverted: false, unary: false) = {
  frame(x, y, 52, 44, fill: white, radius: 0)
  label(x, y + 12, symbol, width: 52, size: 15)
  if unary {
    segment(x - 20, y + 22, x, y + 22)
  } else {
    segment(x - 20, y + 12, x, y + 12)
    segment(x - 20, y + 32, x, y + 32)
  }
  let output-x = x + 52
  if inverted {
    place(top + left, dx: output-x * 1pt, dy: (y + 18) * 1pt,
          circle(radius: 4pt, fill: white, stroke: 1.2pt + ink))
    output-x += 8
  }
  segment(output-x, y + 22, x + 80, y + 22)
}

#let gate-example(name, symbol, expression, inverted: false, unary: false) = diagram(
  width: 300, height: 136,
  {
    label(0, 0, name, width: 300, size: 13)
    gate(120, 40, symbol, inverted: inverted, unary: unary)
    if unary {
      label(64, 54, [a], width: 24)
    } else {
      label(64, 44, [a], width: 24)
      label(64, 64, [b], width: 24)
    }
    label(210, 54, [y], width: 24)
    label(0, 108, expression, width: 300)
  },
)

// Binäre Signalspur; jeder Eintrag gilt für einen gleich langen Zeitabschnitt.
#let trace(y, values, x: 92, step: 42, amplitude: 20) = {
  for (i, value) in values.enumerate() {
    let level = y - value * amplitude
    segment(x + i * step, level, x + (i + 1) * step, level,
            color: accent, thickness: 1.5)
    if i > 0 and values.at(i - 1) != value {
      segment(x + i * step, y - values.at(i - 1) * amplitude,
              x + i * step, level, color: accent, thickness: 1.5)
    }
  }
}
