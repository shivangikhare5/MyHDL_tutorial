from myhdl import block,always_comb,always

@block
def fsr(bit,lfsr,clk):

	@always_comb
	def tap():
		bit.next = (lfsr[0] ^ lfsr[2] ^ lfsr[3] ^ lfsr[5] ) & 1
		'''bit.next = ((lfsr >> 0) ^ (lfsr >> 2) ^ (lfsr >> 3) ^ (lfsr >> 5) ) & 1'''
        
	
	@always(clk.posedge)
	def logic():
		lfsr.next =  (lfsr >> 1) | (bit << 15)
				
	return tap,logic
		

