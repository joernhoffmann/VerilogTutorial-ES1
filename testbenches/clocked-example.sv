// Vollständiges Referenzbeispiel für spätere getaktete Übungen.
// Die derzeitigen Kursübungen sind kombinatorisch und benötigen keinen Takt.
module tb_clocked_example;

localparam integer VALUE_WIDTH = 4;
localparam time WATCHDOG_TIME = 90;
localparam time CLOCK_PERIOD = 10;
localparam time SAMPLE_DELAY = 1;

`include "helpers.svh"

//------------------------------------------------------------------------ //

logic clk = 1'b0;
logic rst = 1'b0;
logic enable_in = 1'b0;
logic [3:0] data_in = 4'd0;
logic [3:0] data_out;

example_register dut (
    .clk(clk), .rst(rst), .enable_in(enable_in),
    .data_in(data_in), .data_out(data_out)
);

always #(CLOCK_PERIOD / 2) clk = ~clk;

// Rückkehr kurz nach der letzten steigenden Flanke: NBA-Zuweisungen sind beendet.
task automatic tick(input integer cycles = 1);
    repeat (cycles) begin
        @(posedge clk);
        #SAMPLE_DELAY;
    end
endtask

// Beispiel für einen synchronen, High-aktiven Reset.
// Andere Aufgaben benötigen gegebenenfalls eine andere Reset-Semantik.
task automatic reset_dut;
    @(negedge clk);
    rst = 1'b1;
    tick(2);
    @(negedge clk);
    rst = 1'b0;
endtask

initial begin
    reset_dut();
    all_passed &= assert_equal(data_out, 4'd0, "Reset setzt das Register auf null");

    // Eingänge an der fallenden Flanke setzen, nicht gleichzeitig mit der Übernahme.
    @(negedge clk);
    enable_in = 1'b1;
    data_in = 4'd9;
    tick();
    all_passed &= assert_equal(data_out, 4'd9, "Enable übernimmt den Eingangswert");

    @(negedge clk);
    enable_in = 1'b0;
    data_in = 4'd3;
    tick(2);
    all_passed &= assert_equal(data_out, 4'd9, "Ohne Enable bleibt der gespeicherte Wert erhalten");
    finish_tests();
end
endmodule

module example_register (
    input logic clk,
    input logic rst,
    input logic enable_in,
    input logic [3:0] data_in,
    output logic [3:0] data_out
);
    always_ff @(posedge clk) begin
        if (rst)
            data_out <= 4'd0;
        else if (enable_in)
            data_out <= data_in;
    end
endmodule
