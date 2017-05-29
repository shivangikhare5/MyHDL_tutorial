#test bench for fifo
from unittest import TestCase
import unittest
from myhdl import *
import random
from random import randrange
import fifo
from fifo import fifo
ADDR = 4
DATA = 8
LOWER = 0
UPPER = 2**ADDR

class Testfifo(TestCase):
    
    def testReadWrite(self):
        """ Check that buffer can be write and read """
        
        #Creating buffer (random data)
        def createbuff(DATA, ADDR):
            return [Signal(modbv(randrange(2**DATA))) for i in range(2**ADDR)]
        
        
        @block
        def test_fifo():
                     
            din, dout          = [Signal(modbv(0)[DATA:]) for i in range(2)]
            
            rst = ResetSignal(0, active=1, async=False)    
            inclk, outclk,we, rd, inbusy, outbusy, hfull, rdout = [Signal(bool(0)) for i in range(8)]
            
            fifo_inst = fifo(din, we, inbusy, inclk, rd, rdout, outbusy, dout, outclk, hfull, rst, DATA = DATA, ADDR =ADDR, UPPER =UPPER,LOWER =LOWER)
         
            #Clock driver for input
            @always(delay(5))
            def inclkgen(): 
                inclk.next = not inclk
            
            #Clock driver for output
            @always(delay(5))
            def outclkgen(): 
                outclk.next = not outclk

            fifobuff =[]
            fifobuff =createbuff(DATA, 2*ADDR)
            #Driver for reset signal
            @instance
            def stimulus():
                yield delay(15)
                rst.next = 1
                yield delay(10)
                rst.next = 0
                yield delay(10)
                
            #Write driver for fifo    
            @instance
            def write():
                we.next = 0
                yield delay(50)
                i = 0
                while 1:
                    yield inclk.posedge
                    if not inbusy:
                        we.next = 1
                        din.next = fifobuff[i]
                        i +=1
                    else:
                        we.next = 0
                        din.next = 0
                    if i == len(fifobuff):
                        break
                yield inclk.posedge
                we.next = 0
                
            #Read driver for fifo
            @instance
            def read():
                rd.next = 0
                yield outclk.posedge
                while(hfull==0):
                    yield outclk.posedge
                    pass
                yield outclk.posedge
                rd.next = 1
                i = 0
                while(1):
                    yield outclk.posedge
                    if rdout:
                        print(dout,fifobuff[i])                        
                        i +=1;
                        
                yield outclk.posedge
                rd.next = 0
                
            @always_comb
            def flag():
                if inbusy:
                    print("Overflow")
                if outbusy:
                    print("Underflow")
                if hfull:
                    print("Half full")
                    
                    
            return instances()
            
        tb = test_fifo()
        tb.config_sim(trace= True)
        tb.run_sim(duration=2000)
        tb.quit_sim()
    
if __name__ == '__main__':
    unittest.main()