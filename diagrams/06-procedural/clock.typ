#import "../lib/style.typ": *
#diagram(width: 500, height: 184, {
  label(0, 0, [Takt · Flanken und Periodendauer], width: 500, size: 13)
  label(72, 35, [steigend (`posedge`)], width: 124, size: 9)
  label(198, 35, [fallend (`negedge`)], width: 124, size: 9)
  for x in (134, 260) {
    segment(x, 53, x, 66, color: muted, thickness: 0.8)
    segment(x - 3, 62, x, 66, color: muted, thickness: 0.8)
    segment(x + 3, 62, x, 66, color: muted, thickness: 0.8)
  }
  for i in range(9) {
    segment(92 + i * 42, 70, 92 + i * 42, 104,
            color: rgb("#dbe3ec"), thickness: 0.6, dashed: true)
    label(80 + i * 42, 114, str(i * 5), width: 24, size: 8, color: muted)
  }
  label(0, 83, [`clk_in`], width: 50)
  label(53, 65, [1], width: 20, size: 8, color: muted)
  label(53, 93, [0], width: 20, size: 8, color: muted)
  trace(100, (0, 1, 0, 1, 0, 1, 0, 1), amplitude: 28)
  label(434, 114, [Zeit / ns], width: 66, size: 8, color: muted)
  segment(134, 138, 134, 150, color: muted, thickness: 0.8)
  segment(218, 138, 218, 150, color: muted, thickness: 0.8)
  segment(134, 144, 218, 144, color: accent)
  label(126, 158, [T = 10 ns], width: 100, size: 10)
  label(278, 158, [f = 100 MHz], width: 180, size: 10)
})
