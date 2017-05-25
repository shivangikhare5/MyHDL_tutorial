#test bench for fifo
from unittest import TestCase
import unittest
from myhdl import *
import random
from random import randrange
import fifo

class Testfifo(TestCase):
    
    def testReadWrite(self):
        """ Check that buffer can be write and read """
        
        #Creating buffer (random data)
        def createbuff(DATA, ADDR):
            return [Signal(modbv(randrange(2**DATA))) for i in range(2**ADDR)]
        
        
        @block
        def test_fifo():
                     
            din, dout = [Signal(intbv(0)[DATA:]) for i in range(2)]
            inclk     = Signal(bool(0))
            in_addr   = Signal(modbv(0)[ADDR+1:])
            dout      = Signal(modbv(0)[DATA:])
            outclk    = Signal(bool(0))
            out_addr  = Signal(modbv(0)[ADDR+1:])
            hfull     = Signal(bool(0))
            DATA      = 8
            ADDR      = 4
            UPPER     = 2**ADDR
            LOWER     = 0    
            we, rd, inbusy, outbusy, hfull, rdout = [Signal(bool(0)) for i in range(6)]
            
            fifo_inst = fifo(din, we, inbusy, inclk, rd, rdout, outbusy, dout, outclk, hfull, DATA, ADDR,UPPER,LOWER)
            
            @always(delay(5))
            def inclkgen(): 
                inclk.next = not inclk
            
            @always(delay(10))
            def outclkgen(): 
                outclk.next = not outclk

            @always(inclk.posedge)
            def write():
                we.next = 0
                yield delay(10)
                
               