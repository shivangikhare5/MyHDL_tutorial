from unittest import TestCase
import unittest
from myhdl import *
import dpram
from random import randrange

ADDR = 4
DATA = 8
        
class TestDpram(TestCase):
    
    def testReadWrite(self):
        """ Check that buffer can be write and read """
        
        #Creating buffer (random data)
        def createbuff(DATA, ADDR):
            return [Signal(modbv(randrange(2**DATA))) for i in range(2**ADDR)]
        
        @block
        def test_dpram(): 
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
            
            #Creating dpram-instance
            dpram_inst = dpram.dpram(clk,
            a_din, a_addr, a_we, a_dout, a_rd, a_rdout,
            b_din, b_addr, b_we, b_dout, b_rd, b_rdout,
            DATA=8, ADDR=4)
            
            #Clock driver
            @always(delay(5))
            def clkgen():
                clk.next = not clk
            
            dprambuff=[]
            dprambuff = createbuff(DATA, ADDR)

            # For port A            
            @instance
            def a_write():
                a_we.next = Signal(bool(0))
                yield delay(50)
                
                for i in range(len(rambuff)):                        
                    yield clk.posedge
                    a_we.next = 1
                    a_addr.next = i
                    a_din.next = rambuff[i]                  
                        
                yield clk.posedge
                a_we.next = 0
                
                yield delay(50)
                yield clk.posedge
                a_rd.next = 1     #To make rd=1 to make read() of ram functional
                a_addr.next = 0   #To make dout read the first addr i.e. '0' since in given for loop addr.next works in next iteration
                yield clk.posedge
                for i in range(1,len(rambuff)):                        
                    a_rd.next = 1
                    a_addr.next = i
                    yield clk.posedge
                    
                a_rd.next = 0
                
            @instance
            def a_read():
                i = 0
                while(1):
                    yield clk.posedge
                    if a_rdout:
                        print(a_dout, rambuff[i])
                        self.assertEqual(a_dout, rambuff[i])                    
                        i+=1

            # For port B
            @instance
            def b_write():
                b_we.next = Signal(bool(0))
                yield delay(50)
                
                for i in range(len(rambuff)):                        
                    yield clk.posedge
                    b_we.next = 1
                    b_addr.next = i
                    b_din.next = rambuff[i]                  
                        
                yield clk.posedge
                b_we.next = 0
                
                yield delay(50)
                yield clk.posedge
                b_rd.next = 1     #To make rd=1 to make read() of ram functional
                b_addr.next = 0   #To make dout read the first addr i.e. '0' since in given for loop addr.next works in next iteration
                yield clk.posedge
                for i in range(1,len(rambuff)):                        
                    b_rd.next = 1
                    b_addr.next = i
                    yield clk.posedge
                    
                b_rd.next = 0
                
            @instance
            def b_read():
                i = 0
                while(1):
                    yield clk.posedge
                    if b_rdout:
                        print(b_dout, rambuff[i])
                        self.assertEqual(b_dout, rambuff[i])                    
                        i+=1
                
            return instances()
        
        
        tb = test_dpram()
        tb.config_sim(trace=True)
        tb.run_sim(duration=1500)
        tb.quit_sim()

    
if __name__ == '__main__':
    unittest.main()
