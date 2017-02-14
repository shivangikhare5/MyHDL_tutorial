@block
def bit_adder(oper_a, oper_b, res_sum, oper_cin, oper_cout):

	@always_comb
	def logic():
		for i in range(5):
			res_sum.next[i] = oper_a[i] ^ (oper_b[i] ^ oper_cin)
			oper_cout.next = (oper_b[i] & (not oper_cin)) | (oper_a[i] & (not oper_cin)) | (oper_a[i] & oper_b[i])

	return instances()

def testbench():
	oper_a, oper_b = [Signal(intbv(0)[5:]) for i in range(2)]
	oper_cin, oper_cout = [Signal(bool()) for i in range(2)]

	oper_sum = Signal(intbv(0)[5:])
	process = bit_adder(oper_a, oper_b, oper_sum, oper_cin, oper_cout)

	@always_comb
	def update_cin():
		oper_cin.next = oper_cout

	@instance
	def stimulus():
		for i in range(20):
			oper_a.next, oper_b.next = randrange(16), randrange(16)
			yield delay(1)
			print (oper_a, oper_b, oper_sum)
			print (bin(oper_a), bin(oper_b), bin(oper_sum), oper_cin)
			print ("")


	return instances();

inst = testbench()
sim = Simulation(inst)
sim.run(50)
