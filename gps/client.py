""" Client == master == GreenerEye
This is a simple client example
for testing if the battery server works
"""

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.payload import BinaryPayloadDecoder, Endian
import json_config


class GreenerEye:
    def __init__(self, env):
        self.address = env['address']
        server_address = env['server_address']
        self.client = ModbusClient(server_address[0], server_address[1])
        self.addr_separator = env['fx_addr_separator']
        self.scaling_factor = env['scaling_factor']

    def read_value(self, addr):
        fx = addr // self.addr_separator
        addr = addr % self.addr_separator

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
        d = BinaryPayloadDecoder.fromRegisters(r.registers, byteorder=env['byte_order'], wordorder=['word_order'])

        # this will print address 310 to 354, IE. all float registers

        
        for x in range(0, 22):
            print(d.decode_32bit_int() / self.scaling_factor)

        # examples, reading a single value
        r = self.read_value(self.address['active_power_in'])
        d = BinaryPayloadDecoder.fromRegisters(r, byteorder=env['byte_order'], wordorder=env['word_order'])
        print(d.decode_32bit_int() / self.scaling_factor)

        r = self.read_value(self.address['reactive_power_in'])
        d = BinaryPayloadDecoder.fromRegisters(r, byteorder=env['byte_order'], wordorder=env['word_order'])
        print(d.decode_32bit_int() / self.scaling_factor)

        r = self.read_value(self.address['current_l1_in'])
        d = BinaryPayloadDecoder.fromRegisters(r, byteorder=env['byte_order'], wordorder=env['word_order'])
        print(d.decode_32bit_int() / self.scaling_factor)

        r = self.read_value(self.address['voltage_l1_l2_out'])
        d = BinaryPayloadDecoder.fromRegisters(r, byteorder=env['byte_order'], wordorder=env['word_order'])
        print(d.decode_32bit_int() / self.scaling_factor)

        r = self.read_value(self.address['frequency_out'])
        d = BinaryPayloadDecoder.fromRegisters(r, byteorder=env['byte_order'], wordorder=env['word_order'])
        print(d.decode_32bit_int() / self.scaling_factor)

    def comb_float_example(self):
        r = self.client.read_holding_registers(10, 46, unit=1)
        d = BinaryPayloadDecoder.fromRegisters(r.registers, byteorder=Endian.Big, wordorder=Endian.Big)

        # this will print address 310 to 354, IE. all float registers
        for x in range(0, 22):
            print(d.decode_32bit_float())

        # examples, reading a single value
        r = self.read_value(self.address['active_power_in'])
        d = BinaryPayloadDecoder.fromRegisters(r, byteorder=env['byte_order'], wordorder=env['word_order'])
        print(d.decode_32bit_float())

        r = self.read_value(self.address['reactive_power_in'])
        d = BinaryPayloadDecoder.fromRegisters(r, byteorder=env['byte_order'], wordorder=env['word_order'])

        print(d.decode_32bit_float())

        r = self.read_value(self.address['current_l1_in'])
        d = BinaryPayloadDecoder.fromRegisters(r, byteorder=env['byte_order'], wordorder=env['word_order'])
        print(d.decode_32bit_float())

        r = self.read_value(self.address['voltage_l1_l2_out'])
        d = BinaryPayloadDecoder.fromRegisters(r, byteorder=env['byte_order'], wordorder=env['word_order'])
        print(d.decode_32bit_float())

        r = self.read_value(self.address['frequency_out'])
        d = BinaryPayloadDecoder.fromRegisters(r, byteorder=env['byte_order'], wordorder=env['word_order'])
        print(d.decode_32bit_float())


# uncomment the needed in correspondence with main module
    def run(self):
        self.client.connect()
        print("CLIENT: is running")
        #self.scale_float_example()  # works with "DEFAULT" and "CUSTOM" + "SCALE"
        self.comb_float_example() # works with "CUSTOM" + "COMB"
        self.client.close()


if __name__ == "__main__":
    env = json_config.get_custom_json("env")
    eye = GreenerEye(env)
    eye.run()

