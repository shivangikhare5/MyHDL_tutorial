from myhdl import *
import hdlcfg

#DUT of ram module
@block
def ram(clk,
        a_din, a_addr, a_we, a_dout, a_rd, a_rdout,
        b_din, b_addr, b_we, b_dout, b_rd, b_rdout,
        DATA=8, ADDR=4):
    """ Ram Module """
    """
    clk   = Clock Signal
    din   = Input data
    addr  = Address 
    we    = Write Enable
    dout  = Output Data
    rd    = Read enable
    rdout = Read out(time required by given ram)
    DATA  = Data bus
    ADDR  = Address bus
    """
    # Define Memory Array
    mem = [Signal(modbv(0)[DATA:]) for i in range(2**ADDR)]
    
    # Define Write Cycle
    @always(clk.posedge)
    def a_write():
        if we:
            mem[a_addr].next = a_din
    
    # Define Read Cycle
    @always(clk.posedge)
    def a_read():
        if a_rd:
            a_dout.next = mem[a_addr]
        a_rdout.next = a_rd
    
    # Define Write Cycle
    @always(clk.posedge)
    def b_write():
        if we:
            mem[b_addr].next = b_din
    
    # Define Read Cycle
    @always(clk.posedge)
    def b_read():
        if b_rd:
            b_dout.next = mem[b_addr]
        b_rdout.next = b_rd
            
    return instances()

# Define VHDL Conversion function
def ram_convert(DATA=8, ADDR=4):
    clk    = Signal(bool(0))
    din    = Signal(modbv(0)[DATA:])
    addr   = Signal(modbv(0)[ADDR:])
    we     = Signal(bool(0))
    dout   = Signal(modbv(0)[DATA:])
    rd     = Signal(bool(0))
    rdout  = Signal(bool(0))
    ram_inst = ram(clk, din, addr, we, dout, rd, rdout, DATA=8, ADDR=4)
    ram_inst.convert(hdl='Verilog', header=hdlcfg.header, directory=hdlcfg.hdl_path,
                     name='ram_' + str(ADDR)+'_'+ str(DATA))

if __name__ == '__main__':
    ram_convert(DATA=8, ADDR=4)
