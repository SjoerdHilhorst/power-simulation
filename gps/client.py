""" Client == master == GreenerEye
This is a simple client example
for testing if the battery server works
"""

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.payload import BinaryPayloadDecoder, Endian


# address = json_config.get_data("custom")

class GreenerEye:
    def __init__(self, env):
        self.address = env['address']
        server_address = env['server_address']
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
            val = self.client.read_holding_registers(addr, 2).registers
        else:
            val = self.client.read_input_registers(addr, 2).registers
        return val

    def from_registers(self, r):
        return BinaryPayloadDecoder.fromRegisters(r.registers, byteorder=self.byte_order, wordorder=self.word_order)

    def scale_float_example(self):
        r = self.client.read_holding_registers(10, 46, unit=1)
        d = self.from_registers(r)

        # this will print address 310 to 354, IE. all float registers

        for x in range(0, 22):
            print(d.decode_32bit_int() / self.scaling_factor)

        # examples, reading a single value
        r = self.read_value(self.address['active_power_in'])
        d = self.from_registers(r)
        print(d.decode_32bit_int() / self.scaling_factor)

        r = self.read_value(self.address['reactive_power_in'])
        d = self.from_registers(r)
        print(d.decode_32bit_int() / self.scaling_factor)

        r = self.read_value(self.address['current_l1_in'])
        d = self.from_registers(r)
        print(d.decode_32bit_int() / self.scaling_factor)

        r = self.read_value(self.address['voltage_l1_l2_out'])
        d = self.from_registers(r)
        print(d.decode_32bit_int() / self.scaling_factor)

        r = self.read_value(self.address['frequency_out'])
        d = self.from_registers(r)
        print(d.decode_32bit_int() / self.scaling_factor)

    def comb_float_example(self):
        r = self.client.read_holding_registers(10, 46, unit=1)
        d = BinaryPayloadDecoder.fromRegisters(r.registers, byteorder=Endian.Big, wordorder=Endian.Big)

        # this will print address 310 to 354, IE. all float registers
        for x in range(0, 20):
            print(d.decode_32bit_float())

        # examples, reading a single value
        r = self.read_value(self.address['active_power_in'])
        d = self.from_registers(r)
        print(d.decode_32bit_float())

        r = self.read_value(self.address['reactive_power_in'])
        d = self.from_registers(r)

        print(d.decode_32bit_float())

        r = self.read_value(self.address['current_l1_in'])
        d = self.from_registers(r)
        print(d.decode_32bit_float())

        r = self.read_value(self.address['voltage_l1_l2_out'])
        d = self.from_registers(r)
        print(d.decode_32bit_float())

        r = self.read_value(self.address['frequency_out'])
        d = self.from_registers(r)
        print(d.decode_32bit_float())

    # uncomment the needed in correspondence with main module
    def run(self):
        self.client.connect()
        print("CLIENT: is running")
        #self.scale_float_example()  # works with "DEFAULT" and "CUSTOM" + "SCALE"
        self.comb_float_example() # works with "CUSTOM" + "COMB"
        self.client.close()


if __name__ == "__main__":
    from config.env import env
    eye = GreenerEye(env)
    eye.run()

