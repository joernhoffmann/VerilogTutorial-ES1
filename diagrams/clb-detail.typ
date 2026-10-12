#import "lib/style.typ": *
#diagram(width: 600, height: 344, {
  label(0, 0, [CLB · Logik berechnen und Ergebnisse speichern], width: 600, size: 13)
  frame(76, 34, 448, 86, radius: 8)
  label(76, 43, [Ein CLB der Artix-7-Familie enthält zwei Slices], width: 448, size: 10)
  for (x, name) in ((90, [Slice 0]), (310, [Slice 1])) {
    frame(x, 64, 200, 44, fill: white, radius: 4)
    label(x, 69, name, width: 200, size: 10)
    label(x, 89, [4 LUTs · 8 Flip-Flops · Carry-Logik], width: 200, size: 8, color: muted)
  }
  label(0, 134, [Ein vereinfachter Signalpfad innerhalb eines Slices], width: 600, size: 10, color: muted)

  frame(106, 182, 108, 62, radius: 5)
  label(106, 194, [LUT], width: 108, size: 12)
  label(106, 218, [Logische Funktion], width: 108, size: 8, color: muted)
  arrow(12, 213, 106)
  label(0, 187, [Eingänge], width: 98, size: 9)

  frame(280, 210, 100, 44, radius: 5)
  label(280, 219, [Flip-Flop], width: 100, size: 10)
  label(280, 238, [D → Q], width: 100, size: 8, color: muted)
  segment(214, 213, 244, 213, color: accent)
  segment(244, 213, 244, 232, color: accent)
  arrow(244, 232, 280)
  arrow(380, 232, 454)

  // Der zweite Pfad umgeht das Speicherelement.
  segment(244, 213, 244, 184, color: accent)
  arrow(244, 184, 454)
  label(250, 166, [Direkt], width: 170, size: 8, color: muted)
  label(380, 244, [Gespeichert], width: 74, size: 8, color: muted)
  place(top + left, dx: 241.5pt, dy: 210.5pt,
        circle(radius: 2.5pt, fill: accent, stroke: none))

  frame(454, 170, 66, 86, fill: white, radius: 4)
  label(454, 197, [MUX], width: 66, size: 12)
  label(454, 220, [Auswahl], width: 66, size: 8, color: muted)
  arrow(520, 213, 590)
  label(520, 188, [Ausgang], width: 80, size: 9)

  // Takt und Konfiguration sind verschiedene Steuersignale.
  segment(330, 285, 330, 254, color: accent)
  segment(327, 259, 330, 254, color: accent)
  segment(333, 259, 330, 254, color: accent)
  label(280, 290, [Takt · CLK], width: 100, size: 9)
  segment(487, 285, 487, 256, color: muted)
  segment(484, 261, 487, 256, color: muted)
  segment(490, 261, 487, 256, color: muted)
  label(427, 290, [Konfiguration], width: 120, size: 9, color: muted)
  label(0, 327, [Weitere Signalpfade, Multiplexer, Carry- und Steuerlogik sind nicht dargestellt.], width: 600, size: 8, color: muted)
})
