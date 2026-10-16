#import "../lib/style.typ": *
#diagram(width: 420, height: 132, {
  label(0, 0, [Ports eines Moduls], width: 420, size: 13)
  frame(142, 37, 136, 65)
  label(142, 48, [`module_ports`], width: 136)
  label(142, 73, [Implementierung], width: 136, size: 9, color: muted)
  arrow(20, 70, 142)
  arrow(278, 70, 400)
  label(0, 44, [`e_in`], width: 136)
  label(284, 44, [`a_out`], width: 136)
  label(0, 88, [`input`], width: 136, size: 9, color: muted)
  label(284, 88, [`output`], width: 136, size: 9, color: muted)
})
