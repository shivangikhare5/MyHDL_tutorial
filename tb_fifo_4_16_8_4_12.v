module tb_fifo_4_16_8_4_12;

reg clk;
wire inbusy;
reg we;
reg [15:0] din;
wire outbusy;
reg rd;
wire [15:0] dout;
wire rdout;
reg rst;

initial begin
    $from_myhdl(
        clk,
        we,
        din,
        rd,
        rst
    );
    $to_myhdl(
        inbusy,
        outbusy,
        dout,
        rdout
    );
end

fifo_4_16_8_4_12 dut(
    clk,
    inbusy,
    we,
    din,
    outbusy,
    rd,
    dout,
    rdout,
    rst
);

endmodule
