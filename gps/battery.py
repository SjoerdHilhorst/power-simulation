import numpy as np
import math

from pymodbus.datastore import ModbusSlaveContext, ModbusSequentialDataBlock, ModbusServerContext
from pymodbus.server.sync import StartTcpServer

import def_config as address

"""Battery represents the Server/Slave"""


def random_gaussian_value(mu, sigma):
    """
    :param mu:
    :param sigma:
    :return: return random normal distribution value
    """
    return np.random.normal(mu, sigma)


class Battery:
    max_capacity = 330

    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock.create(),  # discrete input (1 bit, read-only)
        co=ModbusSequentialDataBlock.create(),  # coils (1 bit, read-write)
        hr=ModbusSequentialDataBlock.create(),  # holding registers (16 bit, read-write)
        ir=ModbusSequentialDataBlock.create())  # input registers (16 bit, read-only)

    def __init__(self,
                 active_power_in,
                 reactive_power_in,
                 active_power_out,
                 reactive_power_out,
                 converter_started,
                 input_connected,
                 system_on_backup_battery,
                 system_status=1,
                 system_mode=5,
                 accept_values=1
                 ):
        """
        fill modbus server with initial data
        """

        self.set_value(address.active_power_in, active_power_in)
        self.set_value(address.reactive_power_in, reactive_power_in)
        self.set_value(address.active_power_out, active_power_out)
        self.set_value(address.reactive_power_out, reactive_power_out)
        self.set_value(address.converter_started, converter_started)
        self.set_value(address.active_power_out, active_power_out)
        self.set_value(address.input_connected, input_connected)
        self.set_value(address.system_on_backup_battery, system_on_backup_battery)
        self.set_value(address.system_status, system_status)
        self.set_value(address.system_mode, system_mode)
        self.set_value(address.accept_values, accept_values)

        # fill relational fields
        self.update()

    def set_value(self, addr, value):
        fx = addr // 100
        address = addr % 100
        self.store.setValues(fx, address, [value])

    def get_value(self, addr):
        fx = addr // 100
        address = addr % 100
        return self.store.getValues(fx, address, 1)[0]

    def update(self):
        """
        update all relational fields

        """
        self.set_active_power_converter()
        self.set_reactive_power_converter()
        self.set_soc()
        self.set_voltage_l1_l2_in()
        self.set_voltage_l2_l3_in()
        self.set_voltage_l3_l1_in()
        self.set_current_l1_in()
        self.set_current_l2_in()
        self.set_current_l3_in()
        self.set_frequency_in()
        self.set_voltage_l1_l2_out()
        self.set_voltage_l2_l3_out()
        self.set_voltage_l3_l1_out()
        self.set_current_l1_out()
        self.set_current_l2_out()
        self.set_current_l3_out()
        self.set_frequency_out()

    # helper functions

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

    def set_voltage_l1_l2_in(self):
        """
        :return: Gaussian distribution centered around 400, deviation 3
        """

        value = random_gaussian_value(400, 3)
        self.set_value(address.voltage_l1_l2_in, value)

    def set_voltage_l2_l3_in(self):
        """
        :return: Gaussian distribution centered around 400, deviation 3
        """

        value = random_gaussian_value(400, 3)
        self.set_value(address.voltage_l2_l3_in, value)

    def set_voltage_l3_l1_in(self):
        """
        :return: Gaussian distribution centered around 400, deviation 3
        """
        value = random_gaussian_value(400, 3)
        self.set_value(address.voltage_l3_l1_in, value)

    def set_current_l1_in(self):
        """

        :return: active_power_in / (sqrt(3) * voltage_l1_l2_in * power_factor_in)
        """

        ap = self.get_value(address.active_power_in)
        voltage = self.get_value(address.voltage_l1_l2_in)
        pf = self.get_power_factor_in()
        current = ap / (math.sqrt(3) * voltage * pf)
        self.set_value(address.current_l1_in, current)

    def set_current_l2_in(self):
        """
        :return: active_power_in / (sqrt(3) * voltage_l2_l3_in * power_factor_in)
        """
        ap = self.get_value(address.active_power_in)
        voltage = self.get_value(address.voltage_l2_l3_in)
        pf = self.get_power_factor_in()
        current = ap / (math.sqrt(3) * voltage * pf)
        self.set_value(address.current_l2_in, current)

    def set_current_l3_in(self):
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
        value = random_gaussian_value(50, 0.01)
        self.set_value(address.frequency_in, value)

    def set_voltage_l1_l2_out(self):
        """
        :return: Gaussian distribution centered around 400, deviation 3
        """
        value = random_gaussian_value(400, 3)
        self.set_value(address.voltage_l1_l2_out, value)

    def set_voltage_l2_l3_out(self):
        """
        :return: Gaussian distribution centered around 400, deviation 3
        """
        value = random_gaussian_value(400, 3)
        self.set_value(address.voltage_l2_l3_out, value)

    def set_voltage_l3_l1_out(self):
        """
        :return: Gaussian distribution centered around 400, deviation 3
        """
        value = random_gaussian_value(400, 3)
        self.set_value(address.voltage_l3_l1_out, value)

    def set_current_l1_out(self):
        """
        :return: active_power_out / (sqrt(3) * voltage_l1_l2_out * power_factor_out)
        """
        ap = self.get_value(address.active_power_out)
        voltage = self.get_value(address.voltage_l1_l2_out)
        pf = self.get_power_factor_out()
        current = ap / (math.sqrt(3) * voltage * pf)
        self.set_value(address.current_l1_out, current)

    def set_current_l2_out(self):
        """
        :return: active_power_out / (sqrt(3) * voltage_l2_l3_out * power_factor_out)
        """
        ap = self.get_value(address.active_power_out)
        voltage = self.get_value(address.voltage_l2_l3_out)
        pf = self.get_power_factor_out()
        current = ap / (math.sqrt(3) * voltage * pf)
        self.set_value(address.current_l2_out, current)

    def set_current_l3_out(self):
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
        value = random_gaussian_value(50, 0.01)
        self.set_value(address.frequency_out, value)

    def run(self):
        print("START")
        context = ModbusServerContext(slaves=self.store, single=True)
        StartTcpServer(context, address=("localhost", 5030))
