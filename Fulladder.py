from myhdl import block , always_comb,Signal,intbv,instance,delay,Simulation , ConcatSignal
import random
from random import randrange
 
@block
def fulladd(c_out,s,a,b,c_in):
	
	@always_comb
	def c_outlogic():
		c_out.next = (a & b) | (c_in & (a ^ b))
	
	@always_comb
	def s_logic():
		s.next = a ^ b ^ c_in
		
	return c_outlogic, s_logic 

@block
def bitadder(s,a,b):

	a1 = [a[i] for i in range(4)]
	b1 = [b[i] for i in range(4)]
	
	s1 = [Signal(bool()) for i in range(5)]
	c1 = [Signal(bool()) for i in range(5)]
	c1[0]=0
	s1[4] = c1[4]
	sc = ConcatSignal(*reversed(s1))
	@always_comb
	def assign():
		s.next = sc 
	
	c =[None] * 4
	for i in range(4):
		c[i] = fulladd(a=a1[i], b=b1[i], s=s1[i], c_in=c1[i], c_out=c1[i+1])
	
	return assign,c
	
@block
def tbfadd():

	a, b = [Signal(intbv(0)[4:0]) for i in range(2)]
	s = Signal(intbv(0)[5:0])
	
	ft = bitadder (s,a,b)
	
	@instance
	def tb_logic():
		print("cout s a b ")
		for i in range(10):
			a.next,b.next= [randrange(16) for i in range(2)]
			yield delay(10)
			print("%s %s %s"%(s,a,b))
			
	return tb_logic,ft
	
inst = tbfadd()
sim = Simulation(inst)
sim.run(50)
