# Arbeitsregeln für VerilogTutorial-ES1

## Zweck und Einstieg

Dieses Repository enthält die Lehrinhalte für HDLab im Hochschulkurs
*Eingebettete Systeme I*. Es enthält nicht den Anwendungscode von HDLab.

Für die Bearbeitung von Lektionen, Übungen und Abbildungen den lokalen
Kurs-Skill [skills/hdlab-kurs/SKILL.md](skills/hdlab-kurs/SKILL.md) lesen.
Er beschreibt Kursziel, didaktische Anforderungen und redaktionellen Stil.
Die [README.md](README.md) erläutert den Aufbau und den Bildexport.

## Dateien und bestehende Änderungen

- `ES1Tutorial.md` ist die aktive Inhaltsquelle für HDLab.
- `ES1Tutorial.md.sav` ist die Sicherung vor der Umstrukturierung. Als Quelle
  für die Übernahme vorhandener Inhalte lesen, aber nicht nebenbei ändern.
- `diagrams/NN-kapitel/*.typ` und `*.svg` enthalten die Abbildungsquellen.
- `diagrams/lib/*.typ` enthält gemeinsame Zeichenbausteine und Gestaltung.
- `images/NN-kapitel/*.png` enthält die abgeleiteten Diagramme.
- `images/00-introduction/basys3.png` enthält das bereitgestellte Herstellerfoto.
- Alte Bilder unter `images/model_*` bleiben für die Sicherung erhalten;
  im aktiven Tutorial die neuen Diagramme verwenden.

Vor einer Änderung den aktuellen Dateistand lesen. Nicht von früheren
Beschreibungen oder einem früheren Tool-Ergebnis auf die jetzigen Inhalte
schließen. Bestehende Benutzeränderungen außerhalb der Aufgabe erhalten.

## HDLab-Schnittstelle

Jede Lektion beginnt mit einem HTML-Kommentar mit folgenden Metadaten:

```markdown
<!--
lesson_id: 101
lesson_title: "1.1 Binär und Hexadezimal"
difficulty: "intro"
duration_min: 15
type: "theory"
-->
```

- `lesson_id` bestimmt Kapitelzuordnung und Reihenfolge. `000` ist der
  Auftakt von Kapitel 0, `100` der Auftakt von Kapitel 1, `101` dessen
  erste Unterlektion. Kapitel 10 beginnt entsprechend mit `1000`.
- IDs müssen eindeutig sein und in der Datei aufsteigend angeordnet werden.
- Bei Umstellungen IDs, sichtbare Nummerierung, `lesson_title`,
  Inhaltsverzeichnis und betroffene Querverweise gemeinsam anpassen.
- Kapitel 0–4 tragen `difficulty: "intro"`, Kapitel 5–6 einschließlich
  ihrer Übungen `difficulty: "beginner"`.
  `type` ist `theory` oder `exercise`.
- `duration_min` soll zum tatsächlichen Umfang passen.
- SystemVerilog-Codeblöcke bleiben für HDLab als `verilog` ausgezeichnet.

Übungen enthalten diese drei Bereiche mit exakt geschriebenen Markern:

```text
**EXERCISE_START** ... **EXERCISE_END**
**SOLUTION_START** ... **SOLUTION_END**
**TESTBENCH_START** ... **TESTBENCH_END**
```

Jeder Bereich enthält einen eigenen `verilog`-Codeblock. Testbenches sind
portlose Module mit benannten Einzelprüfungen, ✅/❌-Ausgaben, Soll-/Istwerten
bei Fehlern und einer abschließenden Zusammenfassung. Alle Prüfergebnisse
werden mit `all_passed &= assert_equal(...)` (beziehungsweise der passenden
Prüffunktion) verknüpft. Kein Kurzschluss-UND verwenden, das Folgeprüfungen
überspringen könnte.

`finish_tests()` gibt genau eine Zeile `TEST_SOLVED=1` beziehungsweise
`TEST_SOLVED=0` aus. Die bestehende HDLab-Auswertung erkennt diese Zeile direkt;
`test_array`, `test_solved`, `TEST_LENGTH` und `TEST_WIDTH` sind nicht mehr nötig.
Die zentrale Quelle der eingebetteten Prüfhilfen ist `testbenches/helpers.svh`.
Nach Änderungen `make testbenches` ausführen. Im Markdown sind die Hilfen
vollständig eingebettet, da HDLab keine zusätzlichen Includes mitliefert.
Modulnamen, Ports, Breiten und Testbench-Instanz müssen zusammenpassen.
Portnamen folgen der Konvention im Kurs-Skill: `_in`/`_out`, kurze
Einbuchstabennamen nur sparsam am Anfang; später deskriptivere Namen wie
`signal_in`/`signal_out` oder Funktionsnamen. Takt/Reset: `clk_in`/`rst_in`.
Die TB-Signale wie die angeschlossenen DUT-Ports benennen. Absichtlich noch
zu ergänzende Ports im Codegerüst mit Richtung und Namen als Kommentar
vorgeben. `make check-course` prüft dies einschließlich Bitbreite und Vorzeichen.
Bei reinen Text- oder Layoutänderungen die Codebereiche erhalten.

