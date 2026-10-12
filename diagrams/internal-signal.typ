#import "lib/style.typ": *
#diagram(width: 420, height: 138, {
  label(0, 0, [Weiterleitung über ein internes Signal], width: 420, size: 13)
  frame(126, 34, 168, 76, dashed: true)
  label(126, 43, [`module_signal`], width: 168, size: 9, color: muted)
  arrow(18, 83, 402)
  label(0, 62, [`signal_in`], width: 110)
  label(132, 62, [`signal_internal`], width: 156)
  label(310, 62, [`signal_out`], width: 110)
  label(0, 118, [Kontinuierliche Verbindung ohne Speicher], width: 420, size: 9, color: muted)
})
