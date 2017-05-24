#File for testcases of ram module

from unittest import TestCase
import unittest
from myhdl import *
import ram
from random import randrange

ADDR = 3
DATA = 8
        
class TestRam(TestCase):
    
    def testReadWrite(self):
        """ Check that buffer can be write and read """
        
        #Creating buffer (random data)
        def createbuff(DATA, ADDR):
            return [Signal(modbv(randrange(2**DATA))) for i in range(2**ADDR)]
        
        @block
        def test_ram(): 
            clk    = Signal(bool(0))
            din    = Signal(modbv(0)[DATA:])
            addr   = Signal(modbv(0)[ADDR:])
            we     = Signal(bool(0))
            dout   = Signal(modbv(0)[DATA:])
            rd     = Signal(bool(0))
            rdout  = Signal(bool(0))
            
            #Creating ram-instance
            ram_inst = ram.ram(clk, din, addr, we, dout, rd, rdout, DATA=8, ADDR=4)
            
            #Clock driver
            @always(delay(5))
            def clkgen():
                clk.next = not clk
            
            rambuff=[]
            rambuff = createbuff(DATA, ADDR)
                        
            @instance
            def write():
                we.next = Signal(bool(0))
                yield delay(50)
                
                for i in range(len(rambuff)):                        
                    yield clk.posedge
                    we.next = 1
                    addr.next = i
                    din.next = rambuff[i]                  
                        
                yield clk.posedge
                we.next = 0
                
                yield delay(50)
                yield clk.posedge
                rd.next = 1     #To make rd=1 to make read() of ram functional
                addr.next = 0   #To make dout read the first addr i.e. '0' since in given for loop addr.next works in next iteration
                yield clk.posedge
                for i in range(1,len(rambuff)):                        
                    rd.next = 1
                    addr.next = i
                    yield clk.posedge
                    
                rd.next = 0
                
            @instance
            def read():
                i = 0
                while(1):
                    yield clk.posedge
                    if rdout:
                        print(dout, rambuff[i])
                        self.assertEqual(dout, rambuff[i])                    
                        i+=1
                    
                
            return instances()
        
        
        tb = test_ram()
        tb.config_sim(trace=True)
        tb.run_sim(duration=1500)
        tb.quit_sim()

    
if __name__ == '__main__':
    ADDR = int(input("Please input size of ADDR"))
    DATA = int(input("Please input size of DATA"))
    unittest.main()
