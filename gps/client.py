""" Client == master == GreenerEye
This is a simple client example
for testing if the battery server works
"""

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.payload import BinaryPayloadDecoder, Endian
import config as address


class GreenerEye:

    def __init__(self):
        self.client = ModbusClient('localhost', port=5030)

    def read_value(self, addr):
        fx = addr // address.fx_addr_separator
        addr = addr % address.fx_addr_separator

        if fx == 1:
            val = self.client.read_coils(addr).bits[0]
        elif fx == 2:
            val = self.client.read_discrete_inputs(addr).bits[0]
        elif fx == 3:
            val = self.client.read_holding_registers(addr, 2).registers
        else:
            val = self.client.read_input_registers(addr, 2).registers
        return val

    def scale_float_example(self):
        r = self.client.read_holding_registers(10, 46, unit=1)
        d = BinaryPayloadDecoder.fromRegisters(r.registers, byteorder=Endian.Big, wordorder=Endian.Big)

        # this will print address 310 to 354, IE. all float registers
        for x in range(0, 22):
            print(d.decode_32bit_int() / address.scaling_factor)

        # examples, reading a single value
        r = self.read_value(address.active_power_in)
        d = BinaryPayloadDecoder.fromRegisters(r, byteorder=address.byte_order, wordorder=address.word_order)
        print(d.decode_32bit_int() / address.scaling_factor)

        r = self.read_value(address.reactive_power_in)
        d = BinaryPayloadDecoder.fromRegisters(r, byteorder=address.byte_order, wordorder=address.word_order)
        print(d.decode_32bit_int() / address.scaling_factor)

        r = self.read_value(address.current_l1_in)
        d = BinaryPayloadDecoder.fromRegisters(r, byteorder=address.byte_order, wordorder=address.word_order)
        print(d.decode_32bit_int() / address.scaling_factor)

        r = self.read_value(address.voltage_l1_l2_out)
        d = BinaryPayloadDecoder.fromRegisters(r, byteorder=address.byte_order, wordorder=address.word_order)
        print(d.decode_32bit_int() / address.scaling_factor)

        r = self.read_value(address.frequency_out)
        d = BinaryPayloadDecoder.fromRegisters(r, byteorder=address.byte_order, wordorder=address.word_order)
        print(d.decode_32bit_int() / address.scaling_factor)

    def comb_float_example(self):
        r = self.client.read_holding_registers(10, 46, unit=1)
        d = BinaryPayloadDecoder.fromRegisters(r.registers, byteorder=Endian.Big, wordorder=Endian.Big)

        # this will print address 310 to 354, IE. all float registers
        for x in range(0, 22):
            print(d.decode_32bit_float())

            # examples, reading a single value
        r = self.read_value(address.active_power_in)
        d = BinaryPayloadDecoder.fromRegisters(r, byteorder=address.byte_order, wordorder=address.word_order)
        print(d.decode_32bit_float())

        r = self.read_value(address.reactive_power_in)
        d = BinaryPayloadDecoder.fromRegisters(r, byteorder=address.byte_order, wordorder=address.word_order)

        print(d.decode_32bit_float())

        r = self.read_value(address.current_l1_in)
        d = BinaryPayloadDecoder.fromRegisters(r, byteorder=address.byte_order, wordorder=address.word_order)
        print(d.decode_32bit_float())

        r = self.read_value(address.voltage_l1_l2_out)
        d = BinaryPayloadDecoder.fromRegisters(r, byteorder=address.byte_order, wordorder=address.word_order)
        print(d.decode_32bit_float())

        r = self.read_value(address.frequency_out)
        d = BinaryPayloadDecoder.fromRegisters(r, byteorder=address.byte_order, wordorder=address.word_order)
        print(d.decode_32bit_float())


# uncomment the needed in correspondence with main module
    def run(self):
        self.client.connect()
        print("CLIENT: is running")
        self.scale_float_example()  # works with "DEFAULT" and "CUSTOM" + "SCALE"
        #self.comb_float_example() # works with "CUSTOM" + "COMB"
        self.client.close()


eye = GreenerEye()
eye.run()

