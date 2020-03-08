""" Server == slave == Battery """


from pymodbus.server.sync import StartTcpServer
import logging

from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from battery_class import Battery



logging.basicConfig()
log = logging.getLogger()
#log.setLevel(logging.DEBUG)



# initialize  data store
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock.create(),  # discrete input (1 bit, read-only)
    co=ModbusSequentialDataBlock.create(),  # coils (1 bit, read-write)
    hr=ModbusSequentialDataBlock.create(),  # holding registers (16 bit, read-write)
    ir=ModbusSequentialDataBlock.create())  # input registers (16 bit, read-only)

# examples
"""
set_value(battery.soc, 100)
print(battery.getsoc(store))
print(get_value(battery.soc))


set_value(battery.accept_values, 1)
print(get_value(battery.accept_values))

set_value(battery.battery_id, "GREENER_001")
print(get_value(battery.battery_id))


context = ModbusServerContext(slaves=store, single=True)
StartTcpServer(context, address=("localhost", 5020))
"""

battery = Battery(60, 60, 30, 20, 1, 1, 1, store)
battery.print_all_values(store)

context = ModbusServerContext(slaves=store, single=True)
StartTcpServer(context, address=("localhost", 5030))




