import threading

from pymodbus.datastore import ModbusSlaveContext, ModbusSequentialDataBlock, ModbusServerContext
from pymodbus.server.asynchronous import StartTcpServer

from battery.payload_handler import PayloadHandler


class Battery:
    """
    Battery represents the Server/Slave. Basically is a modbus server wrapper.
    """

    """
    Initialize the store and the context
    """
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock.create(),
        co=ModbusSequentialDataBlock.create(),
        hr=ModbusSequentialDataBlock.create(),
        ir=ModbusSequentialDataBlock.create())

    context = ModbusServerContext(slaves=store, single=True)

    def __init__(self, env):
        self.fields = env['fields']
        self.id = env['id']
        self.max_capacity = env['battery_capacity']
        self.payload_handler = PayloadHandler(env['float_store'], self.store)
        self.set_initial_values()
        self.run_server(self.context, env['server_address'])

    def set_initial_values(self):
        """
        setting initial values to fields which have 'init' keyword in their dictionary
        """
        for field_name in self.fields:
            if 'init' in self.fields[field_name]:
                self.set_value(self.fields[field_name], self.fields[field_name]['init'])

    def set_value(self, field, value):
        """
        sets the value to the given field; ALL data which is assigned to  16-bit registers (meaning fx > 2) will
        be encoded by payload_handler
        :param field: a field from the the dictionary (fields[field_name])
        :param value: value to set
        """
        fx = field['reg_type']
        addr = field['address']
        if fx > 2:
            mode = field['encode']
            value = self.payload_handler.encode(value, mode)
            self.store.setValues(fx, addr, value)
        else:
            self.store.setValues(fx, addr, [value])

    def get_value(self, field):
        """
        gets the value of a given field; ALL data from  16-bit registers (meaning fx > 2) will be decoded  by
        payload_handler
        :param field: a field from the the dictionary (fields[field_name])
        :return: value of the given field
        """
        fx = field['reg_type']
        addr = field['address']
        if fx <= 2:
            value = int(self.store.getValues(fx, addr, 1)[0])
        elif fx > 2:
            mode = field['encode']
            value = self.payload_handler.decode(fx, addr, mode)
        return value

    def is_input_connected(self):
        return self.get_value(self.fields['input_connected'])

    def is_converter_started(self):
        return self.get_value(self.fields['converter_started'])

    def run_server(self, context, env):
        """
        starts the servers with filled in context
        runs in separate thread
        """
        t = threading.Thread(target=StartTcpServer, kwargs={'context': context, 'address': tuple(env)}, daemon=True)
        t.start()
        print("SERVER: is running")
