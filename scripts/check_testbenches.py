#!/usr/bin/env python3
"""HDLab-Testbenches mit Musterlösungen, Fehlern und optional Verilator prüfen."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def run(command, cwd=None):
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True,
                            encoding="utf-8", errors="replace", timeout=120)
    if result.returncode:
        raise RuntimeError(f"{' '.join(map(str, command))}\n{result.stdout}\n{result.stderr}")
    return result.stdout


def result_ok(log, expected):
    markers = re.findall(r"^TEST_SOLVED=([01])$", log, re.M)
    if markers != [str(int(expected))]:
        raise AssertionError(f"Gesamtergebnis falsch oder fehlend: {markers}\n{log}")
    if "Ergebnis:" not in log or (not expected and "❌ FAIL" not in log):
        raise AssertionError(f"Zusammenfassung/Fehlermeldung fehlt:\n{log}")


def simulate_iverilog(code, top):
    with tempfile.TemporaryDirectory(prefix="hdlab-test-") as directory:
        directory = Path(directory)
        source = directory / "test.sv"
        source.write_text(code)
        output = directory / "test.out"
        run(["iverilog", "-g2012", "-I", str(ROOT / "testbenches"),
             "-s", top, "-o", str(output), str(source)])
        return run(["vvp", str(output)])


def extract():
    text = (ROOT / "ES1Tutorial.md").read_text()
    lessons = re.split(r"(?=<!--\s*\nlesson_id:)", text)
    cases = []
    for lesson in lessons:
        if 'type: "exercise"' not in lesson:
            continue
        identifier = re.search(r"lesson_id: (\d+)", lesson).group(1)
        def block(tag):
            match = re.search(r"\*\*" + tag + r"_START\*\*\s*```verilog\n(.*?)\n```", lesson, re.S)
            if not match:
                raise ValueError(f"Lektion {identifier}: {tag} fehlt")
            return match.group(1)
        bench = block("TESTBENCH")
        top = re.search(r"\bmodule\s+(\w+)", bench).group(1)
        cases.append((identifier, block("SOLUTION"), bench, top))
    if not cases:
        raise ValueError("Keine Übungen gefunden")
    return cases


def check_case(case):
    identifier, solution, bench, top = case
    log = simulate_iverilog(solution + "\n" + bench, top)
    result_ok(log, True)
    if "❌" in log:
        raise AssertionError(log)
    # Ein absichtlich auf null festgelegtes Signal muss als Fehler erkannt werden.
    bad, count = re.subn(r"(assign\s+\w+\s*=)[^;]*;", r"\1 '0;", solution, count=1)
    if count != 1:
        raise ValueError(f"Lektion {identifier}: Fehlerprobe benötigt Anpassung")
    bad_log = simulate_iverilog(bad + "\n" + bench, top)
    result_ok(bad_log, False)
    if "Erwartet:" not in bad_log or "erhalten:" not in bad_log:
        raise AssertionError(bad_log)
    good_count = int(re.search(r"Ergebnis: \d+ von (\d+)", log).group(1))
    bad_count = int(re.search(r"Ergebnis: \d+ von (\d+)", bad_log).group(1))
    if good_count != bad_count:
        raise AssertionError("Prüfungen wurden nach einem Fehler übersprungen")
    return f"{identifier}: {good_count} Prüfungen bestanden; Fehlerprobe erkannt."


def check_helpers():
    prefix = '''module tb_helpers;
localparam integer VALUE_WIDTH = 8;
localparam time WATCHDOG_TIME = 90;
`include "helpers.svh"
'''
    tests = [
        ('''all_passed &= assert_equal(8'hA5, 8'hA5, "Vektorvergleich");
all_passed &= assert_equal_signed(-8'sd3, -8'sd3, "Signed-Vergleich");
all_passed &= assert_true(1'b1, "Wahrheitswert");''', True),
        ('''all_passed &= assert_equal(8'hA5, 8'hA4, "Falscher Vektor");
all_passed &= assert_equal(8'd1, 8'd1, "Folgetest muss noch laufen");''', False),
        ('''all_passed &= assert_equal(8'b0000_00x1, 8'd1, "X ist kein bekannter Sollwert");
all_passed &= assert_true(1'bx, "Unbekannte Bedingung ist nicht wahr");''', False),
        ('''all_passed &= assert_equal(8'b0000_00z1, 8'd1, "Z ist kein bekannter Sollwert");''', False),
        ('''all_passed &= assert_equal_signed(8'sd3, -8'sd3, "Falsches Vorzeichen");''', False),
        ("", False),  # Keine Prüfungen dürfen nicht zum Erfolg führen.
    ]
    for body, expected in tests:
        log = simulate_iverilog(prefix + "initial begin\n" + body + "\nfinish_tests();\nend\nendmodule", "tb_helpers")
        result_ok(log, expected)
    timeout = simulate_iverilog(prefix + "initial begin #1000; end\nendmodule", "tb_helpers")
    result_ok(timeout, False)
    if "Timeout" not in timeout:
        raise AssertionError(timeout)
    example = (ROOT / "testbenches/clocked-example.sv").read_text()
    result_ok(simulate_iverilog(example, "tb_clocked_example"), True)
    result_ok(simulate_iverilog(example.replace("data_out <= data_in;", "data_out <= 4'd0;"), "tb_clocked_example"), False)
    print("Prüfhilfen: Soll/Ist, Signed, X/Z, Folgetests, leere Prüfung und Timeout geprüft.")
    print("Getaktetes Beispiel: Reset, Übernahme und Halten bestanden; Fehlerprobe erkannt.")


def check_verilator(case):
    identifier, solution, bench, top = case
    with tempfile.TemporaryDirectory(prefix="hdlab-verilator-") as directory:
        directory = Path(directory)
        (directory / "main.sv").write_text(solution)
        (directory / "tb.sv").write_text(bench)
        # Gleiche begrenzte Zeitschritte wie im lokalen HDLab-Worker.
        (directory / "sim.cpp").write_text(f'''#include "V{top}.h"
#include "verilated.h"
int main(int argc, char** argv) {{
    Verilated::commandArgs(argc, argv);
    V{top} dut;
    for (int tick = 0; tick < 100 && !Verilated::gotFinish(); ++tick) {{
        dut.eval();
        Verilated::timeInc(1);
    }}
    dut.final();
    return 0;
}}
''')
        # Legal multi-bit logical operands in exercise 402 generate WIDTH warnings
        # with some Verilator versions; keep these warnings non-fatal locally.
        run(["verilator", "--cc", "--timing", "-Wno-fatal", "--top-module", top,
             "main.sv", "tb.sv", "--exe", "sim.cpp", "--build", "-j", "2"], directory)
        log = run([str(directory / "obj_dir" / ("V" + top))], directory)
        result_ok(log, True)
        return f"{identifier}: Verilator/HDLab-Protokoll innerhalb von 100 Zeitschritten bestanden."


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verilator", action="store_true", help="Zusätzlich Verilator und HDLab-Zeitlimit prüfen")
    args = parser.parse_args()
    run(["python3", str(ROOT / "scripts/sync_test_helpers.py"), "--check"])
    cases = extract()
    for case in cases:
        print(check_case(case), flush=True)
    check_helpers()
    if args.verilator:
        clocked = (ROOT / "testbenches/clocked-example.sv").read_text()
        helper = (ROOT / "testbenches/helpers.svh").read_text()
        clocked = clocked.replace('`include "helpers.svh"', helper)
        verilator_cases = cases + [("clocked-example", "", clocked, "tb_clocked_example")]
        with ThreadPoolExecutor(max_workers=3) as executor:
            for message in executor.map(check_verilator, verilator_cases):
                print(message, flush=True)
    print(f"Alle {len(cases)} Testbenches geprüft.")


if __name__ == "__main__":
    main()
