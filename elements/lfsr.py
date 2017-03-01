from myhdl import block,always_comb,always,delay,intbv,instance,Signal,now
import unittest
from unittest import TestCase
from random import randrange

@block
def fsr(bit,lfsr,clk):

	@always_comb
	def tap():
		bit.next = ((lfsr >> 0) ^ (lfsr >> 2) ^ (lfsr >> 3) ^ (lfsr >> 5) ) & 1
        
	
	@always(clk.posedge)
	def logic():
		lfsr.next =  (lfsr >> 1) | (bit << 15)
		
	return tap,logic
		
class TestLFSR(TestCase):

	def testlfsr(self):
	
		@block
		def testbench():
		
			clk = Signal(bool(0))
			f = Signal(bool(0))
			bit = Signal(intbv(0)[16:])
			seed = Signal(intbv(0xACE1)[16:])
			lfsr = seed
			
			tbfsr = fsr(bit,lfsr,clk)
			
			@always(delay(10))
			def clkgen():
				clk.next = not clk
				
			@always_comb
			def stp():
				if lfsr!=seed:
					f.next=1
				
			@instance
			def tfsr():
				while lfsr!=seed or f==0:
					yield clk.posedge
					print(lfsr)
					
			return tfsr,clkgen,tbfsr
			
		tb = testbench()
		tb.config_sim(trace=True)
		tb.run_sim(duration=1000)
		tb.quit_sim()
if __name__ == '__main__':
    unittest.main()