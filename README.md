# VerilogTutorial-ES1

Lehrinhalte für HDLab im Kurs *Eingebettete Systeme I*.

- `ES1Tutorial.md`: aktives Tutorial mit Lektionen und Übungen.
- `ES1Tutorial.md.sav`: Sicherung des Tutorials vor der Umstrukturierung.
- `diagrams/*.typ`: eine Typst-Quelldatei pro Abbildung.
- `diagrams/lib/style.typ`: gemeinsame Farben, Schrift und Zeichenbausteine.
- `images/generated/*.png`: erzeugte und im Tutorial eingebundene Abbildungen.

## Abbildungen erzeugen

Voraussetzungen: Typst 0.15.1 oder neuer, GNU Make und die Schrift **DejaVu Sans**
(einschließlich DejaVu Sans Mono für Codebeschriftungen).
Es werden keine externen Typst-Pakete benötigt.

```sh
make             # Neue oder geänderte Abbildungen erzeugen
make -j4         # Mehrere Abbildungen parallel erzeugen
make rebuild     # Alle Abbildungen neu erzeugen
make rebuild PPI=240  # Alle PNGs mit höherer Auflösung erzeugen
make clean       # Erzeugte PNGs entfernen; Quellen und alte Bilder behalten
```

Standardauflösung: 180 PPI. Nach Änderungen der Auflösung oder der installierten
Schriften ist `make rebuild` erforderlich. Änderungen an der gemeinsamen
Gestaltung erzeugen beim nächsten `make` alle Abbildungen neu.

Eine neue Abbildung wird als `diagrams/name.typ` angelegt. Das Makefile erkennt
sie automatisch und erzeugt `images/generated/name.png`.

```typst
#import "lib/style.typ": *
#diagram(width: 240, height: 100, {
  frame(60, 20, 120, 50)
  label(60, 36, [Komponente], width: 120)
  arrow(0, 45, 60)
  arrow(180, 45, 240)
})
```

Die Einbindung in HDLab erfolgt ausschließlich als Markdown-Bild:

```markdown
![Beschreibung der Abbildung](./images/generated/name.png)
```

Die erzeugten PNGs werden zusammen mit den Quellen versioniert. HDLab benötigt
zum Anzeigen der Abbildungen keinen Typst-Compiler. Der bestehende
GitHub-Workflow benachrichtigt HDLab bei Änderungen an Tutorial oder Bildern.
Die ursprünglichen Bilder bleiben für die Sicherungsdatei erhalten.

## Zeichenbausteine

`diagram`, `frame`, `label` und `arrow` erstellen Blockdiagramme.
`gate` und `gate-example` zeichnen rechteckige IEC-Gattersymbole mit optionaler
Ausgangsinvertierung. Die Beispiele für XOR verwenden zwei Eingänge.
`trace` zeichnet binäre Signalverläufe aus einer Liste von 0/1-Werten;
jeder Wert gilt für einen gleich langen Zeitabschnitt.

Alle Bilder verwenden einen weißen Hintergrund, dunkle Beschriftungen und
blaue Akzente. Signalverläufe sind didaktische Darstellungen und werden nicht
automatisch aus SystemVerilog simuliert.

Die Gatterübersichten `gates.typ` und `gates-ansi.typ` zeigen dieselben Funktionen
mit IEC- beziehungsweise US-/ANSI-Symbolen. Die US-Konturen sind zentral in
`diagrams/lib/ansi.typ` definiert und werden als Vektoren in Typst gezeichnet.
