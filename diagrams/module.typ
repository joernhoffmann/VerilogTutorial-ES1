#import "lib/style.typ": *
#diagram(width: 520, height: 224, {
  label(0, 0, [Aufbau einer Komponente], width: 520, size: 13)

  // Modulgrenze und hervorgehobener Modulname.
  frame(148, 36, 224, 166, radius: 9)
  frame(148, 36, 224, 40, fill: accent, radius: 9)
  label(148, 48, [`module_copy`], width: 224, size: 12, color: white)

  // Anschlüsse außerhalb, Implementierung innerhalb der Modulgrenze.
  label(0, 100, [`e_in`], width: 132)
  label(0, 138, [Eingang · `input`], width: 132, size: 9, color: muted)
  arrow(18, 127, 148)
  label(388, 100, [`a_out`], width: 132)
  label(388, 138, [Ausgang · `output`], width: 132, size: 9, color: muted)
  arrow(372, 127, 502)

  label(158, 89, [Implementierung], width: 204, size: 9, color: muted)
  frame(166, 111, 188, 32, fill: white, radius: 4)
  label(166, 122, [`a_out = e_in`], width: 188, size: 9)
  segment(148, 127, 166, 127, color: accent)
  segment(354, 127, 372, 127, color: accent)
  label(148, 157, [Kontinuierliche Zuweisung · `assign`], width: 224, size: 8, color: muted)
  segment(164, 177, 356, 177, color: rgb("#d6e3f0"), thickness: 0.8)
  label(148, 186, [`endmodule`], width: 224, size: 8, color: muted)
})
