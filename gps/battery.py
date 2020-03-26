import threading

import numpy as np
import math

from pymodbus.datastore import ModbusSlaveContext, ModbusSequentialDataBlock, ModbusServerContext
from pymodbus.server.sync import ModbusTcpServer

from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from handlers import FloatHandler

import config as address

"""
Battery represents the Server/Slave
"""


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

    def __init__(self, id, addr, system_status, system_mode, system_on_backup_battery, accept_values):
        self.id = id

        """
        Initialize the server with provided address
        """
        self.server = ModbusTcpServer(self.context, address=addr)

        """
        initialize payload builder, this converts floats, negative values to
        IEEE-754 hex format before writing in to the datastore
        """
        self.float_handler = FloatHandler(address.byte_order, address.word_order, address.float_mode,
                                          address.scaling_factor, self.store)
        """
        fill modbus server with initial data 
        """
        self.set_value(address.system_on_backup_battery, system_on_backup_battery)
        self.set_value(address.system_status, system_status)
        self.set_value(address.system_mode, system_mode)
        self.set_value(address.accept_values, accept_values)

    def connect_power_in(self, active_power_in, reactive_power_in, input_connected=1):
        self.set_value(address.active_power_in, active_power_in)
        self.set_value(address.reactive_power_in, reactive_power_in)
        self.set_value(address.input_connected, input_connected)

    def connect_power_out(self, active_power_out, reactive_power_out, converter_started=1):
        self.set_value(address.active_power_out, active_power_out)
        self.set_value(address.reactive_power_out, reactive_power_out)
        self.set_value(address.converter_started, converter_started)

    def set_value(self, addr, value):
        """
        sets the value to the given address; ALL data which is assigned to  16-bit registers (meaning fx > 2) is
        multiplied by scaling factor and converted to integers first with the method handle_float()
        :param addr: address where first digit stands for reg type
        :param value: value to set
        """
        fx = addr // address.fx_addr_separator
        addr = addr % address.fx_addr_separator
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
        fx = addr // address.fx_addr_separator
        addr = addr % address.fx_addr_separator
        if fx <= 2:
            value = self.store.getValues(fx, addr, 1)[0]
        elif fx > 2:
            value = self.float_handler.decode_float(fx, addr)
        return value

    def update(self):
        self.set_active_power_converter()
        self.set_reactive_power_converter()
        self.set_voltage_I1_I2_in()
        self.set_voltage_I2_I3_in()
        self.set_voltage_I3_I1_in()
        self.set_current_I1_in()
        self.set_current_I2_in()
        self.set_current_I3_in()
        self.set_frequency_in()
        self.set_voltage_I1_I2_out()
        self.set_voltage_I2_I3_out()
        self.set_voltage_I3_I1_out()
        self.set_current_I1_out()
        self.set_current_I2_out()
        self.set_current_I3_out()
        self.set_frequency_out()
        self.set_soc()

    def print_all_values(self):
        print("active power in: ", self.get_value(address.active_power_in))
        print("reactive power in: ", self.get_value(address.reactive_power_in))
        print("active power out: ", self.get_value(address.active_power_out))
        print("reactive power out: ", self.get_value(address.reactive_power_out))
        print("converter started: ", self.get_value(address.converter_started))
        print("active power out: ", self.get_value(address.active_power_out))
        print("input connected: ", self.get_value(address.input_connected))
        print("system on backup battery: ", self.get_value(address.system_on_backup_battery))
        print("system status: ", self.get_value(address.system_status))
        print("system mode: ", self.get_value(address.system_mode))
        print("accept values: ", self.get_value(address.accept_values))
        print("active power converter: ", self.get_value(address.active_power_converter))
        print("reactive power converter: ", self.get_value(address.reactive_power_converter))
        print("soc: ", self.get_value(address.soc))
        print("voltage I1 I2 in: ", self.get_value(address.voltage_l1_l2_in))
        print("voltage I2 I3 in: ", self.get_value(address.voltage_l2_l3_in))
        print("voltage I3 I1 in: ", self.get_value(address.voltage_l3_l1_in))
        print("current I1 in: ", self.get_value(address.current_l1_in))
        print("current I2 in: ", self.get_value(address.current_l2_in))
        print("current I3 in: ", self.get_value(address.current_l3_in))
        print("frequency in: ", self.get_value(address.frequency_in))
        print("voltage I1 I2 out: ", self.get_value(address.voltage_l1_l2_out))
        print("voltage I2 I3 out: ", self.get_value(address.voltage_l2_l3_out))
        print("voltage I3 I1 out: ", self.get_value(address.voltage_l3_l1_out))
        print("current I1 out: ", self.get_value(address.current_l1_out))
        print("current I2 out: ", self.get_value(address.current_l2_out))
        print("current I3 out: ", self.get_value(address.current_l3_out))
        print("frequency out: ", self.get_value(address.frequency_out))

    def random_gaussian_value(self, mu, sigma):
        return np.random.normal(mu, sigma)

    def get_power_factor_in(self):
        """
        :return: active_power_in / sqrt(active_power_in^2 + reactive_power_in^2)
        """
        ap = self.get_value(address.active_power_in)
        rp = self.get_value(address.reactive_power_in)
        return ap / math.sqrt(ap * ap + rp * rp)

    def get_power_factor_out(self):
        """
        :return: active_power_out / sqrt(active_power_out^2 + reactive_power_out^2)
        """
        ap = self.get_value(address.active_power_out)
        rp = self.get_value(address.reactive_power_out)
        return ap / math.sqrt(ap * ap + rp * rp)

    def set_active_power_converter(self):
        """
        :return: active_power_in - active_power_out
        """
        apc = self.get_value(address.active_power_in) - self.get_value(address.active_power_out)
        self.set_value(address.active_power_converter, apc)

    def set_reactive_power_converter(self):
        """
        :return: reactive_power_in - reactive_power_out
        """
        rpc = self.get_value(address.reactive_power_in) - self.get_value(address.reactive_power_out)
        self.set_value(address.reactive_power_converter, rpc)

    def set_soc(self):
        """
        :return: previous SoC + [(active_power_converter) /
                (Some configurable max battery capacity, say 330 kWh)] * 3600.
        """
        prev_soc = self.get_value(address.soc)
        apc = self.get_value(address.active_power_converter)
        new_soc = prev_soc + (apc / self.max_capacity) * 3600
        self.set_value(address.soc, new_soc)

    def set_voltage_I1_I2_in(self):
        """
        :return: Gaussian distribution centered around 400, deviation 3
        """
        value = self.random_gaussian_value(400, 3)
        self.set_value(address.voltage_l1_l2_in, value)

    def set_voltage_I2_I3_in(self):
        """
        :return: Gaussian distribution centered around 400, deviation 3
        """
        value = self.random_gaussian_value(400, 3)
        self.set_value(address.voltage_l2_l3_in, value)

    def set_voltage_I3_I1_in(self):
        """
        :return: Gaussian distribution centered around 400, deviation 3
        """
        value = self.random_gaussian_value(400, 3)
        self.set_value(address.voltage_l3_l1_in, value)

    def set_current_I1_in(self):
        """
        :return: active_power_in / (sqrt(3) * voltage_l1_l2_in * power_factor_in)
        """
        ap = self.get_value(address.active_power_in)
        voltage = self.get_value(address.voltage_l1_l2_in)
        pf = self.get_power_factor_in()
        current = ap / (math.sqrt(3) * voltage * pf)
        self.set_value(address.current_l1_in, current)

    def set_current_I2_in(self):
        """
        :return: active_power_in / (sqrt(3) * voltage_l2_l3_in * power_factor_in)
        """
        ap = self.get_value(address.active_power_in)
        voltage = self.get_value(address.voltage_l2_l3_in)
        pf = self.get_power_factor_in()
        current = ap / (math.sqrt(3) * voltage * pf)
        self.set_value(address.current_l2_in, current)

    def set_current_I3_in(self):
        """
        :return: active_power_in / (sqrt(3) * voltage_l3_l1_in * power_factor_in)
        """
        ap = self.get_value(address.active_power_in)
        voltage = self.get_value(address.voltage_l3_l1_in)
        pf = self.get_power_factor_in()
        current = ap / (math.sqrt(3) * voltage * pf)
        self.set_value(address.current_l3_in, current)

    def set_frequency_in(self):
        """
        :return: Gaussian distribution centered around 50, deviation 0.01
        """
        value = self.random_gaussian_value(50, 0.01)
        self.set_value(address.frequency_in, value)

    def set_voltage_I1_I2_out(self):
        """
        :return: Gaussian distribution centered around 400, deviation 3
        """
        value = self.random_gaussian_value(400, 3)
        self.set_value(address.voltage_l1_l2_out, value)

    def set_voltage_I2_I3_out(self):
        """
        :return: Gaussian distribution centered around 400, deviation 3
        """
        value = self.random_gaussian_value(400, 3)
        self.set_value(address.voltage_l2_l3_out, value)

    def set_voltage_I3_I1_out(self):
        """
        :return: Gaussian distribution centered around 400, deviation 3
        """
        value = self.random_gaussian_value(400, 3)
        self.set_value(address.voltage_l3_l1_out, value)

    def set_current_I1_out(self):
        """
        :return: active_power_out / (sqrt(3) * voltage_l1_l2_out * power_factor_out)
        """
        ap = self.get_value(address.active_power_out)
        voltage = self.get_value(address.voltage_l1_l2_out)
        pf = self.get_power_factor_out()
        current = ap / (math.sqrt(3) * voltage * pf)
        self.set_value(address.current_l1_out, current)

    def set_current_I2_out(self):
        """
        :return: active_power_out / (sqrt(3) * voltage_l2_l3_out * power_factor_out)
        """
        ap = self.get_value(address.active_power_out)
        voltage = self.get_value(address.voltage_l2_l3_out)
        pf = self.get_power_factor_out()
        current = ap / (math.sqrt(3) * voltage * pf)
        self.set_value(address.current_l2_out, current)

    def set_current_I3_out(self):
        """
        :return: active_power_out / (sqrt(3) * voltage_l3_l1_out * power_factor_out)
        """
        ap = self.get_value(address.active_power_out)
        voltage = self.get_value(address.voltage_l3_l1_out)
        pf = self.get_power_factor_out()
        current = ap / (math.sqrt(3) * voltage * pf)
        self.set_value(address.current_l3_out, current)

    def set_frequency_out(self):
        """
        :return: Gaussian distribution centered around 50, deviation 0.01
        """
        value = self.random_gaussian_value(50, 0.01)
        self.set_value(address.frequency_out, value)

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
