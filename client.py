# --------------------------------------------------------------------------- #
# import the various server implementations
# --------------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #
# configure the service logging
# --------------------------------------------------------------------------- #
import logging

from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.server.sync import StartTcpServer

FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)



def run_server(address,port,inputtype):

    #initialize the data on full address range

    store = ModbusSlaveContext(di=ModbusSequentialDataBlock.create())

    context = ModbusServerContext(slaves=store, single=True)

    # defaut empty strings for identity
    identity = ModbusDeviceIdentification()



    # start server
    StartTcpServer(context, identity=identity, address=(address, port))


