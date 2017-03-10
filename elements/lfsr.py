from myhdl import block,always_comb,always,instance,Signal,intbv,delay

@block
def fsr(bit,lfsr,load,clk,rst):

	seed = Signal(intbv(0xACE1)[16:])

	@always_comb
	def tap():
		bit.next = (lfsr[0] ^ lfsr[2] ^ lfsr[3] ^ lfsr[5] ) & 1
		'''bit.next = ((lfsr >> 0) ^ (lfsr >> 2) ^ (lfsr >> 3) ^ (lfsr >> 5) ) & 1'''
        
	
	@always(clk.posedge,rst.posedge)
	def logic():
		if load:
			lfsr.next = seed
		else:
			lfsr.next =  (lfsr >> 1) | (bit << 15)
		
	
	return tap,logic
		

