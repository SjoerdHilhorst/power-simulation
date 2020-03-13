""" Client == master == GreenerEye """

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from battery import Battery as battery

import logging

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

client = ModbusClient('localhost', port=5030)
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
    return val

#examples
print(read_value(battery.active_power_out))
print(read_value(battery.reactive_power_in))

#currently do not work because values are not integers!!!
print(read_value(battery.current_l1_in))
print(read_value(battery.voltage_l1_l2_out))
print(read_value(battery.frequency_out))


client.close()
