from myhdl import *
import hdlcfg

#DUT of ram module
@block
def ram(clk, din, addr, we, dout, rd, rdout, DATA=8, ADDR=4):
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
    def write():
        if we:
            mem[addr].next = din
    
    # Define Read Cycle
    @always(clk.posedge)
    def read():
        if rd:
            dout.next = mem[addr]
        rdout.next = rd
            
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
