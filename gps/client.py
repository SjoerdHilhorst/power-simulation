""" Client == master == GreenerEye
This is a simple client example
for testing if the battery server works
"""

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.payload import BinaryPayloadDecoder
import json


# address = json_config.get_data("custom")

class GreenerEye:
    def __init__(self, env):
        self.float_mode = env["float_store"]["float_mode"]
        #Gets the currently used address
        with open('./config/current_address.json') as json_file:
            server_address = json.load(json_file)
        self.client = ModbusClient(server_address[0], server_address[1])
        self.scaling_factor = env["float_store"]['scaling_factor']
        self.byte_order = env["float_store"]["byte_order"]
        self.word_order = env["float_store"]["word_order"]

    def read_value(self, addr):
        fx = addr[0]
        addr = addr[1]

        if fx == 1:
            val = self.client.read_coils(addr).bits[0]
        elif fx == 2:
            val = self.client.read_discrete_inputs(addr).bits[0]
        elif fx == 3:
            val = self.client.read_holding_registers(addr, 2)
        else:
            val = self.client.read_input_registers(addr, 2).registers
        return val

    def from_registers(self, r):
        return BinaryPayloadDecoder.fromRegisters(r.registers, byteorder=self.byte_order, wordorder=self.word_order)

    # Prints from registers, as either comb or scale
    def example_output(self, mode):
        r = self.client.read_holding_registers(10,46,unit=1)
        d = self.from_registers(r)
        results = []
        for x in range(0,22):
            results.append(d.decode_32bit_float() if mode == "COMB" else d.decode_32bit_int() / self.scaling_factor)
        print(results)

        '''
        # examples, reading a single value
        r = self.read_value(self.address['active_power_in'])
        d = self.from_registers(r)
        self.print(d.decode_32bit_float() if is_comb else d.decode_32bit_int() / self.scaling_factor)
        '''

    # uncomment the needed in correspondence with main module
    def run(self):
        self.client.connect()
        print("CLIENT: is running")
        self.example_output(self.float_mode)
        self.client.close()


if __name__ == "__main__":
    from config.env import env
    eye = GreenerEye(env)
    eye.run()

