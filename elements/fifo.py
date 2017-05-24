from myhdl import *


@block
def fifo(din, we, inbusy, inclk, in_addr, rd, rdout, outbusy, dout, outclk, out_addr, hfull, DATA, ADDR, UPPER,LOWER):
    
    @always_seq(inclk.posedge)
    def write():
        if we & (not inbusy):
            mem[in_addr[ADDR+1:]].next = din
            in_addr.next = in_addr + modbv(1)[ADDR+1:]
            
    @always_seq(outclk.posedge)
    def read():
        if rd & (not outbusy):
            dout.next = mem[out_addr[ADDR+1:]]
            out_addr.next =  out_addr + modbv(1)[ADDR+1:]
        rdout.next = rd
            
            
    @always_comb
    def wrap():
        if in_addr >= (2**ADDR):
            in_addr.next = in_addr | 2**(ADDR+1)
            
        if out_addr >= (2**ADDR):
            out_addr.next = out_addr | 2**(ADDR+1)

    @always_comb
    def busy():
        diff = in_addr[ADDR+1] ^ out_addr[ADDR+1]

        if (in_addr[:ADDR] == out_addr[:ADDR]):        
            if diff == 1:
                inbusy.next = 1
            elif diff == 0:
                outbusy.next = 1
            else:
                inbusy.next = 0
                outbusy.next =0 
         
        if diff:
            length = UPPER-out_addr + in_addr-LOWER
        else:
            length = in_addr - out_addr
        if length >= 2**ADDR/2:
            hfull.next = 1
        else:
            hfull.next = 0

    return instances
            