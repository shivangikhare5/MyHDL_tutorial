from myhdl import block, always_comb,Signal,Simulation,delay,intbv,instance
import random
from random import randrange

@block
def encoder(out,ip):

	@always_comb
	def out_logic():
		out.next[0] = ip[3]|((ip[1]) & (1^ip[2]))
		out.next[1] = ip[2]|ip[3]
		
	return out_logic
	
@block
def tb():

	ip = Signal(intbv(0)[4:0])
	out = Signal(intbv(0)[2:0])
	
	enc = encoder(out,ip)
	
	@instance
	def stimulus():
		print("out ip")
		for i in range(10):
			ip.next = randrange(16)
			yield delay(10)
			print("%s %s"%(bin(out),bin(ip)))
			
	return enc, stimulus
	
inst = tb()
sim = Simulation(inst)
sim.run(50)
