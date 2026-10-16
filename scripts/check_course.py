#!/usr/bin/env python3
"""Metadaten, Markdown-Verweise, Übungsstruktur und vollständige Codebeispiele prüfen."""
from collections import Counter
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def slug(text):
    text = re.sub(r"<!--.*?-->", "", text).lower().strip()
    return re.sub(r"[^\w\s-]", "", text).replace(" ", "-")


def main():
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
        require(metadata.get("difficulty") == "intro", f"{identifier}: difficulty ist nicht intro")
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
                with tempfile.TemporaryDirectory(prefix="hdlab-example-") as directory:
                    source = Path(directory) / "example.sv"
                    source.write_text(code)
                    for module in modules:
                        result = subprocess.run(["verilator", "--lint-only", "--timing", "--top-module", module, str(source)], capture_output=True, text=True)
                        require(result.returncode == 0, f"{identifier}: Beispiel kompiliert nicht\n{result.stderr}")
                        examples += 1
    print(f"{len(ids)} Lektionen: IDs, Titel, intro-Metadaten und Inhaltsverzeichnis gültig.")
    print(f"{exercises} Übungen: Nummerierung, Abschnitte, Porttabellen und Codebereiche gültig.")
    print(f"{examples} vollständige Beispielmodule ohne Verilator-Warnungen geprüft; {fragments} Syntaxfragmente separat gezählt.")
    print(f"{len(images)} eingebundene PNGs vorhanden; alle internen Links gültig.")


if __name__ == "__main__":
    main()
