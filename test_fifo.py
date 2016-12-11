from unittest import TestCase
import unittest
from myhdl import block, instances, Signal, modbv, ResetSignal, intbv, always, delay, instance
from fifo import fifo
from random import randrange

class TestFifo(TestCase):
    
    def testFifoBuffer(self):
        """ Check that fifo can be write and read """
        ADDR = 4
        DATA = 16
        OFFSET = 8
        LOWER = 4
        UPPER =2**ADDR-4
        WATCHDOG = 3000
        def createbuff(DATA, ADDR):
            return [Signal(intbv(randrange(2**DATA))) for i in range(2**4)]
     
        @block
        def tb_fifo(): 
            clk = Signal(bool(0))
            rst = ResetSignal(0, active=1, async=False)
            
            we, rd, inbusy, outbusy, hfull, rdout = [Signal(bool(0)) for i in range(6)]
            din, dout = [Signal(intbv(0)[DATA:]) for i in range(2)]
            
            fifo_inst = fifo(clk, inbusy, we, din, 
                      outbusy, rd, dout, rdout, rst,
                      ADDR=ADDR, DATA=DATA, OFFSET=OFFSET, LOWER=LOWER, UPPER=UPPER)
            fifo_inst.convert(hdl='Verilog', name='fifo_' + str(ADDR)+'_'+ str(DATA)+'_'
                          + str(OFFSET)+'_'+ str(LOWER)+'_'+ str(UPPER))
            @always(delay(8))
            def clkgen():
                clk.next = not clk
            
            rambuff = createbuff(DATA, ADDR) 
            
            @instance
            def stimulus():
                yield delay(20)
                rst.next = 1
                yield delay(20)
                rst.next = 0
                yield delay(20)
                
            @instance
            def write():
                we.next = Signal(bool(0))
                yield delay(50)
                
                for data in rambuff:                        
                    yield clk.posedge
                    while inbusy:
                        we.next = 0
                        yield clk.posedge
                        
                    we.next = 1                    
                    din.next = data                        
                        
                yield clk.posedge
                we.next = 0
                #din.next = 0
                
            @instance
            def read():
                watchdog = 30
                watchctr = 0
                yield delay(250)
                j = 0
                while 1:
                    yield clk.posedge
                    if watchctr == watchdog:
                        watchctr = 0
                        break
                        
                    if not outbusy:
                        rd.next = Signal(bool(1))
                    else:
                        rd.next = Signal(bool(0))
                        watchctr = watchctr + 1
                        #print watchctr
                        
                    if (rdout):
                        print hex(dout), hex(rambuff[j])
                        #self.assertEqual(dout, rambuff[j])
                        j = j + 1
                        
                yield clk.posedge
                rd.next = Signal(bool(0))
                
                
            return instances()
        
        
        tb = tb_fifo()
        tb.config_sim(trace=True)
        tb.run_sim(duration=1500)
        tb.quit_sim()

if __name__ == '__main__':
    unittest.main()