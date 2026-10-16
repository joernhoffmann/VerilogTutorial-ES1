// Vollständiges Referenzbeispiel für spätere getaktete Übungen.
module tb_clocked_example;

localparam integer VALUE_WIDTH = 4;
localparam time WATCHDOG_TIME = 90;
localparam time CLOCK_PERIOD = 10;
localparam time SAMPLE_DELAY = 1;

`include "helpers.svh"

//------------------------------------------------------------------------ //

logic clk_in = 1'b0;
logic rst_in = 1'b0;
logic enable_in = 1'b0;
logic [3:0] e_in = 4'd0;
logic [3:0] a_out;

example_register dut (
    .clk_in(clk_in), .rst_in(rst_in), .enable_in(enable_in),
    .e_in(e_in), .a_out(a_out)
);

always #(CLOCK_PERIOD / 2) clk_in = ~clk_in;

// Rückkehr kurz nach der letzten steigenden Flanke: NBA-Zuweisungen sind beendet.
task automatic tick(input integer cycles = 1);
    repeat (cycles) begin
        @(posedge clk_in);
        #SAMPLE_DELAY;
    end
endtask

// Beispiel für einen synchronen, High-aktiven Reset.
// Andere Aufgaben benötigen gegebenenfalls eine andere Reset-Semantik.
task automatic reset_dut;
    @(negedge clk_in);
    rst_in = 1'b1;
    tick(2);
    @(negedge clk_in);
    rst_in = 1'b0;
endtask

initial begin
    reset_dut();
    all_passed &= assert_equal(a_out, 4'd0, "Reset setzt das Register auf null");

    // Eingänge an der fallenden Flanke setzen, nicht gleichzeitig mit der Übernahme.
    @(negedge clk_in);
    enable_in = 1'b1;
    e_in = 4'd9;
    tick();
    all_passed &= assert_equal(a_out, 4'd9, "Enable übernimmt den Eingangswert");

    @(negedge clk_in);
    enable_in = 1'b0;
    e_in = 4'd3;
    tick(2);
    all_passed &= assert_equal(a_out, 4'd9, "Ohne Enable bleibt der gespeicherte Wert erhalten");
    finish_tests();
end
endmodule

module example_register (
    input logic clk_in,
    input logic rst_in,
    input logic enable_in,
    input logic [3:0] e_in,
    output logic [3:0] a_out
);
    always_ff @(posedge clk_in) begin
        if (rst_in)
            a_out <= 4'd0;
        else if (enable_in)
            a_out <= e_in;
    end
endmodule
