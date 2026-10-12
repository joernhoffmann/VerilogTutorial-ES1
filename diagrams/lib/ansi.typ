#import "style.typ": *

// US-/ANSI-Gatterkonturen als Vektorpfade, von Typst direkt gerendert.
// Gleiche Abmessungen und Anschlusspositionen wie die IEC-Bausteine.
#let ansi-gate(x, y, kind) = {
  let unary = kind == "not"
  let inverted = kind in ("not", "nand", "nor")
  let curved = kind in ("or", "nor", "xor")
  let outline = if unary {
    "M0 0 L44 22 L0 44 Z"
  } else if curved {
    "M0 0 Q32 0 52 22 Q32 44 0 44 Q20 22 0 0 Z"
  } else {
    "M0 0 H30 C42 0 52 10 52 22 C52 34 42 44 30 44 H0 Z"
  }
  let leads = if unary {
    "M-20 22 H0"
  } else if curved {
    // Schnittpunkte mit der konkaven Eingangskontur bei y=12 und y=32.
    "M-20 12 H7.934 M-20 32 H7.934"
  } else {
    "M-20 12 H0 M-20 32 H0"
  }
  let bubble = if inverted {
    let center = if unary { 48 } else { 56 }
    "<circle cx='" + str(center) + "' cy='22' r='4' fill='white'/>"
  } else { "" }
  let out-start = if inverted {
    if unary { 52 } else { 60 }
  } else { 52 }
  let extra = if kind == "xor" {
    "<path d='M-6 0 Q14 22 -6 44' fill='none'/>"
  } else { "" }
  let svg = ("<svg xmlns='http://www.w3.org/2000/svg' width='102' height='46' viewBox='-21 -1 102 46'>"
    + "<g stroke='#263446' stroke-width='1.2' stroke-linejoin='round' fill='white'>"
    + "<path d='" + outline + "'/>" + extra + bubble
    + "<path d='" + leads + " M" + str(out-start) + " 22 H80' fill='none'/>"
    + "</g></svg>")
  place(top + left, dx: (x - 21) * 1pt, dy: (y - 1) * 1pt,
        image(bytes(svg), format: "svg", width: 102pt, height: 46pt))
}
