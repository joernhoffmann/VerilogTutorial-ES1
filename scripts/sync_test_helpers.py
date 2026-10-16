#!/usr/bin/env python3
"""Prüfhilfen in die eigenständig ausführbaren HDLab-Testbenches einbetten."""
import argparse
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BEGIN = "// BEGIN TEST HELPERS"
END = "// END TEST HELPERS"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Nur prüfen, nichts ändern")
    args = parser.parse_args()
    source = ROOT / "ES1Tutorial.md"
    text = source.read_text()
    helper = (ROOT / "testbenches/helpers.svh").read_text().strip()
    pattern = re.compile(r"(\*\*TESTBENCH_START\*\*\s*```verilog\n)(.*?)(\n```\s*\*\*TESTBENCH_END\*\*)", re.S)
    count = 0

    def replace(match):
        nonlocal count
        bench = match.group(2)
        if bench.count(BEGIN) != 1 or bench.count(END) != 1:
            raise ValueError("Testbench ohne eindeutigen Prüfhilfen-Bereich")
        count += 1
        bench = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END),
                       lambda _: BEGIN + "\n" + helper + "\n" + END, bench, flags=re.S)
        return match.group(1) + bench + match.group(3)

    updated = pattern.sub(replace, text)
    if not count:
        raise SystemExit("Keine Testbenches gefunden")
    if args.check and updated != text:
        raise SystemExit("Prüfhilfen veraltet: make testbenches ausführen")
    if not args.check and updated != text:
        source.write_text(updated)
    print(f"{count} Testbenches: Prüfhilfen aktuell.")


if __name__ == "__main__":
    main()
