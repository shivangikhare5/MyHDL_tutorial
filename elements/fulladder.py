from myhdl import *

@block
def bit_adder(a, b, cin, s, cout):
    
    @always_comb
    def logic():
        s.next    = a ^ b ^ cin
        cout.next = (a & b) | ((a ^ b) & cin)
        
    return instances()

@block
def bit_adder_vec(a, b, cin, s, cout, DATA=2):
    c = [Signal(bool(0)) for i in range(DATA+1)]
    sv = [Signal(bool(0)) for i in range(DATA)]
    addr_inst = [None for i in range(DATA)]
    
    for i in range(DATA):
        addr_inst[i] = bit_adder(a(i), b(i), c[i], sv[i], c[i+1])
        
    p = [sv[i] for i in reversed(range(DATA))]
    q = ConcatSignal(*p) 
    
    @always_comb
    def logic0():
        c[0].next = cin
        s.next = q
        
    @always_comb
    def logic1():
        cout.next = c[DATA]
        
    return instances()