""" Client == master == GreenerEye
This is a simple client example
for testing if the battery server works
"""

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
        val = client.read_holding_registers(addr, 2).registers
    else:
        val = client.read_input_registers(addr, 2).registers
    return val


def scale_float_example():
    r = client.read_holding_registers(10, 46, unit=1)
    d = BinaryPayloadDecoder.fromRegisters(r.registers, byteorder=Endian.Big, wordorder=Endian.Big)

    # this will print address 310 to 354, IE. all float registers
    for x in range(0, 22):
        print(d.decode_32bit_int() / address.scaling_factor)

    # examples, reading a single value
    r = read_value(address.active_power_in)
    d = BinaryPayloadDecoder.fromRegisters(r, byteorder=address.byte_order, wordorder=address.word_order)
    print(d.decode_32bit_int() / address.scaling_factor)

    r = read_value(address.reactive_power_in)
    d = BinaryPayloadDecoder.fromRegisters(r, byteorder=address.byte_order, wordorder=address.word_order)
    print(d.decode_32bit_int() / address.scaling_factor)

    r = read_value(address.current_l1_in)
    d = BinaryPayloadDecoder.fromRegisters(r, byteorder=address.byte_order, wordorder=address.word_order)
    print(d.decode_32bit_int() / address.scaling_factor)

    r = read_value(address.voltage_l1_l2_out)
    d = BinaryPayloadDecoder.fromRegisters(r, byteorder=address.byte_order, wordorder=address.word_order)
    print(d.decode_32bit_int() / address.scaling_factor)

    r = read_value(address.frequency_out)
    d = BinaryPayloadDecoder.fromRegisters(r, byteorder=address.byte_order, wordorder=address.word_order)
    print(d.decode_32bit_int() / address.scaling_factor)


def comb_float_example():
    r = client.read_holding_registers(10, 46, unit=1)
    d = BinaryPayloadDecoder.fromRegisters(r.registers, byteorder=Endian.Big, wordorder=Endian.Big)

    # this will print address 310 to 354, IE. all float registers
    for x in range(0, 22):
        print(d.decode_32bit_float())

        # examples, reading a single value
    r = read_value(address.active_power_in)
    d = BinaryPayloadDecoder.fromRegisters(r, byteorder=address.byte_order, wordorder=address.word_order)
    print(d.decode_32bit_float())

    r = read_value(address.reactive_power_in)
    d = BinaryPayloadDecoder.fromRegisters(r, byteorder=address.byte_order, wordorder=address.word_order)

    print(d.decode_32bit_float())

    r = read_value(address.current_l1_in)
    d = BinaryPayloadDecoder.fromRegisters(r, byteorder=address.byte_order, wordorder=address.word_order)
    print(d.decode_32bit_float())

    r = read_value(address.voltage_l1_l2_out)
    d = BinaryPayloadDecoder.fromRegisters(r, byteorder=address.byte_order, wordorder=address.word_order)
    print(d.decode_32bit_float())

    r = read_value(address.frequency_out)
    d = BinaryPayloadDecoder.fromRegisters(r, byteorder=address.byte_order, wordorder=address.word_order)
    print(d.decode_32bit_float())


if __name__ == '__main__':
    client = ModbusClient('localhost', port=5050)
    client.connect()
    if address.float_mode == "COMB":
        comb_float_example()
    elif address.float_mode == "SCALE":
        scale_float_example()

    # booleans are not encoded, and can therefore be read directly from the modbus server
    print(read_value(address.converter_started))
    print(read_value(address.input_connected))
    client.close()
