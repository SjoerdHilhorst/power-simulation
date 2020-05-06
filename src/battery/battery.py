import threading

from pymodbus.datastore import ModbusSlaveContext, ModbusSequentialDataBlock, ModbusServerContext
from pymodbus.server.asynchronous import StartTcpServer

from battery.util import FloatHandler

"""
Battery represents the Server/Slave. Basically is a modbus server wrapper
"""


class Battery:
    """
    Initialize the store and the context
    """
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock.create(),  # discrete input (1 bit, read-only)
        co=ModbusSequentialDataBlock.create(),  # coils (1 bit, read-write)
        hr=ModbusSequentialDataBlock.create(),  # holding registers (16 bit, read-write)
        ir=ModbusSequentialDataBlock.create())  # input registers (16 bit, read-only)

    context = ModbusServerContext(slaves=store, single=True)

    def __init__(self, env):
        constants = env['battery_constants']
        self.field = env['fields']
        self.id = constants['id']
        self.run_server(self.context, env['server_address'])
        self.update_delay = env['update_delay']
        self.max_capacity = constants['battery_capacity']

        self.float_handler = FloatHandler(env['float_store'], self.store)
        self.set_value(self.field['system_on_backup_battery'], constants['system_on_backup_battery'])
        self.set_value(self.field['system_status'], constants['system_status'])
        self.set_value(self.field['system_mode'], constants['system_mode'])
        self.set_value(self.field['accept_values'], constants['accept_values'])
        self.set_value(self.field['converter_started'], constants['converter_started'])
        self.set_value(self.field['input_connected'], constants['input_connected'])

        self.set_value(self.field['soc'], env['soc'])

    def set_value(self, field, value):
        """
        sets the value to the given address; ALL data which is assigned to  16-bit registers (meaning fx > 2) is
        multiplied by scaling factor and converted to integers first with the method handle_float()
        :param field:
        :param value: value to set
        """
        fx = field[0]
        addr = field[1]
        if fx > 2:
            mode = field[2]
            value = self.float_handler.encode_float(value, mode)

            self.store.setValues(fx, addr, value)
        else:
            self.store.setValues(fx, addr, [value])

    def get_value(self, field):
        """
        gets the value from given address; ALL data from  16-bit registers (meaning fx > 2) is divided by scaling factor
        :param field:
        :return: value from the given address
        """
        fx = field[0]
        addr = field[1]
        if fx <= 2:
            value = self.store.getValues(fx, addr, 1)[0]
        elif fx > 2:
            mode = field[2]
            value = self.float_handler.decode_float(fx, addr, mode)
        return value

    def is_input_connected(self):
        return self.get_value(self.field['input_connected'])

    def is_converter_started(self):
        return self.get_value(self.field['converter_started'])

    def run_server(self, context, env):
        """
        starts the servers with filled in context
        runs in separate thread
        """
        t = threading.Thread(target=StartTcpServer, kwargs={'context': context, 'address': tuple(env)}, daemon=True)
        t.start()
        print("SERVER: is running")