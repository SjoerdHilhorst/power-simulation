""" Server == slave == Battery """

from pymodbus.server.sync import StartTcpServer
import logging

from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
import register_variables as address


logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# map for registers
reg_map = {"co": 1, "di": 2, "hr": 3, "ir": 4}


def set_value(fx, addr, value):
    store.setValues(reg_map[fx], addr, value)


# initialize  data store
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock.create(),  # discrete input (1 bit, read-only)
    co=ModbusSequentialDataBlock.create(),  # coils (1 bit, read-write)
    hr=ModbusSequentialDataBlock.create(),  # holding registers (16 bit, read-write)
    ir=ModbusSequentialDataBlock.create())  # input registers (16 bit, read-only)

# example: set state of charge to 100
set_value("hr", address.soc, [100])

context = ModbusServerContext(slaves=store, single=True)
StartTcpServer(context, address=("localhost", 5020))
