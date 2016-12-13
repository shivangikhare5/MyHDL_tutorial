from myhdl import block, instances, Signal, modbv, ResetSignal, intbv, always, delay, instance, now
from unittest import TestCase
import unittest
from fifo_main import fifo
from random import randrange

class TestFifo(TestCase):

    def testFifoBuffer(self):
        ADDR = 4
        DATA = 4
        DEPTH = 2**ADDR

        def createbuff(DATA, ADDR):
            return [Signal(intbv(randrange(2**DATA))) for i in range(2**4)]

        @block
        def tb_fifo():
            clk = Signal(bool(0))
            we, rd, inbusy, outbusy, rdout = [Signal(bool(0)) for i in range(5)]
            din, dout = [Signal(intbv(0)[DATA:]) for i in range(2)]

            fifo_inst = fifo(clk, we, rd, din, dout, rdout, outbusy,  inbusy, DATA=DATA, ADDRESS=ADDR, DEPTH=DEPTH)
            fifo_inst.convert(hdl='Verilog', name='fifo_' + str(ADDR)+ '_' + str(DATA)+ '_' + str(DEPTH))

            @always(delay(8))
            def clkgen():
                clk.next = not clk

            rambuff = createbuff(DATA, ADDR)

            @instance
            def write():
                we.next = Signal(bool(0))
                yield delay(5)

                for data in rambuff:
                    yield clk.posedge

                    while inbusy:
                        we.next = 0
                        yield clk.posedge
                    we.next = 1
                    din.next = data

                yield clk.posedge
                we.next = 0

            @instance
            def read():
                yield delay(10)
                j = 0
                while 1:
                    yield clk.posedge
                    if not outbusy:
                        rd.next = Signal(bool(1))
                    else:
                        rd.next = Signal(bool(0))

                    yield delay(1)
                    if rdout:
                        print ("Time: %s, Data  %s : %s, Index : %s" %(now(), dout, rambuff[j], j))
                        j = j+1

                yield clk.posedge
                rd.next = Signal(bool(0))


            return instances()


        tb = tb_fifo()
        tb.config_sim(trace=True)
        tb.run_sim(duration=150)
        tb.quit_sim()

if __name__ == '__main__':
    unittest.main()
