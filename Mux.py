from myhdl import block,always_comb,Signal,intbv ,instance,delay,Simulation
import random
from random import randrange

@block
def mux(out,input ,select):
	
	@always_comb
	def mux_logic():
		out.next = input[select]
		
	return mux_logic
	
@block
def tbmux():
	
	input = Signal(intbv(0)[8:])
	select = Signal (intbv(0)[3:])
	out = Signal(intbv(0))
	
	tmux = mux(out ,input ,select)
	
	@instance
	def stimulus():
		print("out input select")
		for i in range(10):
			input.next = randrange(256)
			select.next = randrange(8)
			yield delay(10)
			print("%s %s %s"%(out,bin(input),select))
	
	return tmux, stimulus
	
inst = tbmux()
Simulation(inst).run(50)
