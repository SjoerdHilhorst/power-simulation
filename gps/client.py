""" Client == master == GreenerEye """

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import config as address

client = ModbusClient('localhost', port=5030)
client.connect()


def read_value(addr):
    fx = addr // address.fx_addr_separator
    addr = addr % address.fx_addr_separator

    if fx == 1:
        val = client.read_coils(addr).bits[0]
    elif fx == 2:
        val = client.read_discrete_inputs(addr).bits[0]
    elif fx == 3:
        val = client.read_holding_registers(addr).registers[0] / address.scaling_factor
    else:
        val = client.read_input_registers(addr).registers[0] / address.scaling_factor
    return val


# examples
print(read_value(address.active_power_out))
print(read_value(address.reactive_power_in))
print(read_value(address.current_l1_in))
print(read_value(address.voltage_l1_l2_out))
print(read_value(address.frequency_out))
print(read_value(address.system_status))
print(read_value(address.input_connected))

client.close()