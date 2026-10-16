---
name: hdlab-kurs
description: Lehrinhalte, SystemVerilog-Übungen und Typst-Abbildungen für den HTWK-Kurs Eingebettete Systeme I in VerilogTutorial-ES1 erstellen, didaktisch überarbeiten und prüfen. Verwenden bei Änderungen am HDLab-Tutorial dieses Kurses.
---

# HDLab-Kurs bearbeiten

## Kurskontext

Der Kurs *Eingebettete Systeme I* an der HTWK, Fakultät für
Ingenieurwissenschaften, verwendet das **Basys3-Board**. Auf dessen FPGA
entsteht ein **RISC-V-Prozessorsystem als System-on-Chip (SoC)** mit Prozessor,
Speicher und weiteren Hardwaremodulen. Ziel ist ein Gaming-System, das im
Verlauf des Kurses schrittweise um in SystemVerilog beschriebene Module
erweitert wird.

Das Tutorial vermittelt die Sprache und grundlegende Entwurfsmethoden.
Es soll die spätere Entwicklung der Kursmodule ermöglichen. Beispiele
müssen nicht schon einen vollständigen Prozessor oder ein Spiel enthalten.
Die Projektbeschreibung gehört in **0.1 Ziel**, nicht als ausführliche
Wiederholung ins Vorwort. Das Vorwort benötigt kein Schaltungsbeispiel.

Die aktive Datei ist `ES1Tutorial.md` im Repository. Für technische Vorgaben,
Metadaten, Marker und Build die `AGENTS.md` im Repository beachten. Den
aktuellen Inhalt der betroffenen und benachbarten Lektionen lesen.

## Sprache und Didaktik

Sachlich und verständlich schreiben, wie in einem Hochschultutorial:
keine persönliche Ansprache, kein erzählendes „wir“, keine flapsigen
Formulierungen und kein unnötig akademischer Stil. Fachbegriffe erklären,
bevor sie für eine Erklärung benötigt werden. Durchgearbeitete Beispiele
statt bloßer Behauptungen verwenden.

Den Einstieg kompakt halten: nur Konzepte erklären, die für die jeweilige
Lektion und ihre Übung benötigt werden. Im aktuellen Einführungstext keine
X/Z-Zustände oder Simulatorvergleiche behandeln. Zusätzliche Datentypen,
bidirektionale Ports, Zweierkomplement-Sonderfälle und Vorzeichenerweiterung
nicht vorziehen. Nötige Rechenschritte und konkrete Beispiele erhalten;
Kürzen darf keine fachlich falschen Vereinfachungen erzeugen.

Eine Lektion soll einen nachvollziehbaren Lernschritt bilden:

- An vorhandenes Wissen anschließen und das neue Konzept erklären.
- Mit einem konkreten Beispiel zeigen, wie es funktioniert.
- Notwendige Schritte und Zwischenergebnisse sichtbar machen.
- Typische Verwechslungen erklären, wenn sie für das Konzept relevant sind.
- Zur anschließenden einfachen Übung hinführen.

Ab Kapitel 1 in der Regel Lektion und einfache Übung abwechseln. Jede
inhaltliche Lektion enthält ein passendes Beispiel. Kapitelauftakte und
Zielbeschreibung benötigen kein künstlich eingefügtes Codebeispiel.
Bei Änderungen an einer einzelnen Lektion nur die abhängigen Nachbarinhalte
anpassen; keine umfassende Umstrukturierung ohne Auftrag.

## Aufbau von Übungen

Überschrift mit der Nummer der zugehörigen Lektion, einem Buchstaben und
Doppelpunkt, beispielsweise **„3.3.a. Übung: Bitselektion“** nach Lektion 3.3.
Mehrere Übungen zu derselben Lektion erhalten a, b, c usw. Die `lesson_id`
bleibt unabhängig davon numerisch und bestimmt weiterhin die Reihenfolge.
Metadatentitel und Inhaltsverzeichnis an die sichtbare Überschrift anpassen.

Danach eine kurze Beschreibung von Zweck und Funktion. Es folgen:

### Schnittstelle

Eine Tabelle mit **Port | Richtung | Typ | Beschreibung**.
Namen, Bitbreiten und signed/unsigned-Interpretation müssen dem Modul
entsprechen. Ports erhalten keine „binäre“ oder „hexadezimale“ Hardwareart;
die Zahlenbasis beschreibt die Schreibweise der Konstanten.

### Verhalten

Stichpunkte mit beobachtbaren Anforderungen: Eingangswerte, Ausgangswerte,
Grenzen, zeitliches Verhalten und gegebenenfalls Zustandsabhängigkeit.
Beispiele und Grenzfälle verwenden, wenn sie Unklarheiten vermeiden.

### Realisierung

Stichpunkte mit den zur Lektion passenden Umsetzungsvorgaben, etwa
kontinuierliche Zuweisung, bedingter Operator, erlaubte Operatoren,
Bitbreiten, Priorität oder Speicherelemente. Vorgaben wie „keine
`always`-Blöcke“ gelten für die jeweiligen kombinatorischen Übungen,
nicht automatisch für spätere sequentielle Aufgaben.

Überlappende Bedingungen, Priorität und fehlende Hysterese nur erwähnen,
wenn sie für die betreffende Aufgabe relevant sind. Kein Wissen über
Bausteine voraussetzen, das noch nicht eingeführt wurde, außer das
Codegerüst gibt diese Teile vollständig vor.

