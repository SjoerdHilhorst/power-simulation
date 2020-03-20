""" Client == master == GreenerEye """

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.payload import BinaryPayloadDecoder, Endian

import config as address

client = ModbusClient('localhost', port=5050)
client.connect()


def read_value(addr):
    fx = addr // address.fx_addr_separator
    addr = addr % address.fx_addr_separator

    if fx == 1:
        val = client.read_coils(addr).bits[0]
    elif fx == 2:
        val = client.read_discrete_inputs(addr).bits[0]
    elif fx == 3:
        val = client.read_holding_registers(addr)
    else:
        val = client.read_input_registers(addr).registers[0] / address.scaling_factor
    return val


r = client.read_holding_registers(10, 40, unit=1)
d = BinaryPayloadDecoder.fromRegisters(r.registers, byteorder=Endian.Big, wordorder=Endian.Big)
while 1:
    print(d.decode_32bit_float())

# examples
print(read_value(address.active_power_in))
print(read_value(address.reactive_power_in))
print(read_value(address.current_l1_in))
print(read_value(address.voltage_l1_l2_out))
print(read_value(address.frequency_out))
print(read_value(address.system_status))
print(read_value(address.input_connected))

client.close()