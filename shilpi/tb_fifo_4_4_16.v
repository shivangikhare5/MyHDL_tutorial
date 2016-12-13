module tb_fifo_4_4_16;

reg clk;
reg wenable;
reg renable;
reg [3:0] din;
wire [3:0] dout;
wire rdout;
wire outbusy;
wire inbusy;

initial begin
    $from_myhdl(
        clk,
        wenable,
        renable,
        din
    );
    $to_myhdl(
        dout,
        rdout,
        outbusy,
        inbusy
    );
end

fifo_4_4_16 dut(
    clk,
    wenable,
    renable,
    din,
    dout,
    rdout,
    outbusy,
    inbusy
);

endmodule
