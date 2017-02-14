from myhdl import block,always_comb,Signal,Simulation,instance,delay,block,intbv

@block
def sum(s,c,a,b):
	
	@always_comb
	def sum_logic():
		s.next=a^b
		
	@always_comb
	def carry_logic():
		c.next=a&b
		
	return sum_logic, carry_logic
	
import random
from random import randrange

@block
def testsum():

	s,c,a,b=[Signal(intbv(0)) for i in range(4)]
	
	tsum = sum(s,c,a,b)
	
	@instance
	def stimulus():
		print("s c a b")
		for i in range(12):
			a.next,b.next= randrange(2),randrange(2)
			yield delay(10)
			print("%s %s %s %s"%(s,c,a,b))
			
	return tsum,stimulus
	
inst=testsum()
sim=Simulation(inst)
sim.run(80)
