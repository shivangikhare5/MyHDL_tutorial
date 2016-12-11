from myhdl import block, instances, Signal, modbv, ResetSignal, intbv, always_seq, always, always_comb

DATA=8         #Size of Data bus
ADDR=8         #Size of address bus
LOWER=2        #lower limit for FIFO read
UPPER=(2**8)-8 #upper limit for FIFO write
OFFSET=(2**8)-8 #upper limit for FIFO write

@block
def fifo(clk, inbusy, we, din, outbusy, rd, dout, rdout, rst,
          DATA=DATA, ADDR=ADDR, LOWER=LOWER, UPPER=UPPER, OFFSET=OFFSET):

    in_addr, out_addr, diff = [Signal(modbv(0)[ADDR+1:]) for i in range(3)]
    noread = Signal(bool(0))
    
    mem = [Signal(modbv(0)[DATA:]) for i in range(2**ADDR)]    
       
    @always_seq(clk.posedge, reset = rst)
    def write_port():
        if we:
            in_addr.next = in_addr + modbv(1)[ADDR+1:]
        if (diff >= UPPER):
            inbusy.next = bool(1)
        else:
            inbusy.next = bool(0)
                
    @always(clk.posedge)
    def write_mem_logic():
        if we:
            mem[in_addr[ADDR:]].next = din

            
    @always_seq(clk.posedge, reset = rst) #    @always(outclk.posedge)
    def read_port():
        dout.next = mem[out_addr[ADDR:]]
        if rd and not noread:
            out_addr.next = out_addr + modbv(1)[ADDR+1:]
            rdout.next = rd
        else:                
            rdout.next = bool(0)
        #if (diff >= OFFSET):
        #    hfull.next = bool(1)
        #    hfullL.next = bool(1)
        #if (diff <= LOWER):
        #    hfull.next = bool(0)
        #    hfullL.next = bool(0)
        
    @always_comb
    def diffLogic():
        diff.next = in_addr - out_addr
        
    @always_comb
    def outbusyLogic():
        #level.next = diff
        if (diff <= LOWER):
            outbusy.next = bool(1)
            noread.next = bool(1)
        else:
            outbusy.next = bool(0)
            noread.next = bool(0)
            
    return instances()