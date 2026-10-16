# VerilogTutorial-ES1

Lehrinhalte für HDLab im Kurs *Eingebettete Systeme I*.

- `ES1Tutorial.md`: aktives Tutorial mit Lektionen und Übungen.
- `ES1Tutorial.md.sav`: unveränderte Sicherung vor der Umstrukturierung.
- `diagrams/<kapitel>/`: kleine Typst- oder SVG-Quelldateien pro Abbildung.
- `diagrams/lib/`: gemeinsame Gestaltung und SVG-Exportvorlage.
- `images/<kapitel>/`: erzeugte PNGs und zugehörige externe Bilder.

## Abbildungen erzeugen

Quellen und PNGs verwenden dieselbe Kapitelstruktur. Ein zusätzlicher
Kursordner ist hier nicht nötig, da dieses Repository ausschließlich ES1 enthält.

| Ordner unter `diagrams/` und `images/` | Kapitel |
|--------------------------------------|---------|
| `00-introduction/` | Vorwort, Board und FPGA-Aufbau |
| `01-basic/` | Digitale Grundlagen und Gatter |
| `02-modules/` | Module und Ports |
| `03-signals/` | Signale und Datentypen |
| `05-assignments/` | Kontinuierliche Zuweisungen und Signalverläufe |
| `06-procedural/` | Prozedurale Blöcke und Takt |

Ordner für weitere Kapitel entstehen, sobald sie eine Abbildung benötigen.
Das unveränderte Herstellerfoto liegt unter `images/00-introduction/basys3.png`;
seine Quelle steht unmittelbar am Bild im Tutorial. Die alten `images/model_*`
bleiben an ihrem bisherigen Ort, damit die `.sav`-Sicherung lesbar bleibt.

Voraussetzungen: Typst 0.15.1 oder neuer, GNU Make und die Schrift **DejaVu Sans**
(einschließlich DejaVu Sans Mono für Codebeschriftungen).
Es werden keine externen Typst-Pakete oder zusätzlichen SVG-Konverter benötigt.

```sh
make                 # Neue oder geänderte Abbildungen erzeugen
make -j4             # Mehrere Abbildungen parallel erzeugen
make rebuild         # Alle Abbildungen neu erzeugen
make rebuild PPI=240 # PNGs mit höherer Auflösung erzeugen
make clean           # Erzeugte PNGs entfernen; Foto und alte Bilder behalten
```

Standardauflösung: 180 PPI. Nach Änderungen der Auflösung oder installierter
Schriften ist `make rebuild` erforderlich. Änderungen an gemeinsamen
Zeichenbausteinen erzeugen beim nächsten `make` die Abbildungen neu.

Blockdiagramme, IEC-Gatter und Signalverläufe werden in Typst beschrieben.
Für freie Konturen oder Abbildungen, die sich mit den Typst-Zeichenbausteinen
nicht sinnvoll ausdrücken lassen, eine eigenständige SVG-Datei verwenden.
Die ANSI-Gatterübersicht ist dafür `diagrams/01-basic/gates-ansi.svg`.
Typst übernimmt auch bei SVG den PNG-Export über `diagrams/lib/svg.typ`.
Fotos bleiben Rasterbilder und werden nicht künstlich in SVG umgewandelt.

Neue Abbildungen als `diagrams/01-basic/name.typ` oder
`diagrams/01-basic/name.svg` anlegen. Das Makefile erkennt beide Formate und
erzeugt `images/01-basic/name.png`. Pro Abbildung genau eine Hauptquelle
verwenden. Neue Kapitelordner folgen dem Muster `NN-name`.

```typst
#import "../lib/style.typ": *
#diagram(width: 240, height: 100, {
  frame(60, 20, 120, 50)
  label(60, 36, [Komponente], width: 120)
  arrow(0, 45, 60)
  arrow(180, 45, 240)
})
```

Die Einbindung in HDLab erfolgt als Markdown-Bild:

```markdown
![Beschreibung der Abbildung](./images/01-basic/name.png)
```

Die erzeugten PNGs zusammen mit den Quellen versionieren. HDLab benötigt zum
Anzeigen keinen Typst-Compiler. Sein bestehender Sync übernimmt den Bilderbaum
rekursiv; die Kapitelordner benötigen keine Änderung an der Veröffentlichung.

## Zeichenbausteine

`diagram`, `frame`, `label` und `arrow` erstellen Blockdiagramme.
`gate` und `gate-example` zeichnen rechteckige IEC-Gattersymbole mit optionaler
Ausgangsinvertierung. Die Beispiele für XOR verwenden zwei Eingänge.
`trace` zeichnet binäre Signalverläufe aus einer Liste von 0/1-Werten;
jeder Wert gilt für einen gleich langen Zeitabschnitt.

