// Wird für HDLab direkt in jede Testbench eingebettet (keine Includes nötig).
// VALUE_WIDTH und WATCHDOG_TIME werden in der jeweiligen Testbench festgelegt.
integer tests_run = 0;
integer tests_passed = 0;
bit all_passed = 1'b1;

function automatic string bit_string(
    input logic [VALUE_WIDTH-1:0] value,
    input integer width
);
    string result;
    result = "";
    for (integer i = width - 1; i >= 0; i = i - 1)
        result = {result, $sformatf("%b", value[i])};
    return result;
endfunction

function automatic bit report_check(
    input bit passed,
    input string description,
    input string details
);
    tests_run = tests_run + 1;
    if (passed) begin
        tests_passed = tests_passed + 1;
        $display("✅ PASS %0d: %s", tests_run, description);
    end
    else begin
        $display("❌ FAIL %0d: %s", tests_run, description);
        $display("   %s", details);
    end
    return passed;
endfunction

function automatic bit assert_equal(
    input logic [VALUE_WIDTH-1:0] actual,
    input logic [VALUE_WIDTH-1:0] expected,
    input string description,
    input integer width = VALUE_WIDTH
);
    return report_check(actual === expected, description,
        $sformatf("Erwartet: %s (unsigned %0d); erhalten: %s (unsigned %0d)",
                  bit_string(expected, width), expected,
                  bit_string(actual, width), actual));
endfunction

function automatic bit assert_equal_signed(
    input logic signed [VALUE_WIDTH-1:0] actual,
    input logic signed [VALUE_WIDTH-1:0] expected,
    input string description
);
    return report_check(actual === expected, description,
        $sformatf("Erwartet: %0d (Bits %b); erhalten: %0d (Bits %b)",
                  expected, expected, actual, actual));
endfunction

function automatic bit assert_true(
    input logic condition,
    input string description
);
    return report_check(condition === 1'b1, description,
        $sformatf("Erwartet: wahr (1); erhalten: %b", condition));
endfunction

task automatic finish_tests;
    // Ohne ausgeführte Prüfungen darf eine Testbench nicht bestehen.
    all_passed = all_passed & (tests_run > 0) & (tests_run == tests_passed);
    $display("\nErgebnis: %0d von %0d Prüfungen bestanden.", tests_passed, tests_run);
    if (all_passed)
        $display("✅ PASS Gesamtergebnis");
    else
        $display("❌ FAIL Gesamtergebnis");
    // Maschinenlesbares Gesamtergebnis für die bestehende HDLab-Auswertung.
    $display("TEST_SOLVED=%b", all_passed);
    $finish;
endtask

initial begin : watchdog
    #WATCHDOG_TIME;
    $display("❌ FAIL Timeout: Testbench nach %0t nicht beendet.", $time);
    all_passed = 1'b0;
    finish_tests();
end
