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


<<<<<<< HEAD
def run_server(address, port):
    # initialize the data on full address range
=======
def run_server(address,port,inputtype):

    #initialize the data on full address range
>>>>>>> b8f2c4a6be6f060f4cb6d6a9ccab31aeb2bd722f
    store = ModbusSlaveContext(di=ModbusSequentialDataBlock.create())

    context = ModbusServerContext(slaves=store, single=True)

    # defaut empty strings for identity
    identity = ModbusDeviceIdentification()

<<<<<<< HEAD
    # start server
    StartTcpServer(context, identity=identity, address=(address, port))
=======


    # start server
    StartTcpServer(context, identity=identity, address=(address, port))




>>>>>>> b8f2c4a6be6f060f4cb6d6a9ccab31aeb2bd722f