Anschließend die vorhandenen HDLab-Bereiche für Codegerüst, Musterlösung
und Testbench verwenden. Tests prüfen funktionale Anforderungen; rein
syntaktische Vorgaben wie ein bestimmter Operator benötigen zusätzlich
eine Sichtprüfung der Musterlösung.

## Testbenches

Benannte Einzelprüfungen mit ✅/❌ und aussagekräftigen Beschreibungen verwenden.
Fehler nennen Ausgang, Eingangssituation, Soll- und Istwert. Am Ende stehen
Anzahl bestandener Prüfungen und ein mit UND verknüpftes Gesamtergebnis.
Das Format `TEST_SOLVED=1` beziehungsweise `0` ermöglicht HDLab die Auswertung
ohne Ergebnisarrays. Ein Fehler darf die folgenden Prüfungen nicht verhindern.
Keine ausgeführten Prüfungen oder ein Timeout müssen zum Fehlschlag führen.

Die Hilfen `assert_equal`, `assert_equal_signed`, `assert_true` und
`finish_tests` liegen in `testbenches/helpers.svh`. Im Tutorial müssen sie
innerhalb jeder Testbench eingebettet sein; `make testbenches` synchronisiert
sie. Vergleiche verwenden `===`. `VALUE_WIDTH` muss den breitesten geprüften
Wert aufnehmen; schmalere Werte bei Bedarf explizit erweitern. Signed-Werte
mit der signed-Prüfhilfe vergleichen. Die optionale Anzeigebreite von
`assert_equal` verändert nicht die Vergleichsbreite.

Gezielte Fälle, Grenzwerte und Rückkehr zu früheren Eingaben auswählen.
Sollwerte möglichst unabhängig von der Musterlösung festlegen. Kapitel 6 führt kombinatorische und getaktete prozedurale Blöcke ein.
Kapitel 5 und 6 sind `beginner`, Kapitel 0–4 sind `intro`. Für getaktete Aufgaben zeigt
`testbenches/clocked-example.sv` Takterzeugung, `tick()` und einen synchronen,
High-aktiven Reset. Reset-Semantik jeweils aus der Aufgabe ableiten. Eingänge
an der fallenden Flanke ändern und nach der steigenden Flanke erst nach den
Nonblocking-Zuweisungen prüfen. Jeder Ablauf benötigt einen Timeout.

HDLab verwendet Verilator mit zwei Zuständen. `make check-testbenches` muss
standardmäßig Verilator mit fatalen Warnungen verwenden. Auch fehlerhafte
Lösungen und die Prüfhilfen damit testen; Icarus ist nur eine optionale
Ergänzung. Vollständige Codebeispiele mit `make check-course` prüfen.
X/Z-Prüfungen nur im
4-State-Simulator ausführen und in Verilator nicht als bewiesene Eigenschaft
ausgeben. Der lokale HDLab-Worker begrenzt den Lauf auf 100 Zeitschritte;
die aktuellen Testbenches beenden sich vorher oder melden über den Watchdog
einen Fehler. Bei künftigen längeren Tests muss die Laufzeitunterstützung
geprüft werden.

## Fachliche Leitlinien

- Zahlenwert, Bitmuster, Zahlenbasis, Bitbreite und Vorzeicheninterpretation
  getrennt erklären. Bei Beispielen die verwendete Interpretation angeben.
- Zweierkomplement über negative Stellengewichte erklären, dann die
  Bildung durch Invertieren und Addieren von 1 herleiten. Den Wertebereich
  mit einem Beispiel zeigen; Überlauf und Vorzeichenerweiterung erst bei
  einer passenden späteren Aufgabe vertiefen.
- Hardwarebeschreibung und CPU-Programm unterscheiden. Die Reihenfolge
  kontinuierlicher Zuweisungen ist keine zeitliche Ausführungsfolge.
- Den vereinbarten deutschen Begriff **kontinuierliche Zuweisung (`assign`)**
  verwenden. „Kombinatorisch“ beschreibt die Logik, nicht das Synonym für
  jede Art nebenläufiger Anweisung.
- Simulation und Synthese unterscheiden. Testbench-Verzögerungen und
  Konsolenausgaben sind keine Bestandteile der beschriebenen Hardware.
- Generische FPGA-Prinzipien und konkrete Artix-7-Ressourcen unterscheiden.
  Gerätespezifische Angaben anhand von AMD-/Digilent-Dokumentation prüfen.

## Abbildungen und Abschluss

Bestehende Typst-Zeichenbausteine bevorzugen. Neue Abbildungen als kleine
`diagrams/*.typ`-Dateien erstellen und per `make` nach
`images/generated/*.png` exportieren. Die PNGs tatsächlich im aktuellen
Tutorial einbinden und visuell prüfen. Nicht aus einem erfolgreichen Build
schließen, dass die Markdown-Verweise bereits ersetzt wurden.

Die Originalbilder und `.sav`-Datei für den bisherigen Kursstand erhalten.
Externe Bildquellen direkt an der Abbildung nennen. Eine eigene vereinfachte
Zeichnung als solche kennzeichnen und die fachliche Referenz verlinken.

Nach der aufgabengerechten Prüfung kurz berichten, was geändert wurde,
welche Prüfungen tatsächlich liefen und welche Einschränkungen bestehen.
