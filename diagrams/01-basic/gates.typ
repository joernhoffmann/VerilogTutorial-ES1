#import "../lib/style.typ": *
#diagram(width: 510, height: 296, {
  label(0, 0, [Logische Gatter · rechteckige IEC-Symbole], width: 510, size: 13)
  for (i, spec) in (
    ([AND], [&], `y = a & b`, false, false),
    ([OR], [≥1], `y = a | b`, false, false),
    ([XOR], [=1], `y = a ^ b`, false, false),
    ([NOT], [1], `y = ~a`, true, true),
    ([NAND], [&], `y = ~(a & b)`, true, false),
    ([NOR], [≥1], `y = ~(a | b)`, true, false),
  ).enumerate() {
    let x = calc.rem(i, 3) * 170
    let y = calc.floor(i / 3) * 125 + 38
    label(x, y, spec.at(0), width: 170, size: 11)
    gate(x + 59, y + 24, spec.at(1), inverted: spec.at(3), unary: spec.at(4))
    if spec.at(4) {
      label(x + 14, y + 38, [a], width: 18, size: 9)
    } else {
      label(x + 14, y + 28, [a], width: 18, size: 9)
      label(x + 14, y + 48, [b], width: 18, size: 9)
    }
    label(x + 144, y + 38, [y], width: 18, size: 9)
    label(x, y + 83, spec.at(2), width: 170, size: 8)
  }
  label(0, 278, [Kreis am Ausgang: Invertierung · XOR hier mit zwei Eingängen], width: 510, size: 9, color: muted)
})
