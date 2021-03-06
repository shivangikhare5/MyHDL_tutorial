// File: fifo_4_16_8_4_12.v
// Generated by MyHDL 1.0dev
// Date: Mon Dec 12 19:07:10 2016


`timescale 1ns/10ps

module fifo_4_16_8_4_12 (
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


input clk;
output inbusy;
reg inbusy;
input we;
input [15:0] din;
output outbusy;
reg outbusy;
input rd;
output [15:0] dout;
reg [15:0] dout;
output rdout;
reg rdout;
input rst;

reg [4:0] out_addr;
reg [4:0] in_addr;
reg noread;
wire [4:0] diff;
reg [15:0] mem [0:16-1];



always @(posedge clk) begin: FIFO_4_16_8_4_12_WRITE_PORT
    if (rst == 1) begin
        inbusy <= 0;
        in_addr <= 0;
    end
    else begin
        if (we) begin
            in_addr <= (in_addr + 5'h1);
        end
        if ((diff >= 12)) begin
            inbusy <= (1 != 0);
        end
        else begin
            inbusy <= (0 != 0);
        end
    end
end


always @(posedge clk) begin: FIFO_4_16_8_4_12_READ_PORT
    if (rst == 1) begin
        out_addr <= 0;
        rdout <= 0;
        dout <= 0;
    end
    else begin
        dout <= mem[out_addr[4-1:0]];
        if ((rd && (!noread))) begin
            out_addr <= (out_addr + 5'h1);
            rdout <= rd;
        end
        else begin
            rdout <= (0 != 0);
        end
    end
end


always @(posedge clk) begin: FIFO_4_16_8_4_12_WRITE_MEM_LOGIC
    if (we) begin
        mem[in_addr[4-1:0]] <= din;
    end
end



assign diff = (in_addr - out_addr);


always @(diff) begin: FIFO_4_16_8_4_12_OUTBUSYLOGIC
    if ((diff <= 4)) begin
        outbusy = (1 != 0);
        noread = (1 != 0);
    end
    else begin
        outbusy = (0 != 0);
        noread = (0 != 0);
    end
end

endmodule
