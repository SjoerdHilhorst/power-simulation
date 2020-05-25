""" Client == master == GreenerEye
This is a simple client example
for testing if the battery server works
"""

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from config.var_names import *
from pymodbus.payload import BinaryPayloadDecoder


class GreenerEye:
    def __init__(self, env):
        self.field = env['fields']
        server_address = env['server_address']
        self.client = ModbusClient(server_address[0], server_address[1])
        self.d_s_factor = env["float_store"]['default_scaling_factor']
        self.byte_order = env["float_store"]["byte_order"]
        self.word_order = env["float_store"]["word_order"]

    def read_value(self, field):
        fx = field['reg_type']
        addr = field['address']

        if fx == 1:
            return self.client.read_coils(addr).bits[0]
        elif fx == 2:
            return self.client.read_discrete_inputs(addr).bits[0]
        elif fx == 3:
            encoding = field['encode']
            val = self.client.read_holding_registers(addr, 2)
        else:
            encoding = field['encode']
            val = self.client.read_input_registers(addr, 2).registers

        d = self.from_registers(val)

        decode_type = {
            INT8: lambda: d.decode_8bit_int(),
            UINT8: lambda: d.decode_8bit_uint(),
            INT16: lambda: d.decode_16bit_int(),
            UINT16: lambda: d.decode_16bit_uint(),
            INT32: lambda: d.decode_32bit_int(),
            UINT32: lambda: d.decode_32bit_uint(),
            FLOAT32: lambda: d.decode_32bit_float(),
        }

        if encoding['e_type'] == SCALE:
            return decode_type[encoding['d_type']]() / encoding.get('s_factor', self.d_s_factor)
        if encoding['e_type'] == COMB:
            return decode_type[encoding['d_type']]()

    def from_registers(self, r):
        return BinaryPayloadDecoder.fromRegisters(r.registers, byteorder=self.byte_order, wordorder=self.word_order)

    def read_float_example(self):
        # examples, reading a single value
        r = self.read_value(self.field['active_power_in'])
        print(r)

        r = self.read_value(self.field['reactive_power_in'])
        print(r)

        r = self.read_value(self.field['current_l1_in'])
        print(r)

        r = self.read_value(self.field['voltage_l1_l2_out'])
        print(r)

        r = self.read_value(self.field['frequency_out'])
        print(r)

        r = self.read_value(self.field['system_mode'])
        print(r)

    def set_converter_started(self, bit):
        self.client.write_coil(self.field['converter_started']['address'], bit)

    def set_input_connected(self, bit):
        self.client.write_coil(self.field['input_connected']['address'], bit)

    def run(self):
        self.client.connect()
        print("CLIENT: is running")
        # self.read_float_example()

        self.set_converter_started(False)
        self.set_input_connected(False)

        self.read_float_example()


if __name__ == "__main__":
    from src.config.env import env

    eye = GreenerEye(env)
    eye.run()
