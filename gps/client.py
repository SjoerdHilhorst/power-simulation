""" Client == master == GreenerEye """

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from def_config import Battery as battery

import logging

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

client = ModbusClient('localhost', port=5020)
client.connect()


def read_value(addr):
    fx = addr // 100
    address = addr % 100
    if fx == 1:
        val = client.read_coils(address).bits
    elif fx == 2:
        val = client.read_discrete_inputs(address).bits
    elif fx == 3:
        val = client.read_holding_registers(address).registers
    else:
        val = client.read_input_registers(address).registers
    return val[0]


print(read_value(battery.soc))
print(read_value(battery.accept_values))

client.close()
