import threading
from pymodbus.datastore import ModbusSlaveContext, ModbusSequentialDataBlock, ModbusServerContext
from pymodbus.server.asynchronous import StartTcpServer
from battery.util import FloatHandler
from battery.math_engine import MathEngine

"""
Battery represents the Server/Slave
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
        self.math_engine = MathEngine(self, self.field)
        self.float_handler = FloatHandler(env['float_store'], self.store)
        self.set_value(self.field['system_on_backup_battery'], constants['system_on_backup_battery'])
        self.set_value(self.field['system_status'], constants['system_status'])
        self.set_value(self.field['system_mode'], constants['system_mode'])
        self.set_value(self.field['accept_values'], constants['accept_values'])
        self.set_value(self.field['converter_started'], constants['converter_started'])
        self.set_value(self.field['input_connected'], constants['input_connected'])
        self.db = None
        self.graph = None

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

    def update(self, api, rpi, apo, rpo):
        self.update_powers(api, rpi, apo, rpo)
        self.update_relational()
        if self.db: self.write_to_db()
        if self.graph: self.write_to_graph()

    def update_powers(self, api, rpi, apo, rpo):
        self.set_value(self.field['active_power_in'], self.math_engine.get_active_power_in(api))
        self.set_value(self.field['reactive_power_in'], self.math_engine.get_reactive_power_in(rpi))
        self.set_value(self.field['active_power_out'], self.math_engine.get_active_power_out(apo))
        self.set_value(self.field['reactive_power_out'], self.math_engine.get_reactive_power_out(rpo))

    def update_relational(self):
        address = self.field
        self.set_value(address["active_power_converter"], self.math_engine.get_active_power_converter())
        self.set_value(address["reactive_power_converter"], self.math_engine.get_reactive_power_converter())
        self.set_value(address["voltage_l1_l2_in"], self.math_engine.get_voltage_I1_I2_in())
        self.set_value(address["voltage_l2_l3_in"], self.math_engine.get_voltage_I2_I3_in())
        self.set_value(address["voltage_l3_l1_in"], self.math_engine.get_voltage_I3_I1_in())
        self.set_value(address["current_l1_in"], self.math_engine.get_current_I1_in())
        self.set_value(address["current_l2_in"], self.math_engine.get_current_I2_in())
        self.set_value(address["current_l3_in"], self.math_engine.get_current_I3_in())
        self.set_value(address["frequency_in"], self.math_engine.get_frequency_in())
        self.set_value(address["voltage_l1_l2_out"], self.math_engine.get_voltage_I1_I2_out())
        self.set_value(address["voltage_l2_l3_out"], self.math_engine.get_voltage_I2_I3_out())
        self.set_value(address["voltage_l3_l1_out"], self.math_engine.get_voltage_I3_I1_out())
        self.set_value(address["current_l1_out"], self.math_engine.get_current_I1_out())
        self.set_value(address["current_l2_out"], self.math_engine.get_current_I2_out())
        self.set_value(address["current_l3_out"], self.math_engine.get_current_I3_out())
        self.set_value(address["frequency_out"], self.math_engine.get_frequency_out())
        self.set_value(address["soc"], self.math_engine.get_soc())

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
        t.start()  # start the thread
        print("SERVER: is running")

    def write_to_db(self):
        address = self.field
        values = []
        for field in address:
            values.append(self.get_value(address[field]))
        self.db.write("battery", values)

    def print_all_values(self):
        """
        makes a dictionary and json.dumps it to output
        this way we can also save the output :)
        """
        address = self.field
        log = {}
        for field in address:
            log[field] = self.get_value(address[field])

    def write_to_graph(self):
        self.graph.mutex.lock()
        for field in self.graph.graphs:
            value = self.get_value(self.field[field])
            self.graph.data[field].append(value)
        self.graph.data['t'] += 1
        self.graph.mutex.unlock()
