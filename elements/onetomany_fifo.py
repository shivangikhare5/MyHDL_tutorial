from myhdl import *
from pyhdllib import hdlcfg
from pyhdllib import fifo

ADDR = 4
DATA = 8
WORD = 4
LOWER=4               #lower limit for lane read
UPPER=(2**ADDR)-4     #upper limit for lane write
OFFSET = 2**(ADDR-1)
  

@block
def onetomany_fifo(aBus, din, inclk, outclk, rst, DATA = DATA, ADDR =ADDR, UPPER =UPPER, LOWER =LOWER, OFFSET=OFFSET):
    count = modbv(0)[length:]

    
    fifo_inst+'_'+str((i)= [fifo.fifo(Bus[i].din, Bus[i].we, Bus[i].inbusy, inclk,
                                                  Bus[i].rd, Bus[i].rdout, Bus[i].outbusy, Bus[i].dout, outclk,Bus[i].hfull, rst,
                                                  DATA = DATA, ADDR =ADDR, UPPER =UPPER, LOWER =LOWER, OFFSET=OFFSET) for i in range(4)]
    
    @always(inclk.posedge)
    def count_logic():
            Bus[count].din.next = aBus.din
            count+=1   
    
    return instances()
    
# Define VHDL Conversion function
def onetomany_fifo_convert(DATA=DATA, ADDR=ADDR, UPPER=UPPER, LOWER=LOWER, OFFSET=OFFSET):
    Bus = [fifo.bus(DATA = DATA, ADDR =ADDR) for i in range(4)]
    rst = ResetSignal(0, active=1, async=False)
    inclk, outclk = [Signal(bool(0)) for i in range(2)]    
    
    onetomany_fifo_inst = onetomany_fifo(Bus, inclk, outclk, rst, DATA = DATA, ADDR =ADDR, UPPER =UPPER, LOWER =LOWER, OFFSET=OFFSET)

    onetomany_fifo_inst.convert(hdl='Verilog', header=hdlcfg.header, directory=hdlcfg.hdl_path,
                     name='lane_' + str(DATA)+'_'+ str(ADDR)+'_'+ str(UPPER)+'_'+ str(LOWER)+'_'+ str(OFFSET))
    
if __name__ == '__main__':
    onetomany_fifo_convert(DATA=8, ADDR=4, UPPER=(2**ADDR)-4, LOWER=4, OFFSET=2**(ADDR-1))