#!/usr/bin/env python3
"""HDLab-Prüfung mit strengem Verilator-Build; Icarus optional als Ergänzung."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def run(command, cwd=None, input_text=None):
    result = subprocess.run(command, cwd=cwd, input=input_text, capture_output=True,
                            text=True, encoding="utf-8", errors="replace", timeout=120)
    if result.returncode:
        raise RuntimeError(f"{' '.join(map(str, command))}\n{result.stdout}\n{result.stderr}")
    return result.stdout


def result_ok(log, expected):
    markers = re.findall(r"^TEST_SOLVED=([01])$", log, re.M)
    if markers != [str(int(expected))]:
        raise AssertionError(f"Gesamtergebnis falsch oder fehlend: {markers}\n{log}")
    if "Ergebnis:" not in log or (not expected and "❌ FAIL" not in log):
        raise AssertionError(f"Zusammenfassung/Fehlermeldung fehlt:\n{log}")
    if expected and "❌" in log:
        raise AssertionError(log)


def check_failure(good_log, bad_log):
    result_ok(good_log, True)
    result_ok(bad_log, False)
    if "Erwartet:" not in bad_log or "erhalten:" not in bad_log:
        raise AssertionError(bad_log)
    counts = [int(re.search(r"Ergebnis: \d+ von (\d+)", log).group(1))
              for log in (good_log, bad_log)]
    if counts[0] != counts[1]:
        raise AssertionError("Prüfungen wurden nach einem Fehler übersprungen")
    return counts[0]


def simulate_iverilog(code, top, arguments=()):
    with tempfile.TemporaryDirectory(prefix="hdlab-iverilog-") as directory:
        directory = Path(directory)
        source = directory / "test.sv"
        source.write_text(code)
        output = directory / "test.out"
        run(["iverilog", "-g2012", "-s", top, "-o", str(output), str(source)])
        return run(["vvp", str(output), *arguments])


def compile_verilator(solution, bench, top, directory):
    (directory / "main.sv").write_text(solution)
    (directory / "tb.sv").write_text(bench)
    # Entspricht HDLabs begrenzter eval/timeInc-Schleife, nicht --binary.
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
    # Wie im HDLab-Entrypoint: Warnungen sind fatal, keine pauschale Ausnahme.
    run(["verilator", "--cc", "--timing", "--top-module", top,
         "main.sv", "tb.sv", "--exe", "sim.cpp", "--build", "-j", "2"], directory)
    return directory / "obj_dir" / ("V" + top)


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


def fault(solution):
    bad, count = re.subn(r"(assign\s+\w+\s*=)[^;]*;", r"\1 '0;", solution, count=1)
    if count != 1:
        raise ValueError("Fehlerprobe benötigt Anpassung")
    return bad


def check_case(case):
    identifier, solution, bench, top = case
    with tempfile.TemporaryDirectory(prefix="hdlab-verilator-") as directory:
        directory = Path(directory)
        executable = compile_verilator(solution, bench, top, directory)
        good_log = run([str(executable)], directory)
        executable = compile_verilator(fault(solution), bench, top, directory)
        bad_log = run([str(executable)], directory)
    count = check_failure(good_log, bad_log)
    return identifier, count, good_log, bad_log, bench


def embed_helpers(code):
    return code.replace('`include "helpers.svh"', (ROOT / "testbenches/helpers.svh").read_text())


def helper_example():
    return embed_helpers('''module tb_helpers;
localparam integer VALUE_WIDTH = 8;
localparam time WATCHDOG_TIME = 90;
`include "helpers.svh"
integer selected = 0;
initial begin
    if (!$value$plusargs("CASE=%d", selected)) selected = 0;
    case (selected)
        0: begin
            all_passed &= assert_equal(8'hA5, 8'hA5, "Vektorvergleich");
            all_passed &= assert_equal_signed(-8'sd3, -8'sd3, "Signed-Vergleich");
            all_passed &= assert_true(1'b1, "Wahrheitswert");
        end
        1: begin
            all_passed &= assert_equal(8'hA5, 8'hA4, "Falscher Vektor");
            all_passed &= assert_equal(8'd1, 8'd1, "Folgetest muss noch laufen");
        end
        2: all_passed &= assert_true(1'b0, "Falsche Bedingung");
        3: all_passed &= assert_equal_signed(8'sd3, -8'sd3, "Falsches Vorzeichen");
        4: begin end // Ohne Prüfungen muss das Gesamtergebnis falsch sein.
        5: begin #1000; end // Der Watchdog muss vorher auslösen.
`ifndef VERILATOR
        6: begin
            all_passed &= assert_equal(8'b0000_00x1, 8'd1, "X ist nicht 1");
            all_passed &= assert_true(1'bx, "X ist nicht wahr");
        end
        7: all_passed &= assert_equal(8'b0000_00z1, 8'd1, "Z ist nicht 1");
`endif
    endcase
    finish_tests();
end
endmodule
''')


def check_helpers():
    with tempfile.TemporaryDirectory(prefix="hdlab-helpers-") as directory:
        directory = Path(directory)
        executable = compile_verilator("", helper_example(), "tb_helpers", directory)
        for selected in range(6):
            log = run([str(executable), f"+CASE={selected}"], directory)
            result_ok(log, selected == 0)
            if selected == 1 and "✅ PASS 2:" not in log:
                raise AssertionError("Nach dem ersten Fehler fehlt der Folgetest")
            if selected == 5 and "Timeout" not in log:
                raise AssertionError("Watchdog wurde nicht ausgeführt")
    code = embed_helpers((ROOT / "testbenches/clocked-example.sv").read_text())
    with tempfile.TemporaryDirectory(prefix="hdlab-clock-") as directory:
        directory = Path(directory)
        executable = compile_verilator("", code, "tb_clocked_example", directory)
        good = run([str(executable)], directory)
        bad_code = code.replace("data_out <= data_in;", "data_out <= 4'd0;")
        executable = compile_verilator("", bad_code, "tb_clocked_example", directory)
        check_failure(good, run([str(executable)], directory))
    print("Verilator: Prüfhilfen, Folgeprüfungen, leere Läufe und Timeout bestanden.", flush=True)
    print("Verilator: Takt/Reset/Übernahme/Halten bestanden; fehlerhaftes Register erkannt.", flush=True)


def check_iverilog(cases):
    for identifier, solution, bench, top in cases:
        check_failure(simulate_iverilog(solution + "\n" + bench, top),
                      simulate_iverilog(fault(solution) + "\n" + bench, top))
    for selected in range(8):
        result_ok(simulate_iverilog(helper_example(), "tb_helpers", [f"+CASE={selected}"]), selected == 0)
    print("Ergänzend Icarus: alle Übungen und die zusätzlichen X/Z-Prüfungen bestanden.", flush=True)


def check_backend(source_root, results):
    import json
    # Nur vorhandene Parserfunktionen lesen, keine Backend-Dienste starten.
    route = source_root / "apps/backend/src/routes/tutorial.js"
    code = '''import fs from 'node:fs';
const data = JSON.parse(fs.readFileSync(0, 'utf8'));
const source = fs.readFileSync(process.argv[1], 'utf8');
function extract(name) {
  const start = source.indexOf('function ' + name + '(');
  if (start < 0) throw Error('Backend-Funktion fehlt: ' + name);
  return source.slice(start, source.indexOf('\\n}', start) + 2);
}
const api = new Function(extract('injectTestSolvedDisplay') + '\\n' +
  extract('checkValidationLog') + '\\nreturn {injectTestSolvedDisplay, checkValidationLog};')();
for (const row of data) {
  const [id, count, good, bad, bench] = row;
  if (api.injectTestSolvedDisplay(bench) !== bench) throw Error(id + ': unerwartete Instrumentierung');
  if (!api.checkValidationLog(good)) throw Error(id + ': Musterlösung abgelehnt');
  if (api.checkValidationLog(bad)) throw Error(id + ': Fehler akzeptiert');
}
console.log(data.length + ' Übungen: tatsächliche HDLab-Backendfunktionen erkennen Erfolg und Fehler.');
'''
    print(run(["node", "--input-type=module", "-e", code, str(route)],
              input_text=json.dumps(results, ensure_ascii=False)).strip(), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verilator", action="store_true", help="Kompatibler Alias: Verilator ist bereits Standard")
    parser.add_argument("--iverilog", action="store_true", help="Zusätzliche 4-State-Prüfung mit Icarus")
    parser.add_argument("--hdlab-source", type=Path, help="Optionaler lokaler HDLab-Checkout für den echten Backend-Parser")
    args = parser.parse_args()
    run(["python3", str(ROOT / "scripts/sync_test_helpers.py"), "--check"])
    print(run(["verilator", "--version"]).strip(), flush=True)
    cases = extract()
    results = []
    with ThreadPoolExecutor(max_workers=3) as executor:
        for result in executor.map(check_case, cases):
            results.append(result)
            print(f"{result[0]}: {result[1]} Prüfungen bestanden; Fehlerprobe erkannt (Verilator).", flush=True)
    check_helpers()
    if args.iverilog:
        check_iverilog(cases)
    if args.hdlab_source:
        check_backend(args.hdlab_source, results)
    print(f"Alle {len(cases)} Testbenches mit strengem Verilator-Build geprüft.")


if __name__ == "__main__":
    main()
