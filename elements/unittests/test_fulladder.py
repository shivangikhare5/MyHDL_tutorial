import sys, os

from unittest import TestCase
import unittest
from myhdl import *
import fulladder
from random import randrange

class TestFullAdder(TestCase):
    
    def testFullAdder(self):
        
        @block
        def testbench():
            a, b, s, cin, cout = [Signal(bool(0)) for i in range(5)]
            clk = Signal(bool(0))
            addr_inst = fulladder.bit_adder(a, b, s, cin, cout)
            
            @always(delay(10))
            def clkgen():
                clk.next = not clk
            
            @instance
            def write():
                a.next    = bool(0)
                b.next    = 0
                cin.next  = 0
                yield delay(50)      
                for i in range(10):
                    yield clk.posedge
                    a.next = bool(randrange(2))
                    b.next = bool(randrange(2))
                    cin.next = bool(randrange(2))
                    #self.assertEqual(s, a ^ b ^ cin)
                    #self.assertEqual(cout, (a & b) | ((a ^ b) & cin))
                    print(int(a), int(b), int(cin), int(s))
            return instances()        
        
        tb = testbench()
        tb.config_sim(trace=True)
        tb.run_sim(duration=1500)
        tb.quit_sim()

if __name__ == '__main__':
    unittest.main()
