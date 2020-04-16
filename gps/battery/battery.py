import threading
import json
from pymodbus.datastore import ModbusSlaveContext, ModbusSequentialDataBlock, ModbusServerContext
from pymodbus.server.sync import ModbusTcpServer
from battery.util import *
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
        self.address = env['address']
        self.id = constants['id']
        self.server = ModbusTcpServer(self.context, address=tuple(env['server_address']))
        self.update_delay = env['update_delay']
        self.max_capacity = constants['battery_capacity']
        self.math_engine = MathEngine(self, self.address)
        self.float_handler = get_float_handler(env['float_store'], self.store)
        self.set_value(self.address['system_on_backup_battery'], constants['system_on_backup_battery'])
        self.set_value(self.address['system_status'], constants['system_status'])
        self.set_value(self.address['system_mode'], constants['system_mode'])
        self.set_value(self.address['accept_values'], constants['accept_values'])
        self.db = None


    def set_value(self, addr, value):
        """
        sets the value to the given address; ALL data which is assigned to  16-bit registers (meaning fx > 2) is
        multiplied by scaling factor and converted to integers first with the method handle_float()
        :param addr: address where first digit stands for reg type
        :param value: value to set
        """
        fx = addr[0]
        addr = addr[1]
        if fx > 2:
            value = self.float_handler.encode_float(value)
            self.store.setValues(fx, addr, value)
        else:
            self.store.setValues(fx, addr, [value])

    def get_value(self, addr):
        """
        gets the value from given address; ALL data from  16-bit registers (meaning fx > 2) is divided by scaling factor
        :param addr: address where first digit stands for reg type
        :return: value from the given address
        """
        fx = addr[0]
        addr = addr[1]
        if fx <= 2:
            value = self.store.getValues(fx, addr, 1)[0]
        elif fx > 2:
            value = self.float_handler.decode_float(fx, addr)
        return value

    def update(self, api, rpi, apo, rpo):
        self.update_powers(api, rpi, apo, rpo)
        self.update_relational()
        #self.print_all_values()
        if self.db: self.write_to_db()

    def update_powers(self, api, rpi, apo, rpo):
        self.set_value(self.address['active_power_in'], api)
        self.set_value(self.address['reactive_power_in'], rpi)
        self.set_value(self.address['active_power_out'], apo)
        self.set_value(self.address['reactive_power_out'], rpo)

    def update_relational(self):
        address = self.address
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

    def run_server(self):
        """
        starts the servers with filled in context
        runs in separate thread
        """
        t = threading.Thread(target=self.server.serve_forever, daemon=True)
        t.start()  # start the thread
        print("SERVER: is running")

    def write_to_db(self):
        address = self.address
        values = []
        for field in address:
            values.append(self.get_value(address[field]))
        self.db.write("battery", values)

    def print_all_values(self):
        """
        makes a dictionary and json.dumps it to output
        this way we can also save the output :)
        """
        address = self.address
        log = {}
        for field in address:
            log[field] = self.get_value(address[field])
            # print("hist_soc", self.power.soc_list[0])
            print(json.dumps(log, indent=4))