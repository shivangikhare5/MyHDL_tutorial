from myhdl import *
import hdlcfg

DATA=8         #Size of Data bus
ADDR=4         #Size of address bus
LOWER=4       #lower limit for FIFO read
UPPER=(2**ADDR)-4  #upper limit for FIFO write
OFFSET = (2**ADDR)-4

@block
def fifo(din, we, inbusy, inclk, rd, rdout, outbusy, dout, outclk, hfull,rst, DATA = DATA, ADDR =ADDR, UPPER =UPPER,LOWER =LOWER):
    
    """ Half full FIFO model
    inclk  = Clock Input for write
    inbusy = Input bus is busy (overflow)
    we     = Input bus write enable
    din    = Input bus data input
    inclk  = Clock Input for read
    outbusy= Output bus is busy (underflow)
    rd     = Output bus read enable
    dout   = Output bus data output
    rdout  = Output bus data can be read
    hfull  = Buffer half full
    rst    = Reset
    ADDR   = Size of Address bus
    DATA   = Size of Data bus
    LOWER  = Size of lower limit for buffer after which buffer can be read
    UPPER  = Size of upper limit for buffer after which buffer can not be written"""
        
    mem = [Signal(modbv(0)[DATA:]) for i in range(2**ADDR)]
    in_addr, out_addr  = [Signal(modbv(0)[ADDR+1:]) for i in range(2)]
    diff = Signal(bool(1))
    length = Signal(modbv(0)[ADDR+1:])
    
    #In_Rst = ResetSignal(0, active=1, async=False)
    #Out_Rst = ResetSignal(0, active=1, async=False)
    
    @always(inclk.posedge)
    def write():
        if we & (not inbusy):
            mem[in_addr[ADDR:]].next = din
            in_addr.next = in_addr + modbv(1)[ADDR+1:]
            
    @always(outclk.posedge)
    def read():
        if rd & (not outbusy):
            dout.next = mem[out_addr[ADDR:]]
            out_addr.next =  out_addr + modbv(1)[ADDR+1:]
        rdout.next = rd and not outbusy
            
            
    @always_seq(inclk.posedge, reset = rst)
    def in_wrap():          #while wrapping in_addr change (ADDR+1)th bit
        if in_addr[ADDR:] > UPPER:
            #n_addr.next = in_addr | 2**(ADDR+1)
            in_addr[ADDR+1].next = not in_addr[ADDR+1]
            

    @always_seq(outclk.posedge, reset = rst)
    def out_wrap():           #while wrapping out_addr change (ADDR+1)th bit
        if out_addr[ADDR:] > UPPER:
            #ut_addr.next = out_addr | 2**(ADDR+1)
            out_addr[ADDR+1].next = not out_addr[ADDR+1]
        
        if length > OFFSET:
            hfull.next = 1
        elif length == 4:
            hfull.next = 0

    @always_comb
    def busylogic():
        diff.next = in_addr[ADDR] ^ out_addr[ADDR]    #diff is a flag which indicates wrapping of any one pointer(in or out)
        
    @always_comb
    def busy():
        if (in_addr[ADDR:] == out_addr[ADDR:]):        
            if diff == 1:
                outbusy.next = 0
                inbusy.next = 1
            else:
                outbusy.next = 1                
                inbusy.next = 0
        else:
            inbusy.next = 0
            outbusy.next = 0 

         
        if diff: 
            length.next = UPPER-out_addr[ADDR:] + in_addr[ADDR:]-LOWER
        else:
            length.next = in_addr[ADDR:] - out_addr[ADDR:]
            
                        

    return instances()


# Define VHDL Conversion function
def fifo_convert(DATA=8, ADDR=4):
    din, dout          = [Signal(modbv(0)[DATA:]) for i in range(2)]
    in_addr, out_addr  = [Signal(modbv(0)[ADDR+1:]) for i in range(2)]
    DATA               = 8
    ADDR               = 4
    UPPER              = 2**ADDR
    LOWER              = 0    
    rst = ResetSignal(0, active=1, async=False)
    inclk, outclk,we, rd, inbusy, outbusy, hfull, rdout = [Signal(bool(0)) for i in range(8)]    
    
    fifo_inst = fifo(din, we, inbusy, inclk, rd, rdout, outbusy, dout, outclk, hfull, rst, DATA = DATA, ADDR =ADDR, UPPER =UPPER,LOWER =LOWER)
    fifo_inst.convert(hdl='Verilog', header=hdlcfg.header, directory=hdlcfg.hdl_path,
                     name='fifo_' + str(ADDR)+'_'+ str(DATA))
    
if __name__ == '__main__':
    fifo_convert(DATA=8, ADDR=4)

            