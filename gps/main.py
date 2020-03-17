from battery import Battery
from pymodbus.datastore import ModbusSlaveContext, ModbusSequentialDataBlock, ModbusServerContext
import math

battery = Battery('DEFAULT', 40, 60, 30, 20, 1, 1, 1)
battery.print_all_values()

battery.set_value(312, 123.456)
print(battery.get_value(312))
battery.run()


# initialize the store
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock.create(),  # discrete input (1 bit, read-only)
    co=ModbusSequentialDataBlock.create(),  # coils (1 bit, read-write)
    hr=ModbusSequentialDataBlock.create(),  # holding registers (16 bit, read-write)
    ir=ModbusSequentialDataBlock.create())  # input registers (16 bit, read-only)

val = 123.456
val = math.modf(val)
list = []
list.append(round(val[0]*100))
list.append(round(val[1]))
print(list)
store.setValues(3, 0, [0x100])
x = store.getValues(3, 0, 3)


print(x)