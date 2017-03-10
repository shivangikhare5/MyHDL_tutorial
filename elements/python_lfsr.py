
def LFSR(seed):
	import time

	lfsr = seed
	bit = 0
	f = 0
	print("%s"%hex(seed))
		
	while lfsr!=seed or f==0:
		
		bit = ((lfsr >> 0) ^ (lfsr >> 2) ^ (lfsr >> 3) ^ (lfsr >> 5) ) & 1
		lfsr =  (lfsr >> 1) | (bit << 15)
		print("%s"%hex(lfsr))
		if lfsr == seed:
			f = 1
		time.sleep(0.75)
		
		
		