""" Client == master == GreenerEye """

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import register_variables as address

import logging

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

client = ModbusClient('localhost', port=5020)
client.connect()

# example requests

log.debug("Read state of charge")
rr = client.read_holding_registers(address.soc)
assert (rr.registers[address.soc] == 100)
print(rr.registers[address.soc])

log.debug("Update state of charge")
client.write_registers(address.soc, 99)

log.debug("Read state of charge")
rr = client.read_holding_registers(address.soc)
assert (rr.registers[address.soc] == 99)
print(rr.registers[address.soc])

client.close()
