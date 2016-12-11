from unittest import TestCase
import unittest
from myhdl import block, instances, instance, intbv, Signal, ResetSignal, always, delay
from random import randrange
from fifo import cfifo

class TestFifo(TestCase):
    
    def testBuffer(self):
        """ Check that buffer can be write and read """
        ADDR = 4
        DATA = 16
        OFFSET = 8
        LOWER = 4
        UPPER =2**ADDR-4
        WATCHDOG = 3000
        
        def createbuff(DATA, ADDR):
            return [Signal(intbv(randrange(2**DATA))) for i in range(2**4)]
        
        @block
        def test_cfifo(): 
            inclk = Signal(bool(0))
            outclk = Signal(bool(0))
            rst = ResetSignal(0, active=1, async=False)
            
            we, rd, inbusy, outbusy, hfull, rdout = [Signal(bool(0)) for i in range(6)]
            din, dout = [Signal(intbv(0)[DATA:]) for i in range(2)]
            
            fifo_inst = cfifo(inclk, inbusy, we, din, 
                      outclk, outbusy, rd, dout, rdout, hfull, rst,
                      ADDR=ADDR, DATA=DATA, OFFSET=OFFSET, LOWER=LOWER, UPPER=UPPER)
            
            @always(delay(8))
            def inclkgen():
                inclk.next = not inclk
            
            @always(delay(5))
            def outclkgen():
                outclk.next = not outclk
          
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
                    yield inclk.posedge
                    while inbusy:
                        we.next = 0
                        yield inclk.posedge
                        
                    we.next = 1                    
                    din.next = data                        
                        
                yield inclk.posedge
                we.next = 0
                #din.next = 0
                
            @instance
            def read():
                watchdog = 30
                watchctr = 0
                yield delay(250)
                j = 0
                while 1:
                    yield outclk.posedge
                    if watchctr == watchdog:
                        watchctr = 0
                        break
                        
                    if hfull:# not outbausy:
                        rd.next = Signal(bool(1))
                    else:
                        rd.next = Signal(bool(0))
                        watchctr = watchctr + 1
                        #print watchctr
                        
                    if (rdout):
                        print hex(dout), hex(rambuff[j])
                        #self.assertEqual(dout, rambuff[j])
                        j = j + 1
                        
                yield outclk.posedge
                rd.next = Signal(bool(0))
                
                
            return instances()
        
        
        tb = test_cfifo()
        tb.config_sim(trace=True)
        tb.run_sim(duration=1500)
        tb.quit_sim()

    
if __name__ == '__main__':
    unittest.main()