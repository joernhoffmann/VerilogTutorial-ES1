#import "../lib/style.typ": *
#diagram(width: 420, height: 156, {
  label(0, 0, [Weiterleitung und konstanter Ausgang], width: 420, size: 13)
  arrow(76, 58, 350)
  label(0, 50, [`e_in`], width: 54)
  label(364, 50, [`a1_out`], width: 54)
  label(104, 35, [`assign a1_out = e_in;`], width: 220, size: 9, color: muted)
  frame(42, 98, 34, 30, radius: 3)
  label(42, 105, [1], width: 34)
  arrow(76, 113, 350)
  label(364, 105, [`a2_out`], width: 54)
  label(104, 89, [`assign a2_out = 1'b1;`], width: 220, size: 9, color: muted)
})