Alle Diagramme verwenden einen weißen Hintergrund, dunkle Beschriftungen und
blaue Akzente. Signalverläufe sind didaktische Darstellungen und werden nicht
automatisch aus SystemVerilog simuliert.

Die Gatterübersichten `01-basic/gates.typ` und `01-basic/gates-ansi.svg` zeigen
dieselben Funktionen mit IEC- beziehungsweise US-/ANSI-Symbolen.

## Testbenches

Jede Übung enthält eine eigenständig ausführbare SystemVerilog-Testbench.
Benannte Einzelprüfungen zeigen ✅/❌; bei Fehlern folgen Soll- und Istwert.
Alle Prüfungen laufen weiter. `finish_tests()` zeigt die Anzahl bestandener
Prüfungen und das Gesamtergebnis. `TEST_SOLVED=1` beziehungsweise `0` ist die
maschinenlesbare Schnittstelle zur bestehenden HDLab-Auswertung.
Die bisherigen Ergebnisarrays sind dafür nicht erforderlich.

Die Prüfhilfen werden zentral in `testbenches/helpers.svh` gepflegt und in
die Markdown-Testbenches eingebettet. HDLab benötigt somit keine zusätzliche
Include-Datei. Die Größenangabe `VALUE_WIDTH` gilt für die Vergleichswerte;
`assert_equal_signed` ergänzt eine korrekte signed-Ausgabe. Die optionale
Anzeigebreite von `assert_equal` kürzt nur die binäre Anzeige, nicht den Vergleich.
Alle Prüfaufrufe werden mit `all_passed &= ...` verknüpft.

```sh
make testbenches              # Prüfhilfen ins Tutorial übernehmen
make check-testbenches       # Strenge Verilator-Prüfung inkl. Fehlerproben
make check-course           # Metadaten, Links, Ports und Codebeispiele prüfen
make check                  # Kursstruktur und Verilator-Testbenches prüfen
make check-testbenches-iverilog  # Zusätzlich Icarus mit X/Z-Prüfungen
```

Voraussetzungen: Python 3, Verilator, Make und ein C++-Compiler. **Verilator
ist der maßgebliche Simulator**, weil HDLab ihn verwendet. Die Prüfung
kompiliert ohne pauschales `-Wno-fatal`: Warnungen führen wie beim lokalen
HDLab-Entrypoint zum Fehler. Logische Vektoren werden in den ausführbaren
Beispielen vor der Verknüpfung ausdrücklich mit null verglichen.
Die Prüfungen erzeugen ihre Dateien in temporären Verzeichnissen.

Optional prüft `--iverilog` zusätzlich mit Icarus Verilog (`iverilog`, `vvp`).
`--verilator` bleibt als kompatibler Alias erhalten, ist aber nicht mehr nötig.
Ein vorhandener HDLab-Checkout lässt sich zusätzlich über seine tatsächlichen
Backendfunktionen prüfen, ohne Dienste zu starten oder dort Dateien zu ändern:

```sh
python3 scripts/check_testbenches.py --hdlab-source /pfad/zum/HDLab
```

Die Skripte geben die verwendete Verilator-Version aus. Der lokale HDLab-
Dockerfile nennt Version 5.036; zuletzt wurde hier lokal Version 5.048 geprüft.
Ein Test der laufenden oder bereitgestellten HDLab-Instanz ist damit nicht
verbunden.

`testbenches/clocked-example.sv` ist ein vollständiges, geprüftes Beispiel für
spätere getaktete Aufgaben: Hintergrundtakt, `tick()`, synchroner High-Reset,
Datenübernahme, Halten des Wertes und Watchdog. Es ist noch keine zusätzliche
Kursübung. Die Zeitangaben verwenden derzeit die Standardzeiteinheit des
Simulators, damit die unveränderten DUTs keine gemischten Timescales erhalten.

Die aktiven Übungen verwenden kompakte, benannte Fälle einschließlich
Grenzwerten und Zustandswechseln der Eingaben. Bei der Bitselektion werden
beispielsweise alle Eingangspositionen einzeln geprüft; beim Lüfter alle
Schwellen in beiden Richtungen. Diese Auswahl ersetzt die bisherigen langen
Tabellen und Vollsweeps. Ein Timeout verhindert ein endloses Warten.
Der lokale HDLab-Worker läuft höchstens 100 Zeitschritte; die Testbenches
enden vorher, ihr Watchdog meldet nach 90 Einheiten einen Fehler.

X/Z-Tests laufen mit Icarus Verilog als 4-State-Simulator. Im 2-State-Simulator
Verilator werden sie mit einer bedingten Übersetzung ausgelassen, damit die
Ausgabe keine erfolgreiche X/Z-Prüfung vortäuscht. Simulatorläufe und die
Prüfung des Ausgabeprotokolls ersetzen keinen Test einer laufenden HDLab-Instanz.
