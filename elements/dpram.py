from myhdl import *
import hdlcfg

#DUT of ram module
@block
def dpram(clk,
        a_din, a_addr, a_we, a_dout, a_rd, a_rdout,
        b_din, b_addr, b_we, b_dout, b_rd, b_rdout,
        DATA=8, ADDR=4):
    """ Dpram Module """
    """
    clk   = Clock Signal
    a_din   = Input data
    a_addr  = Address 
    a_we    = Write Enable
    a_dout  = Output Data
    a_rd    = Read enable
    a_rdout = Read out(time required by given ram)
    
    b_din   = Input data
    b_addr  = Address 
    b_we    = Write Enable
    b_dout  = Output Data
    b_rd    = Read enable
    b_rdout = Read out(time required by given ram)
    DATA  = Data bus
    ADDR  = Address bus
    """
    # Define Memory Array
    mem = [Signal(modbv(0)[DATA:]) for i in range(2**ADDR)]
    
    # Define Write Cycle for A port
    @always(clk.posedge)
    def a_write():
        if a_we:
            mem[a_addr].next = a_din
    
    # Define Read Cycle for A port
    @always(clk.posedge)
    def a_read():
        if a_rd:
            a_dout.next = mem[a_addr]
        a_rdout.next = a_rd
    
    # Define Write Cycle for B port
    @always(clk.posedge)
    def b_write():
        if b_we:
            mem[b_addr].next = b_din
    
    # Define Read Cycle for B port
    @always(clk.posedge)
    def b_read():
        if b_rd:
            b_dout.next = mem[b_addr]
        b_rdout.next = b_rd
            
    return instances()

# Define VHDL Conversion function
def dpram_convert(DATA=8, ADDR=4):
    clk    = Signal(bool(0))
    a_din    = Signal(modbv(0)[DATA:])
    a_addr   = Signal(modbv(0)[ADDR:])
    a_we     = Signal(bool(0))
    a_dout   = Signal(modbv(0)[DATA:])
    a_rd     = Signal(bool(0))
    a_rdout  = Signal(bool(0))
    
    b_din    = Signal(modbv(0)[DATA:])
    b_addr   = Signal(modbv(0)[ADDR:])
    b_we     = Signal(bool(0))
    b_dout   = Signal(modbv(0)[DATA:])
    b_rd     = Signal(bool(0))
    b_rdout  = Signal(bool(0))
    dpram_inst = dpram(clk,
        a_din, a_addr, a_we, a_dout, a_rd, a_rdout,
        b_din, b_addr, b_we, b_dout, b_rd, b_rdout,
        DATA=8, ADDR=4)
    dpram_inst.convert(hdl='Verilog', header=hdlcfg.header, directory=hdlcfg.hdl_path,
                     name='dpram_' + str(ADDR)+'_'+ str(DATA))

if __name__ == '__main__':
    dpram_convert(DATA=8, ADDR=4)
