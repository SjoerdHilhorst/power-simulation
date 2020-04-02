import threading

from pymodbus.datastore import ModbusSlaveContext, ModbusSequentialDataBlock, ModbusServerContext
from pymodbus.server.sync import ModbusTcpServer

from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from util import *
from math_engine import MathEngine

import json_config

"""
Battery represents the Server/Slave
"""

address = {}


class Battery:
    max_capacity = 330
    """
    Initialize the store and the context
    """
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock.create(),  # discrete input (1 bit, read-only)
        co=ModbusSequentialDataBlock.create(),  # coils (1 bit, read-write)
        hr=ModbusSequentialDataBlock.create(),  # holding registers (16 bit, read-write)
        ir=ModbusSequentialDataBlock.create())  # input registers (16 bit, read-only)

    context = ModbusServerContext(slaves=store, single=True)

    """
    constructor, only constants are initialized here
    """

    def __init__(self, id, addr, config, system_status, system_mode, system_on_backup_battery, accept_values):
        global address
        self.config = config
        address = json_config.get_data(config)
        self.id = id
        """
        Initialize the server with provided address
        """
        self.server = ModbusTcpServer(self.context, address=addr)

        """
        initialize payload builder, this converts floats, negative values to
        IEEE-754 hex format before writing in to the datastore
        """
        self.float_handler = FloatHandler(address['byte_order'], address['word_order'], address['float_mode'],
                                          address['scaling_factor'], self.store)
        self.math_engine = MathEngine(self)
        """
        fill modbus server with initial data 
        """
        self.set_value(address['system_on_backup_battery'], system_on_backup_battery)
        self.set_value(address['system_status'], system_status)
        self.set_value(address['system_mode'], system_mode)
        self.set_value(address['accept_values'], accept_values)
        self.set_value(address['soc'], 0)

        """
        initialize power source and load
        """
        self.power_source = None
        self.power_load = None

    def connect_power_in(self, power_source):
        """
        Literally connect the source and set the initial value of active/reactive power_in
        :param power_source: power_source to connect
        """
        self.power_source = power_source
        self.set_value(address['active_power_in'], self.power_source.get_active_power())
        self.set_value(address['reactive_power_in'], self.power_source.get_reactive_power())
        self.set_value(address['input_connected'], 1)

    def connect_power_out(self, power_load):
        """
        Literally connect the load and set the initial value of active/reactive power_out
        :param power_load: load to connect to
        """
        self.power_load = power_load
        self.set_value(address['active_power_out'], self.power_load.get_active_power())
        self.set_value(address['reactive_power_out'], self.power_load.get_reactive_power())
        self.set_value(address['converter_started'], 1)

    def update_powers(self):
        self.set_value(address['active_power_in'], self.power_source.get_active_power())
        self.set_value(address['reactive_power_in'], self.power_source.get_reactive_power())
        self.set_value(address['active_power_out'], self.power_load.get_active_power())
        self.set_value(address['reactive_power_out'], self.power_load.get_reactive_power())

    def set_value(self, addr, value):
        """
        sets the value to the given address; ALL data which is assigned to  16-bit registers (meaning fx > 2) is
        multiplied by scaling factor and converted to integers first with the method handle_float()
        :param addr: address where first digit stands for reg type
        :param value: value to set
        """
        fx = addr // address['fx_addr_separator']
        addr = addr % address['fx_addr_separator']
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
        fx = addr // address['fx_addr_separator']
        addr = addr % address['fx_addr_separator']
        if fx <= 2:
            value = self.store.getValues(fx, addr, 1)[0]
        elif fx > 2:
            value = self.float_handler.decode_float(fx, addr)
        return value

    def update(self):
        self.update_powers()
        self.set_value(address["active_power_converter"], self.math_engine.get_active_power_converter())
        self.set_value(address["reactive_power_converter"], self.math_engine.get_reactive_power_converter())
        self.set_value(address["voltage_I1_I2_in"], self.math_engine.get_voltage_I1_I2_in())
        self.set_value(address["voltage_I2_I3_in"], self.math_engine.get_voltage_I2_I3_in())
        self.set_value(address["voltage_I3_I1_in"], self.math_engine.get_voltage_I3_I1_in())
        self.set_value(address["current_I1_in"], self.math_engine.get_current_I1_in())
        self.set_value(address["current_I2_in"], self.math_engine.get_current_I2_in())
        self.set_value(address["current_I3_in"], self.math_engine.get_current_I3_in())
        self.set_value(address["frequency_in"], self.math_engine.get_frequency_in())
        self.set_value(address["voltage_I1_I2_out"], self.math_engine.get_voltage_I1_I2_out())
        self.set_value(address["voltage_I2_I3_out"], self.math_engine.get_voltage_I2_I3_out())
        self.set_value(address["voltage_I3_I1_out"], self.math_engine.get_voltage_I3_I1_out())
        self.set_value(address["current_I1_out"], self.math_engine.get_current_I1_out())
        self.set_value(address["current_I2_out"], self.math_engine.get_current_I2_out())
        self.set_value(address["current_I3_out"], self.math_engine.get_current_I3_out())
        self.set_value(address["frequency_out"], self.math_engine.get_frequency_out())
        self.set_value(address["soc"], self.math_engine.get_soc())
        self.print_all_values()

    def run(self):
        """
        starts the servers with filled in context
        runs in separate thread
        """
        t = threading.Thread(target=self.server.serve_forever, daemon=True)
        t.start()  # start the thread
        print("SERVER: is running")
        # update each 2 secs
        interval = 2  # interval with which update happens, in that case every 2 seconds
        loop = LoopingCall(f=self.update)
        loop.start(interval, now=True)
        reactor.run()

    def print_all_values(self):
        print("active power in: ", self.get_value(address['active_power_in']))
        print("reactive power in: ", self.get_value(address['reactive_power_in']))
        print("active power out: ", self.get_value(address['active_power_out']))
        print("reactive power out: ", self.get_value(address['reactive_power_out']))
        print("converter started: ", self.get_value(address['converter_started']))
        print("active power out: ", self.get_value(address['active_power_out']))
        print("input connected: ", self.get_value(address['input_connected']))
        print("system on backup battery: ", self.get_value(address['system_on_backup_battery']))
        print("system status: ", self.get_value(address['system_status']))
        print("system mode: ", self.get_value(address['system_mode']))
        print("accept values: ", self.get_value(address['accept_values']))
        print("active power converter: ", self.get_value(address['active_power_converter']))
        print("reactive power converter: ", self.get_value(address['reactive_power_converter']))
        print("soc: ", self.get_value(address['soc']))
        print("voltage I1 I2 in: ", self.get_value(address['voltage_I1_I2_in']))
        print("voltage I2 I3 in: ", self.get_value(address['voltage_I2_I3_in']))
        print("voltage I3 I1 in: ", self.get_value(address['voltage_I3_I1_in']))
        print("current I1 in: ", self.get_value(address['current_I1_in']))
        print("current I2 in: ", self.get_value(address['current_I2_in']))
        print("current I3 in: ", self.get_value(address['current_I3_in']))
        print("frequency in: ", self.get_value(address['frequency_in']))
        print("voltage I1 I2 out: ", self.get_value(address['voltage_I1_I2_out']))
        print("voltage I2 I3 out: ", self.get_value(address['voltage_I2_I3_out']))
        print("voltage I3 I1 out: ", self.get_value(address['voltage_I3_I1_out']))
        print("current I1 out: ", self.get_value(address['current_I1_out']))
        print("current I2 out: ", self.get_value(address['current_I2_out']))
        print("current I3 out: ", self.get_value(address['current_I3_out']))
        print("frequency out: ", self.get_value(address['frequency_out']))
        print('----------------------------------')
