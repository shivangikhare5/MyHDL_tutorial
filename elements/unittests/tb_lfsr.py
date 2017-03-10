from myhdl import block,always_comb,always,delay,intbv,instance,Signal,now,ResetSignal
import unittest
from unittest import TestCase
from lfsr import fsr
import random
from random import randrange

class TestLFSR(TestCase):

	def testlfsr(self):
	
		@block
		def testbench():
		
			clk = Signal(bool(0))
			f = Signal(bool(0))
			bit = Signal(intbv(0)[16:])
			rst = ResetSignal(0,active = 0,async = True)
			seed = Signal(intbv(0xACE1)[16:])
			lfsr = Signal(intbv(0)[16:])
			load = Signal(bool(1))
			
			tbfsr = fsr(bit,lfsr,load,clk,rst)
			
			tbfsr.convert(hdl='Verilog',name='LFSR')
			
			@always(delay(10))
			def clkgen():
				clk.next = not clk
				
				
			@instance
			def stimulus():
				rst.next =  0
				yield clk.negedge	
				rst.next = 1
				
			@always_comb
			def stp():
				if lfsr!=seed:
					f.next=1
				
			@instance
			def tfsr():
				yield rst.posedge
				yield delay(2)
				load.next = 0
				print(lfsr)
				while lfsr!=seed or f==0:
					yield clk.posedge
					self.assertEqual(bit ,(lfsr[0] ^ lfsr[2] ^ lfsr[3] ^ lfsr[5] ) & 1)
					print((lfsr >> 1) | (bit << 15),end='')
					yield delay(1)
					print("\t%s"%lfsr)
	
			return tfsr,clkgen,tbfsr,stimulus
			
		tb = testbench()
		tb.config_sim(trace=True)
		tb.run_sim(duration=100)
		tb.quit_sim()
		
if __name__ == '__main__':
    unittest.main()
