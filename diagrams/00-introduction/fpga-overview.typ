#import "../lib/style.typ": *
#diagram(width: 510, height: 376, {
  label(0, 0, [FPGA · programmierbare Logik und Verbindungen], width: 510, size: 13)
  frame(52, 38, 406, 288, fill: rgb("#f8fafc"), radius: 14)

  // Routingkanäle zwischen den Logikblöcken.
  for x in (117, 209, 301, 393) {
    for offset in (-3, 3) {
      segment(x + offset, 68, x + offset, 296, color: rgb("#b5c5d8"), thickness: 0.7)
    }
  }
  for y in (94, 156, 218, 280) {
    for offset in (-3, 3) {
      segment(84, y + offset, 426, y + offset, color: rgb("#b5c5d8"), thickness: 0.7)
    }
  }
  for x in (135, 227, 319) {
    for y in (107, 169, 231) {
      frame(x, y, 56, 36, radius: 4)
      label(x, y + 10, [CLB], width: 56)
      segment(x - 18, y + 18, x, y + 18, color: accent)
      segment(x + 56, y + 18, x + 74, y + 18, color: accent)
    }
  }

  // I/O-Blöcke am Rand verbinden interne Signale mit den Pins.
  let io-fill = rgb("#e7f3ee")
  for x in (145, 237, 329) {
    frame(x, 48, 36, 22, fill: io-fill, radius: 3)
    label(x, 52, [IOB], width: 36, size: 8)
    segment(x + 18, 27, x + 18, 48)
    segment(x + 18, 70, x + 18, 91, color: accent)
    frame(x, 296, 36, 22, fill: io-fill, radius: 3)
    label(x, 300, [IOB], width: 36, size: 8)
    segment(x + 18, 283, x + 18, 296, color: accent)
    segment(x + 18, 318, x + 18, 338)
  }
  for y in (114, 176, 238) {
    frame(62, y, 30, 22, fill: io-fill, radius: 3)
    label(62, y + 4, [IOB], width: 30, size: 8)
    segment(34, y + 11, 62, y + 11)
    segment(92, y + 11, 114, y + 11, color: accent)
    frame(418, y, 30, 22, fill: io-fill, radius: 3)
    label(418, y + 4, [IOB], width: 30, size: 8)
    segment(396, y + 11, 418, y + 11, color: accent)
    segment(448, y + 11, 476, y + 11)
  }
  label(0, 350, [CLB: Logikblock · IOB: Ein-/Ausgangsblock · Linien: Routing], width: 510, size: 9, color: muted)
})
