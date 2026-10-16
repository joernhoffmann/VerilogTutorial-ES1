#!/usr/bin/env python3
"""Metadaten, Markdown-Verweise, Übungsstruktur und vollständige Codebeispiele prüfen."""
from collections import Counter
from pathlib import Path
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def slug(text):
    text = re.sub(r"<!--.*?-->", "", text).lower().strip()
    return re.sub(r"[^\w\s-]", "", text).replace(" ", "-")


def module_ports(code):
    clean = re.sub(r"//[^\n]*|/\*.*?\*/", "", code, flags=re.S)
    match = re.search(r"\bmodule\s+(\w+)\s*\((.*?)\);", clean, re.S)
    require(match is not None, "Modul mit Portliste fehlt")
    ports = {}
    for item in match.group(2).split(","):
        words = item.split()
        if not words:
            continue
        require(words[0] in ("input", "output", "inout"), f"Nicht unterstützte Portdeklaration: {item}")
        ports[words[-1]] = (words[0], " ".join(words[1:-1]) or "wire")
    return match.group(1), ports


def check_port_names(ports):
    for name, (direction, _) in ports.items():
        suffix = {"input": "_in", "output": "_out", "inout": "_io"}[direction]
        require(name.endswith(suffix), f"Port {name}: Richtungssuffix {suffix} fehlt")
        require(name not in ("clk", "rst", "clk_i", "rst_i"), f"Port {name}: clk_in/rst_in verwenden")


def signal_shape(kind):
    # Wire und logic sind als TB-Verbindung kompatibel; Breite/Vorzeichen müssen passen.
    width = re.search(r"\[[^]]+\]", kind)
    return ("signed" in kind.split(), re.sub(r"\s+", "", width.group()) if width else "[0:0]")


def check_interfaces(identifier, blocks, solution_ports):
    solution_name, _ = module_ports(blocks["SOLUTION"])
    check_port_names(solution_ports)
    scaffold_name, scaffold_ports = module_ports(blocks["EXERCISE"])
    require(scaffold_name == solution_name, f"{identifier}: Modulname im Codegerüst abweichend")
    require(set(scaffold_ports) <= set(solution_ports), f"{identifier}: Zusätzliche/falsch benannte Ports im Codegerüst")
    for name, declaration in scaffold_ports.items():
        require(declaration == solution_ports[name], f"{identifier}: Port {name} im Codegerüst abweichend")
    header = blocks["EXERCISE"].split(");", 1)[0]
    for name in set(solution_ports) - set(scaffold_ports):
        direction = {"input": "Eingang", "output": "Ausgang", "inout": "Ein-/Ausgang"}[solution_ports[name][0]]
        require(re.search(r"//[^\n]*\b" + re.escape(direction) + r"\s+" + re.escape(name) + r"\b", header),
                f"{identifier}: Fehlender Port {name} muss im Codegerüst namentlich vorgegeben sein")
    bench = blocks["TESTBENCH"].split("// END TEST HELPERS", 1)[-1]
    instance = re.search(r"\b(\w+)\s+dut\s*\((.*?)\);", bench, re.S)
    require(instance is not None and instance.group(1) == solution_name, f"{identifier}: DUT-Modulname passt nicht")
    connections = dict(re.findall(r"\.(\w+)\s*\(\s*(\w+)\s*\)", instance.group(2)))
    require(set(connections) == set(solution_ports), f"{identifier}: DUT-Portanschlüsse fehlen oder sind falsch benannt")
    declarations = {}
    for kind, variables in re.findall(r"^\s*((?:logic|wire|reg)(?:\s+signed)?(?:\s*\[[^]]+\])?)\s+([^;]+);", bench, re.M):
        for variable in variables.split(","):
            name = variable.split("=", 1)[0].strip()
            declarations[name] = kind
    for port, signal in connections.items():
        require(port == signal, f"{identifier}: TB-Signal {signal} soll wie Port {port} heißen")
        require(signal in declarations, f"{identifier}: TB-Signal {signal} nicht deklariert")
        require(signal_shape(declarations[signal]) == signal_shape(solution_ports[port][1]),
                f"{identifier}: Breite/Vorzeichen des TB-Signals {signal} passt nicht")


