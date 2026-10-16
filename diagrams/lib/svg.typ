// SVG in natürlicher Größe auf einer weißen Seite als PNG rendern.
#set page(width: auto, height: auto, margin: 0pt, fill: white)
#image(sys.inputs.at("svg"))
