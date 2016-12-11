# fifo.py - First In First Out (Queue Datastructure)
# from myhdl import *

from myhdl import block, Signal, now, always, instance, delay, modbv, instances 
data_arr = [] # The array on which queue is implemented
MAX_SIZE = 500 # Define a max size of the array


'''Now as a primer let me introduce you one basic concept of HDL. In HDL we talk about two entities.
1) DUT- Device Under Test
2) Test Bench

So always write to code them separately. 
from HDL point of view @block can be seen as a unit module. For example I can define complete DUT in a singal @block. Similarly I can also define complete Test Bench in another @block. 

So in order to retain modularity let me modify your code to club into two blocks
'''

@block
def fifo_dut(clk, input_data, output_data):
    '''The push instances
    input_data: The data to be pushed in the queue
    clk : clock Signal'''
    @always(clk.posedge)
    def do_write():
        if len (data_arr) >= MAX_SIZE:
            print ("Overflow. No more elements could be inserted")
        else:
            data_arr.insert(0, input_data.val) #Pushing the element on index 0
            print ("Pushed data %s" %(input_data.val))

    '''The pop block
    output_data: Data is popped (Stored) into it.
    clk : Clock Signal'''
    @always(clk.posedge)
    def do_read():
        if len(data_arr) == 0:
            print "Underflow occured. No elements to pop"
        else:
            output_data.next = data_arr.pop()
            print ("Data pop: %s" %(output_data.val))

    return instances() #return all the instances no need to name all the instances


# The clock driver block.
@block
def fifo_testbench():
    clk = Signal(bool(0))
    input_data, output_data, counter = [Signal(modbv(0)[8:]) for i in range(3)]
    counter = Signal(modbv(0)[8:])
    #Sample input data array (To be pushed in the queue)
    input_list = [i for i in range(1,100)]

    fifo_inst = fifo_dut(clk, input_data, output_data)

    #fifo_inst.convert(hdl='Verilog') #To convert DUT into verilog

    @instance
    def drive_clk():
        while True:
            yield delay(10)
            clk.next = not clk

    @instance
    def do_set_write_data():
        while True:
            yield clk.posedge
            input_data.next = input_list[counter]
            counter.next += 1

    return instances()

tb = fifo_testbench()
tb.config_sim(trace=True)
tb.run_sim(duration=1500)

'''Now this works but will not help in writing HDL as HDL doesn't know anything about push and pop.'''
tb.quit_sim()

