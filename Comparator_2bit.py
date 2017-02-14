from myhdl import block,always_comb,Signal,intbv ,instance, Simulation ,delay

@block
def compare(q,p_0,p_1,a,b):

	@always_comb
	def p_logic():
		p_0.next = (a[0] & b[0])|( (not a[0]) & (not b[0]))
		p_1.next = (a[1] & b[1])|( (not a[1]) & (not b[1]))

	@always_comb
	def q_logic():
		q.next = p_0 & p_1
         		
	return p_logic,q_logic

import random
from random import randrange

@block
def tbcomp():

	q,p_0,p_1 = [Signal(intbv(0)) for i in range(3)]
	a,b = [Signal(intbv(0)[2:]) for i in range(2)]
	
	tcomp = compare(q,p_0,p_1,a,b)
	
	@instance
	def stimulus():
		print("q a b")
		for i in range(10):
			a.next,b.next = [randrange(4) for i in range(2)]
			yield delay(5)
			print("%s %s %s"%(q,bin(a),bin(b)))
			
	return tcomp,stimulus
	
inst = tbcomp()
sim = Simulation(inst)
sim.run(40)
