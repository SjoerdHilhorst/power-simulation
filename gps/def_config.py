import numpy as np
import math
""" Default configuration of the addresses

The addresses are in following format: first digit represents the type of registry
(coils = 1, discrete input = 2, holding reg = 3, input reg = 4);
remaining two digits are the actual address """


class Battery:
    # Battery Registers:

    battery_id = 310  # str     config
    soc = 311  # float   dep
    active_power_in = 312  # float   in
    reactive_power_in = 313  # float   in
    current_l1_in = 314  # float   dep
    current_l2_in = 315  # float   dep
    current_l3_in = 316  # float   dep
    voltage_l1_l2_in = 317  # float   semi
    voltage_l2_l3_in = 318  # float   semi
    voltage_l3_l1_in = 319  # float   semi
    frequency_in = 320  # float   semi
    active_power_out = 321  # float   in
    reactive_power_out = 322  # float   in
    current_l1_out = 323  # float   dep
    current_l2_out = 324  # float   dep
    current_l3_out = 325  # float   dep
    voltage_l1_l2_out = 326  # float   semi
    voltage_l2_l3_out = 327  # float   semi
    voltage_l3_l1_out = 328  # float   semi
    frequency_out = 329  # float   semi
    active_power_converter = 330  # float   dep
    reactive_power_converter = 331  # float   dep

    # Battery State

    time = 332
    system_status = 333  # int    const
    system_mode = 334  # int    const
    accept_values = 110  # bool   const
    converter_started = 111  # bool   in
    input_connected = 112  # bool   in
    system_on_backup_battery = 113  # bool   in

    # Battery values
    max_capacity = 330

    # register mapping
    map_type = 100
    map_address = 100

    # helper functions

    def get_register_type_address(self, register):
        """
        :param register: the input register
        :return: the type of register and the address of the register
        """
        return register // self.map_type, register % self.map_address

    def random_gaussian_value(self, mu, sigma):
        """
        :param mu:
        :param sigma:
        :return: return random normal distribution value
        """
        return np.random.normal(mu, sigma)

    def get_power_factor_in(self, store):
        """
        :param store:
        :return: active_power_in / sqrt(active_power_in^2 + reactive_power_in^2)
        """
        ap = self.get_value(self.active_power_in, store)
        rp = self.get_value(self.reactive_power_in, store)
        return ap / math.sqrt(ap*ap + rp*rp)

    def get_power_factor_out(self, store):
        """
        :param store:
        :return: active_power_out / sqrt(active_power_out^2 + reactive_power_out^2)
        """
        ap = self.get_value(self.active_power_out, store)
        rp = self.get_value(self.reactive_power_out, store)
        return ap / math.sqrt(ap*ap + rp*rp)

    # fields getters and setters

    def set_value(self, value, store, address):
        """

        :param value: the value to be stored
        :param store:
        :param address: the address to store the value in
        :return:
        """
        register_type, register_address = self.get_register_type_address(address)
        store.setValues(register_type, register_address, [value])

    def get_value(self, register, store):
        register_type, register_address = self.get_register_type_address(register)
        return store.getValues(register_type, register_address, 1)[0]

    # dependent fields


    def set_active_power_converter(self, store):
        """
        :param store:
        :return: active_power_in - active_power_out
        """

        register_type, register_address = self.get_register_type_address(self.active_power_converter)
        apc = self.get_value(self.active_power_in, store) - self.get_value(self.active_power_out, store)
        store.setValues(register_type, register_address, apc)

    def set_reactive_power_converter(self, store):
        """
        :param store:
        :return: reactive_power_in - reactive_power_out
        """

        register_type, register_address = self.get_register_type_address(self.reactive_power_converter)
        rpc = self.get_value(self.reactive_power_in, store) - self.get_value(self.reactive_power_out, store)
        store.setValues(register_type, register_address, rpc)

    # previous SoC + [(active_power_converter) / (Some configurable max battery capacity, say 330 kWh)] * 3600.
    def set_soc(self, store):
        """
        :param store:
        :return: previous SoC + [(active_power_converter) /
                (Some configurable max battery capacity, say 330 kWh)] * 3600.
        """
        register_type, register_address = self.get_register_type_address(self.soc)
        prev_soc = self.get_value(self.soc, store)
        apc = self.get_value(self.active_power_converter)
        new_soc = prev_soc + (apc / self.max_capacity) * 3600
        store.setValues(register_type, register_address, [new_soc])


    def set_voltage_I1_I2_in(self, store):
        """
        :param store:
        :return: Gaussian distribution centered around 400, deviation 3
        """
        register_type, register_address = self.get_register_type_address(self.voltage_l1_l2_in)
        value = self.random_gaussian_value(400, 3)
        store.setValues(register_type, register_address, [value])

    def set_voltage_I2_I3_in(self, store):
        """
        :param store:
        :return: Gaussian distribution centered around 400, deviation 3
        """
        register_type, register_address = self.get_register_type_address(self.voltage_l2_l3_in)
        value = self.random_gaussian_value(400, 3)
        store.setValues(register_type, register_address, [value])

    def set_voltage_I3_I1_in(self, store):
        """
        :param store:
        :return: Gaussian distribution centered around 400, deviation 3
        """
        register_type, register_address = self.get_register_type_address(self.voltage_l3_l1_in)
        value = self.random_gaussian_value(400, 3)
        store.setValues(register_type, register_address, [value])

    def set_current_I1_in(self, store):
        """
        :param store:
        :return: active_power_in / (sqrt(3) * voltage_l1_l2_in * power_factor_in)
        """
        register_type, register_address = self.get_register_type_address(self.current_l1_in)
        ap = self.get_value(self.active_power_in, store)
        voltage = self.get_value(self.voltage_l1_l2_in, store)
        pf = self.get_power_factor_in(store)
        current = ap / (math.sqrt(3) * voltage * pf)
        store.setValues(register_type, register_address, [current])

    def set_current_I2_in(self, store):
        """
        :param store:
        :return: active_power_in / (sqrt(3) * voltage_l2_l3_in * power_factor_in)
        """
        register_type, register_address = self.get_register_type_address(self.current_l2_in)
        ap = self.get_value(self.active_power_in, store)
        voltage = self.get_value(self.voltage_l2_l3_in, store)
        pf = self.get_power_factor_in(store)
        current = ap / (math.sqrt(3) * voltage * pf)
        store.setValues(register_type, register_address, [current])


    def set_current_I3_in(self, store):
        """
        :param store:
        :return: active_power_in / (sqrt(3) * voltage_l3_l1_in * power_factor_in)
        """
        register_type, register_address = self.get_register_type_address(self.current_l3_in)
        ap = self.get_value(self.active_power_in, store)
        voltage = self.get_value(self.voltage_l3_l1_in, store)
        pf = self.get_power_factor_in(store)
        current = ap / (math.sqrt(3) * voltage * pf)
        store.setValues(register_type, register_address, [current])


    def set_frequency_in(self, store):
        """
        :param store:
        :return: Gaussian distribution centered around 50, deviation 0.01
        """
        register_type, register_address = self.get_register_type_address(self.frequency_in)
        value = self.random_gaussian_value(50, 0.01)
        store.setValues(register_type, register_address, [value])

    def set_voltage_I1_I2_out(self, store):
        """
        :param store:
        :return: Gaussian distribution centered around 400, deviation 3
        """
        register_type, register_address = self.get_register_type_address(self.voltage_l1_l2_out)
        value = self.random_gaussian_value(400, 3)
        store.setValues(register_type, register_address, [value])

    def set_voltage_I2_I3_out(self, store):
        """
        :param store:
        :return: Gaussian distribution centered around 400, deviation 3
        """
        register_type, register_address = self.get_register_type_address(self.voltage_l2_l3_out)
        value = self.random_gaussian_value(400, 3)
        store.setValues(register_type, register_address, [value])

    def set_voltage_I3_I1_out(self, store):
        """
        :param store:
        :return: Gaussian distribution centered around 400, deviation 3
        """
        register_type, register_address = self.get_register_type_address(self.voltage_l3_l1_out)
        value = self.random_gaussian_value(400, 3)
        store.setValues(register_type, register_address, [value])

    def set_current_I1_out(self, store):
        """
        :param store:
        :return: active_power_out / (sqrt(3) * voltage_l1_l2_out * power_factor_out)

        """
        register_type, register_address = self.get_register_type_address(self.current_l1_out)
        ap = self.get_value(self.active_power_out, store)
        voltage = self.get_value(self.voltage_l1_l2_out, store)
        pf = self.get_power_factor_out(store)
        current = ap / (math.sqrt(3) * voltage * pf)
        store.setValues(register_type, register_address, [current])

    def set_current_I2_out(self, store):
        """
        :param store:
        :return: active_power_out / (sqrt(3) * voltage_l2_l3_out * power_factor_out)
        """
        register_type, register_address = self.get_register_type_address(self.current_l2_out)
        ap = self.get_value(self.active_power_out, store)
        voltage = self.get_value(self.voltage_l2_l3_out, store)
        pf = self.get_power_factor_out(store)
        current = ap / (math.sqrt(3) * voltage * pf)
        store.setValues(register_type, register_address, [current])

    def set_current_I3_out(self, store):
        """
        :param store:
        :return: active_power_out / (sqrt(3) * voltage_l3_l1_out * power_factor_out)
        """
        register_type, register_address = self.get_register_type_address(self.current_l3_out)
        ap = self.get_value(self.active_power_out, store)
        voltage = self.get_value(self.voltage_l3_l1_out, store)
        pf = self.get_power_factor_out(store)
        current = ap / (math.sqrt(3) * voltage * pf)
        store.setValues(register_type, register_address, [current])

    def set_frequency_out(self, store):
        """
        :param store:
        :return: Gaussian distribution centered around 50, deviation 0.01
        """
        register_type, register_address = self.get_register_type_address(self.frequency_out)
        value = self.random_gaussian_value(50, 0.01)
        store.setValues(register_type, register_address, [value])