## Abbildungen

Die Diagramme werden mit **Typst oder eigenständigen SVG-Quellen** erstellt,
mit PNG-Ausgabe für HDLab. Typst bleibt auch für SVG der PNG-Renderer.
Die früher diskutierten Mermaid-, PlantUML- und TikZ-Varianten sind nicht
mehr der gewählte Buildweg.

- Gemeinsam gestaltete kleine Quelldateien verwenden. Typst für technische
  Diagramme, eigenständiges SVG für freie Konturen oder Grenzen der
  Typst-Zeichenbausteine; externe Pakete sind derzeit nicht erforderlich.
- Quellen und Bilder nach Kapiteln ordnen, etwa `diagrams/01-basic/` und
  `images/01-basic/`. Fotos bleiben unveränderte Rasterbilder.
- Schrift: DejaVu Sans, für Code DejaVu Sans Mono; weißer Hintergrund,
  dunkle Beschriftung und blaue Akzente.
- Gatterübersichten in IEC- und US-/ANSI-Darstellung erhalten.
- Abbildungen im Tutorial als relative Markdown-Bildverweise auf PNGs
  einbinden. Keine Typst-Quellen als Ersatz für das sichtbare Bild einbetten.
- Für Herstellerfotos und externe Vorlagen Herkunft und Quellenlink angeben.
- Vereinfachte Architekturdiagramme ausdrücklich als solche kennzeichnen.

```sh
make             # Neue und geänderte Diagramme bauen
make -j4         # Parallel bauen
make rebuild     # Vollständig neu bauen
make rebuild PPI=240
```

Das Makefile erkennt `.typ`- und `.svg`-Hauptquellen in
`diagrams/NN-kapitel/` automatisch. Pro Abbildung genau eine Hauptquelle. Nach Änderungen
an einer Bibliothek alle betroffenen PNGs bauen und visuell prüfen.
Die erzeugten PNGs gehören zusammen mit den Quellen zum Repository.

## Prüfung nach Änderungen

Die Prüfung auf den geänderten Inhalt beschränken:

- Bei redaktionellen Änderungen: Fachlichkeit, vorausgesetztes Wissen,
  Beispiele, Metadaten, Inhaltsverzeichnis und Bildverweise prüfen.
- Bei Codeänderungen: `make check-testbenches` ausführen. Maßgeblich ist
  **Verilator**, da HDLab diesen Simulator verwendet. Ohne pauschales
  `-Wno-fatal` kompilieren, wie im HDLab-Entrypoint. Musterlösungen,
  gezielt fehlerhafte Varianten, Prüfhilfen und das Taktbeispiel prüfen;
  `TEST_SOLVED` kontrollieren, nicht nur den Prozessstatus.
- `make check-course` prüft die Kursstruktur und vollständige Codebeispiele
  mit strengem Verilator-Lint. `make check` führt beide Prüfungen aus.
- `make check-testbenches-iverilog` ergänzt die Prüfung um Icarus und X/Z.
  Diese 4-State-Prüfung ist kein Nachweis für das Verhalten in HDLab.
  Alle Simulatorprüfungen verwenden isolierte temporäre Dateien.
- Bei Abbildungen: PNGs erzeugen, Bildverweise prüfen und die tatsächlichen
  Bilder auf Lesbarkeit, Überlappungen, abgeschnittene Elemente und
  fachlich richtige Verbindungen ansehen.
- Abschließend `git diff --check` ausführen.

## Veröffentlichung

Der Workflow `.github/workflows/notify-hdlab.yml` benachrichtigt das separate
HDLab-Repository bei einem Push auf `main`, wenn das Tutorial oder die Bilder
geändert wurden. Lokales Bearbeiten und `make` veröffentlichen noch nichts.
Nicht ohne entsprechenden Auftrag pushen, einen Dispatch auslösen oder die
Veröffentlichungskonfiguration ändern.
