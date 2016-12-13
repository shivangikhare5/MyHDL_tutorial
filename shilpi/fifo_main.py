from myhdl import block, instance, Signal, always, delay, modbv, intbv, always_comb, instances, now

# Constants
DATA=8 # Bus Width
ADDRESS=8   # Address Width
DEPTH=(2**ADDRESS)    # Memory Depth - Taken as the total size of memory
# The purpose of UPPER and LOWER was not clear. I could check for overflow and underflow in a queue without it too.

@block
def fifo(clk, wenable, renable, din, dout, rdout, outbusy, inbusy, DATA=DATA, ADDRESS = ADDRESS, DEPTH = DEPTH):

    mem = [Signal(modbv(0)[DATA:]) for i in range(2**ADDRESS)] #Memory
    # Why ADDRESS+1 bit length is taken for these variable pointers? Is it for signed representation?
    in_addr, out_addr, diff  = [Signal(modbv(0)[ADDRESS:]) for i in range(3)] #Pointer Variables


    #Write Module.
    #I didn't get the purpose of always_seq, always_comb ? How is it different from always module.?
    @always(clk.posedge)
    def write_data():
        if wenable:
            mem[in_addr[ADDRESS:]].next = din
            in_addr.next = in_addr + modbv(1)[ADDRESS:]

    #Read Module
    # when rdout is not used, the first element read is '0' which is false. Is that the purpose of rdout here?
    @always(clk.posedge)
    def read_data():
        if renable:
            dout.next = mem[out_addr[ADDRESS:]] 
            out_addr.next = out_addr + modbv(1)[ADDRESS:]
            rdout.next = renable
        else:
            rdout.next = bool(0)

    #Checks and updates overflow underflow conditions
    @always_comb
    def chk_flow():
        diff = in_addr - out_addr

        # Underflow Condition
        if diff == 0:
            outbusy.next = bool(1)
        else:
            outbusy.next = bool(0)

        # Overflow Condition (Why auto wrap doesn't work here, begin modbv types?)
        # Cyclic Queue, 1 Element taken as LOWER
        if out_addr == (in_addr + modbv(1)[ADDRESS:])%DEPTH:
            inbusy.next = bool(1)
        else:
            inbusy.next = bool(0)

    return instances()

# .next for signals. Does it assign value only in the next timestep?
