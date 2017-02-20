from myhdl import *

@block
def bit_adder(a, b, cin, s, cout):
    
    @always(a, b, cin)
    def logic():
        print ('#',a, b, cin)
        pass
        #s.next    = a ^ b ^ cin
        #cout.next = (a & b) | ((a ^ b) & cin)
        
    return instances()
