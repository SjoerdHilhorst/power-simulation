""" Client == master == GreenerEye """
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

# configure the client logging
import logging

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

client = ModbusClient('localhost', port=5020)
client.connect()

# example requests
# Read: first parameter is the address, second is the number of coils/discretes/registers to read
# Write: first parameter is the address and second is the value to write

log.debug("Reading Coils")
rr = client.read_coils(1, 1)
assert (rr.bits[0] == False)  # test the expected value

log.debug("Write to a Coil and read back")
rq = client.write_coil(0, True)
rr = client.read_coils(0, 1)
assert (rq.function_code < 0x80)  # test that we are not an error
assert (rr.bits[0] == True)  # test the expected value

log.debug("Write to multiple coils and read back")
rq = client.write_coils(1, [True] * 8)
assert (rq.function_code < 0x80)  # test that we are not an error
rr = client.read_coils(1, 21)
assert (rr.function_code < 0x80)  # test that we are not an error
resp = [True] * 21

log.debug("Read discrete inputs")
rr = client.read_discrete_inputs(0, 8)
assert (rq.function_code < 0x80)  # test that we are not an error

log.debug("Write to a holding register and read back")
rq = client.write_register(1, 10)
rr = client.read_holding_registers(1, 1)
a = client.read_holding_registers(2, 1)
assert (rq.function_code < 0x80)  # test that we are not an error
assert (rr.registers[0] == 10)  # test the expected value

log.debug("Write to multiple holding registers and read back")
rq = client.write_registers(1, [10] * 8)
rr = client.read_holding_registers(1, 8)
assert (rq.function_code < 0x80)  # test that we are not an error
assert (rr.registers == [10] * 8)  # test the expected value

log.debug("Read input registers")
rr = client.read_input_registers(1, 8)
assert (rq.function_code < 0x80)  # test that we are not an error

client.close()
