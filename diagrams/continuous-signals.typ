#import "lib/style.typ": *
#diagram(width: 470, height: 198, {
  label(0, 0, [Signalverlauf einer kontinuierlichen Zuweisung], width: 470, size: 13)
  label(0, 26, [`assign y = a & b;`], width: 470, size: 10, color: muted)
  for i in range(9) {
    segment(92 + i * 42, 52, 92 + i * 42, 172,
            color: rgb("#dbe3ec"), thickness: 0.6, dashed: true)
    label(82 + i * 42, 179, str(i), width: 20, size: 8, color: muted)
  }
  label(0, 64, [`a`], width: 68)
  label(0, 104, [`b`], width: 68)
  label(0, 144, [`y`], width: 68)
  trace(88, (0, 1, 1, 0, 0, 1, 1, 0))
  trace(128, (0, 0, 1, 1, 0, 0, 1, 1))
  trace(168, (0, 0, 1, 0, 0, 0, 1, 0))
})