def check_figures():
    outputs = set()
    sources = sorted((ROOT / "diagrams").glob("[0-9][0-9]-*/*"))
    for source in sources:
        if source.suffix not in (".typ", ".svg"):
            continue
        target = ROOT / "images" / source.relative_to(ROOT / "diagrams").with_suffix(".png")
        require(target not in outputs, f"Mehrere Hauptquellen für {target.relative_to(ROOT)}")
        outputs.add(target)
        require(target.is_file(), f"PNG zur Quelle fehlt: {source.relative_to(ROOT)}")
        require(target.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"), f"Ungültiger PNG-Export: {target}")
        if source.suffix == ".svg":
            require(ET.parse(source).getroot().tag == "{http://www.w3.org/2000/svg}svg",
                    f"Keine SVG-Quelle: {source.relative_to(ROOT)}")
    require(outputs, "Keine kapitelweise geordneten Abbildungsquellen gefunden")
    require(not list((ROOT / "diagrams").glob("*.typ")), "Typst-Quelle ohne Kapitelordner")
    require(not list((ROOT / "diagrams").glob("*.svg")), "SVG-Quelle ohne Kapitelordner")
    return len(outputs)


def main():
    figure_count = check_figures()
    text = (ROOT / "ES1Tutorial.md").read_text()
    matches = list(re.finditer(r"<!--\s*\nlesson_id: (\d+)\n(.*?)-->", text, re.S))
    ids = [int(match.group(1)) for match in matches]
    require(ids == sorted(set(ids)), "lesson_ids nicht eindeutig/aufsteigend")
    require(bool(ids), "Keine Lektionen gefunden")
    without_code = re.sub(r"```.*?```", "", text, flags=re.S)
    headings = re.findall(r"^#{1,6} (.+)$", without_code, re.M)
    seen = Counter()
    anchors = set()
    for heading in headings:
        base = slug(heading)
        anchors.add(base if not seen[base] else f"{base}-{seen[base]}")
        seen[base] += 1
    for anchor in re.findall(r"\]\(#([^)]+)\)", without_code):
        require(anchor in anchors, f"Inhaltsverzeichnis: #{anchor} ohne Ziel")
    images = re.findall(r"!\[([^]]*)\]\(([^)]+)\)", without_code)
    for alt, reference in images:
        require(bool(alt.strip()), f"Bild ohne Beschreibung: {reference}")
        require(re.fullmatch(r"(?:\./)?images/\d{2}-[a-z0-9-]+/[^/]+\.png", reference),
                f"Aktives Bild ohne Kapitelordner: {reference}")
        file = ROOT / reference
        require(file.is_file(), f"Bild fehlt: {reference}")
        require(file.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"), f"Kein PNG: {reference}")
        require("model_" not in reference, f"Altes Bild im aktiven Tutorial: {reference}")
    helper = (ROOT / "testbenches/helpers.svh").read_text().strip()
    previous = None
    exercise_index = 0
    exercises = 0
    examples = 0
    fragments = 0
    for i, match in enumerate(matches):
        body = text[match.end():matches[i + 1].start() if i + 1 < len(matches) else len(text)]
        metadata = dict(re.findall(r'^(\w+):\s*"?([^"\n]+)"?$', match.group(0), re.M))
        identifier = match.group(1)
        expected_difficulty = "beginner" if 500 <= int(identifier) < 700 else "intro"
        require(metadata.get("difficulty") == expected_difficulty, f"{identifier}: difficulty muss {expected_difficulty} sein")
        require(metadata.get("type") in ("theory", "exercise"), f"{identifier}: ungültiger type")
        require(int(metadata.get("duration_min", "-1")) >= 0, f"{identifier}: ungültige Dauer")
        title = metadata["lesson_title"]
        heading = re.search(r"^#{2,3} (.+)$", body, re.M)
        require(heading is not None and heading.group(1) == title, f"{identifier}: Titel/Überschrift verschieden")
        if metadata["type"] == "exercise":
            exercises += 1
            require(previous is not None, f"{identifier}: Übung ohne vorausgehende Lektion")
            expected = f"{previous}.{chr(ord('a') + exercise_index)}. Übung:"
            require(title.startswith(expected), f"{identifier}: Übungsnummer passt nicht zur Lektion")
            exercise_index += 1
            for part in ("Schnittstelle", "Verhalten", "Realisierung"):
                require(body.count("#### " + part) == 1, f"{identifier}: Abschnitt {part} fehlt/doppelt")
            require("| Port | Richtung | Typ | Beschreibung |" in body, f"{identifier}: Porttabelle fehlt")
            blocks = {}
            for tag in ("EXERCISE", "SOLUTION", "TESTBENCH"):
                require(body.count(f"**{tag}_START**") == body.count(f"**{tag}_END**") == 1,
                        f"{identifier}: Marker {tag} fehlt/doppelt")
                block = re.search(r"\*\*" + tag + r"_START\*\*\s*```verilog\n(.*?)\n```\s*\*\*" + tag + r"_END\*\*", body, re.S)
                require(block is not None, f"{identifier}: Codebereich {tag} ungültig")
                blocks[tag] = block.group(1)
            bench = blocks["TESTBENCH"]
            require(helper in bench, f"{identifier}: Prüfhilfen veraltet")
            require("// END TEST HELPERS\n\n//--------" in bench, f"{identifier}: Trennlinie fehlt")
            require('`include' not in bench, f"{identifier}: HDLab bekommt keine Include-Dateien")
            require(not re.search(r"\btest_(solved|array)\b", bench), f"{identifier}: alte Ergebnisarrays")
            # Portnamen und Typen der Tabelle gegen die Musterlösung prüfen.
            solution_ports = {}
            header = blocks["SOLUTION"].split(");", 1)[0]
            for direction, declaration in re.findall(r"^\s*(input|output|inout)\s+(.+?)\s*,?\s*$", header, re.M):
                words = declaration.rstrip(",").split()
                name = words[-1]
                kind = " ".join(words[:-1]) or "wire"
                solution_ports[name] = (direction, kind)
            table = dict((name, (direction, kind)) for name, direction, kind in re.findall(
                r"^\| `([^`]+)` \| `([^`]+)` \| `([^`]+)` \|", body, re.M))
            require(table == solution_ports, f"{identifier}: Porttabelle passt nicht zur Musterlösung")
            check_interfaces(identifier, blocks, solution_ports)
        else:
            number = re.match(r"(\d+\.\d+) ", title)
            previous = number.group(1) if number else None
            exercise_index = 0
            if number and identifier != "001":
                require("Beispiel" in body or "```verilog" in body, f"{identifier}: Beispiel fehlt")
            for code in re.findall(r"```verilog\n(.*?)\n```", body, re.S):
                modules = re.findall(r"^module\s+(\w+)", code, re.M)
                if not modules:
                    fragments += 1  # Deklarationen und bewusst schematische Syntax.
                    continue
                for declaration in re.findall(r"module\s+\w+\s*\(.*?\);", code, re.S):
                    check_port_names(module_ports(declaration)[1])
                with tempfile.TemporaryDirectory(prefix="hdlab-example-") as directory:
                    source = Path(directory) / "example.sv"
                    source.write_text(code)
                    for module in modules:
                        result = subprocess.run(["verilator", "--lint-only", "--timing", "--top-module", module, str(source)], capture_output=True, text=True)
                        require(result.returncode == 0, f"{identifier}: Beispiel kompiliert nicht\n{result.stderr}")
                        examples += 1
    print(f"{len(ids)} Lektionen: IDs, Titel, Schwierigkeitsgrade und Inhaltsverzeichnis gültig.")
    print(f"{exercises} Übungen: Nummerierung, Codegerüste, Porttabellen und TB-Anschlüsse gültig.")
    print(f"{examples} vollständige Beispielmodule ohne Verilator-Warnungen geprüft; {fragments} Syntaxfragmente separat gezählt.")
    print(f"{figure_count} Typst-/SVG-Abbildungen mit PNG-Export in Kapitelordnern vorhanden.")
    print(f"{len(images)} eingebundene PNGs vorhanden; alle internen Links gültig.")


if __name__ == "__main__":
    main()
