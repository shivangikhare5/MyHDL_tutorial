from myhdl import block,always_comb, Signal,intbv ,instance, Simulation ,delay

@block
def compare(q,a,b):

	@always_comb
	def q_logic():
		q.next= (a & b)|((not a) & (not b)) 
		
	return q_logic

import random
from random import randrange

@block
def tbcomp():

	q,a,b=[Signal(intbv(0)) for i in range(3)]
	
	tcomp = compare(q,a,b)
	
	@instance
	def stimulus():
		print("q a b")
		for i in range(10):
			a.next,b.next= [randrange(2)for i in range(2)]
			yield delay(5)
			print("%s %s %s"%(q,a,b))
			
	return tcomp,stimulus
	
inst = tbcomp()
sim = Simulation(inst)
sim.run(40)
