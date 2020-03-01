""" Server == slave == Battery """
from pymodbus.server.sync import StartTcpServer
import logging

from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

# configure the service logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# initialize  data store
# here create() makes datastore with the full address space initialized to 0x00
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock.create(),  # discrete input (1 bit, read-only)
    co=ModbusSequentialDataBlock.create(),  # coils (1 bit, read-write)
    hr=ModbusSequentialDataBlock.create(),  # holding registers (16 bit, read-write)
    ir=ModbusSequentialDataBlock.create())  # input registers (16 bit, read-only)

#fx=1->co; 2->di;3->hr;4->ir
#store.setValues(4,0,[1]*100)

# single = only one slave
context = ModbusServerContext(slaves=store, single=True)
StartTcpServer(context, address=("localhost", 5020))
