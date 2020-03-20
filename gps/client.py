""" Client == master == GreenerEye """

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from twisted.internet.task import LoopingCall

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
            val = self.client.read_holding_registers(addr).registers[0] / address.scaling_factor
        else:
            val = self.client.read_input_registers(addr).registers[0] / address.scaling_factor
        return val

    def run(self):
        self.client.connect()
        print("CLIENT: is running")
        print("CLIENT: ", self.read_value(address.soc))
        self.client.close()

# eye = GreenerEye()
# eye.run()
