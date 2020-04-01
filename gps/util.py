import numpy as np
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder

import json_config

address = {}


class FloatHandler:
    def __init__(self, byte_order, word_order, float_mode, scaling_factor, store):
        self.builder = BinaryPayloadBuilder(byteorder=byte_order, wordorder=word_order)
        self.byte_order = byte_order
        self.word_order = word_order
        self.float_mode = float_mode
        self.scaling_factor = scaling_factor
        self.battery_store = store

    def encode_float(self, value):
        """
        encodes float according to the way it is stored in registry
        SCALE stands for multiplying/dividing by scaling factor method, I.E. 32bit int
        COMB stands for storing the float in two registers, I.E. 32bit float
        :param value: float which should be handled
        :return: float rounded to integer
        """
        self.builder.reset()
        if self.float_mode == "SCALE":
            self.builder.add_32bit_int(round(value * self.scaling_factor))
        elif self.float_mode == "COMB":
            self.builder.add_32bit_float(value)
        return self.builder.to_registers()

    def decode_float(self, fx, addr):
        """
        decodes float value, the way specified in address
        """
        encoded_value = self.battery_store.getValues(fx, addr, 2)
        decoder = BinaryPayloadDecoder.fromRegisters(encoded_value, byteorder=self.byte_order,
                                                     wordorder=self.word_order)
        if self.float_mode == "SCALE":
            value = decoder.decode_32bit_int() / self.scaling_factor
        elif self.float_mode == "COMB":
            value = decoder.decode_32bit_float()
        return value


class MathEngine:

    def __init__(self, battery):
        self.battery = battery
        global address
        address = json_config.get_data(battery.config)

    def random_gaussian_value(self, mu, sigma):
        return np.random.normal(mu, sigma)

    def get_power_factor_in(self):
        """
        :return: active_power_in / sqrt(active_power_in^2 + reactive_power_in^2)
        """
        ap = self.battery.get_value(address['active_power_in'])
        rp = self.battery.get_value(address['reactive_power_in'])
        return ap / np.math.sqrt(ap * ap + rp * rp)

    def get_power_factor_out(self):
        """
        :return: active_power_out / sqrt(active_power_out^2 + reactive_power_out^2)
        """
        ap = self.battery.get_value(address['active_power_out'])
        rp = self.battery.get_value(address['reactive_power_out'])
        return ap / np.math.sqrt(ap * ap + rp * rp)

    def get_active_power_converter(self):
        """
        :return: active_power_in - active_power_out
        """
        apc = self.battery.get_value(address['active_power_in']) - self.battery.get_value(address['active_power_out'])
        return apc

    def get_reactive_power_converter(self):
        """
        :return: reactive_power_in - reactive_power_out
        """
        rpc = self.battery.get_value(address['reactive_power_in']) - self.battery.get_value(
            address['reactive_power_out'])
        return rpc

    def get_soc(self):
        """
        :return: previous SoC + [(active_power_converter) /
                (Some configurable max battery capacity, say 330 kWh)] * 3600.
        """
        prev_soc = self.battery.get_value(address['soc'])
        apc = self.battery.get_value(address['active_power_converter'])

        # multiply by 1000 to convert from kWh
        new_soc = prev_soc + (apc / (self.battery.max_capacity * 1000)) * 3600
        return new_soc

    def get_voltage_I1_I2_in(self):
        """
        :return: Gaussian distribution centered around 400, deviation 3
        """
        value = self.random_gaussian_value(400, 3)
        return value

    def get_voltage_I2_I3_in(self):
        """
        :return: Gaussian distribution centered around 400, deviation 3
        """
        value = self.random_gaussian_value(400, 3)
        return value

    def get_voltage_I3_I1_in(self):
        """
        :return: Gaussian distribution centered around 400, deviation 3
        """
        value = self.random_gaussian_value(400, 3)
        return value

    def get_current_I1_in(self):
        """
        :return: active_power_in / (sqrt(3) * voltage_l1_l2_in * power_factor_in)
        """
        ap = self.battery.get_value(address['active_power_in'])
        voltage = self.battery.get_value(address['voltage_I1_I2_in'])
        pf = self.get_power_factor_in()
        current = ap / (np.math.sqrt(3) * voltage * pf) * 1000  # from kW to W
        return current

    def get_current_I2_in(self):
        """
        :return: active_power_in / (sqrt(3) * voltage_l2_l3_in * power_factor_in)
        """
        ap = self.battery.get_value(address['active_power_in'])
        voltage = self.battery.get_value(address['voltage_I2_I3_in'])
        pf = self.get_power_factor_in()
        current = ap / (np.math.sqrt(3) * voltage * pf) * 1000  # from kW to W
        return current

    def get_current_I3_in(self):
        """
        :return: active_power_in / (sqrt(3) * voltage_l3_l1_in * power_factor_in)
        """
        ap = self.battery.get_value(address['active_power_in'])
        voltage = self.battery.get_value(address['voltage_I3_I1_in'])
        pf = self.get_power_factor_in()
        current = ap / (np.math.sqrt(3) * voltage * pf) * 1000  # from kW to W
        return current

    def get_frequency_in(self):
        """
        :return: Gaussian distribution centered around 50, deviation 0.01
        """
        value = self.random_gaussian_value(50, 0.01)
        return value

    def get_voltage_I1_I2_out(self):
        """
        :return: Gaussian distribution centered around 400, deviation 3
        """
        value = self.random_gaussian_value(400, 3)
        return value

    def get_voltage_I2_I3_out(self):
        """
        :return: Gaussian distribution centered around 400, deviation 3
        """
        value = self.random_gaussian_value(400, 3)
        return value

    def get_voltage_I3_I1_out(self):
        """
        :return: Gaussian distribution centered around 400, deviation 3
        """
        value = self.random_gaussian_value(400, 3)
        return value

    def get_current_I1_out(self):
        """
        :return: active_power_out / (sqrt(3) * voltage_l1_l2_out * power_factor_out)
        """
        ap = self.battery.get_value(address['active_power_out'])
        voltage = self.battery.get_value(address['voltage_I1_I2_out'])
        pf = self.get_power_factor_out()
        current = ap / (np.math.sqrt(3) * voltage * pf) * 1000  # from kW to W
        return current

    def get_current_I2_out(self):
        """
        :return: active_power_out / (sqrt(3) * voltage_l2_l3_out * power_factor_out)
        """
        ap = self.battery.get_value(address['active_power_out'])
        voltage = self.battery.get_value(address['voltage_I2_I3_out'])
        pf = self.get_power_factor_out()
        current = ap / (np.math.sqrt(3) * voltage * pf) * 1000  # from kW to W
        return current

    def get_current_I3_out(self):
        """
        :return: active_power_out / (sqrt(3) * voltage_l3_l1_out * power_factor_out)
        """
        ap = self.battery.get_value(address['active_power_out'])
        voltage = self.battery.get_value(address['voltage_I3_I1_out'])
        pf = self.get_power_factor_out()
        current = ap / (np.math.sqrt(3) * voltage * pf) * 1000  # from kW to W
        return current

    def get_frequency_out(self):
        """
        :return: Gaussian distribution centered around 50, deviation 0.01
        """
        value = self.random_gaussian_value(50, 0.01)
        return value
