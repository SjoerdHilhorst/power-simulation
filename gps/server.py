""" Server == slave == Battery """


from pymodbus.server.sync import StartTcpServer
import logging

from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
import def_config as address

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)


def set_value(addr, value):
    fx = addr // 100
    address = addr % 100
    store.setValues(fx, address, [value])


def get_value(addr):
    fx = addr // 100
    address = addr % 100
    return store.getValues(fx, address, 1)[0]


# initialize  data store
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock.create(),  # discrete input (1 bit, read-only)
    co=ModbusSequentialDataBlock.create(),  # coils (1 bit, read-write)
    hr=ModbusSequentialDataBlock.create(),  # holding registers (16 bit, read-write)
    ir=ModbusSequentialDataBlock.create())  # input registers (16 bit, read-only)

# examples
set_value(address.soc, 100)
print(get_value(address.soc))

set_value(address.accept_values, 1)
print(get_value(address.accept_values))

set_value(address.battery_id, "GREENER_001")
print(get_value(address.battery_id))


context = ModbusServerContext(slaves=store, single=True)
StartTcpServer(context, address=("localhost", 5020))
