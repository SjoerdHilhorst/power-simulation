import threading
import time

import numpy as np

"""
Superclass for simulation which is responsible for updating all fields, as it it IS the simulation in essence. Was merged
with MathEngine, so it provides default implementations of formulas. SHOULD NOT BE MODIFIED BY CLIENT
"""


class SimulationSuper:

    def __init__(self, battery, env):
        self.t = 0
        self.env = env
        self.fields = env['fields']
        self.delay = env['update_delay']
        self.max_iter = env['max_iterations']
        self.battery = battery
        self.db = None
        self.graph = None

    def update(self):
        self.update_powers()
        self.update_relational()
        self.update_custom()
        if self.db: self.write_to_db()
        if self.graph: self.write_to_graph()



    def update_powers(self):
        field = self.fields
        self.battery.set_value(field['active_power_in'], self.get_active_power_in())
        self.battery.set_value(field['reactive_power_in'], self.get_reactive_power_in())
        self.battery.set_value(field['active_power_out'], self.get_active_power_out())
        self.battery.set_value(field['reactive_power_out'], self.get_reactive_power_out())

    def update_relational(self):
        field = self.fields
        self.battery.set_value(field["active_power_converter"], self.get_active_power_converter())
        self.battery.set_value(field["reactive_power_converter"], self.get_reactive_power_converter())
        self.battery.set_value(field["voltage_l1_l2_in"], self.get_voltage_I1_I2_in())
        self.battery.set_value(field["voltage_l2_l3_in"], self.get_voltage_I2_I3_in())
        self.battery.set_value(field["voltage_l3_l1_in"], self.get_voltage_I3_I1_in())
        self.battery.set_value(field["current_l1_in"], self.get_current_I1_in())
        self.battery.set_value(field["current_l2_in"], self.get_current_I2_in())
        self.battery.set_value(field["current_l3_in"], self.get_current_I3_in())
        self.battery.set_value(field["frequency_in"], self.get_frequency_in())
        self.battery.set_value(field["voltage_l1_l2_out"], self.get_voltage_I1_I2_out())
        self.battery.set_value(field["voltage_l2_l3_out"], self.get_voltage_I2_I3_out())
        self.battery.set_value(field["voltage_l3_l1_out"], self.get_voltage_I3_I1_out())
        self.battery.set_value(field["current_l1_out"], self.get_current_I1_out())
        self.battery.set_value(field["current_l2_out"], self.get_current_I2_out())
        self.battery.set_value(field["current_l3_out"], self.get_current_I3_out())
        self.battery.set_value(field["frequency_out"], self.get_frequency_out())
        self.battery.set_value(field["soc"], self.get_soc())

    def update_custom(self):
        '''
        should be implemented by the subclass in case there are custom fields
        '''
        pass

    def run_simulation(self):
        for i in range(0, self.max_iter):
            print(i)
            self.update()
            self.t += 1
            time.sleep(self.delay)

    def run_thread(self):
        t = threading.Thread(target=self.run_simulation, daemon=True)
        t.start()

    def write_to_db(self):
        address = self.fields
        values = []
        for field in address:
            values.append(self.battery.get_value(address[field]))
        self.db.write("battery", values)

    def write_to_graph(self):
        for field in self.graph.graphs:
            value = self.battery.get_value(self.fields[field])
            self.graph.data[field].append(value)
        self.graph.data['t'] += 1
        
    def random_gaussian_value(self, mu, sigma):
        return np.random.normal(mu, sigma)

    def get_active_power_in(self):
        api = 0
        if not self.battery.is_input_connected():
            api = 0
        return api

    def get_reactive_power_in(self):
        rpi = 0
        if not self.battery.is_input_connected():
            rpi = 0
        return rpi

    def get_active_power_out(self):
        apo = 0
        return apo

    def get_reactive_power_out(self):
        rpo = 0
        return rpo

    def get_power_factor_in(self):
        """
        :return: active_power_in / sqrt(active_power_in^2 + reactive_power_in^2)
        """
        ap = self.battery.get_value(self.fields['active_power_in'])
        rp = self.battery.get_value(self.fields['reactive_power_in'])
        return ap / np.math.sqrt(ap * ap + rp * rp) if ap and rp else 0

    def get_power_factor_out(self):
        """
        :return: active_power_out / sqrt(active_power_out^2 + reactive_power_out^2)
        """
        ap = self.battery.get_value(self.fields['active_power_out'])
        rp = self.battery.get_value(self.fields['reactive_power_out'])
        return ap / np.math.sqrt(ap * ap + rp * rp) if ap and rp else 0

    def get_active_power_converter(self):
        """
        :return: active_power_in - active_power_out
        """
        if not self.battery.is_converter_started():
            apc = 0
        else:
            apc = self.battery.get_value(self.fields['active_power_in']) - self.battery.get_value(
                self.fields['active_power_out'])
        return apc

    def get_reactive_power_converter(self):
        """
        :return: reactive_power_in - reactive_power_out
        """
        if not self.battery.is_converter_started():
            rpc = 0
        else:
            rpc = self.battery.get_value(self.fields['reactive_power_in']) - self.battery.get_value(
                self.fields['reactive_power_out'])
        return rpc

    def get_soc(self):
        """
        :return: previous SoC + [(active_power_converter) /
                max battery capacity * 3600.
        """
        if not self.battery.is_converter_started():
            return self.battery.get_value(self.fields['soc'])
        prev_soc = self.battery.get_value(self.fields['soc'])
        apc = self.battery.get_value(self.fields['active_power_converter'])
        new_soc = prev_soc + (apc / (self.battery.max_capacity * 3600)) * 100
        if new_soc > 100:
            new_soc = 100
        elif new_soc < 0:
            new_soc = 0
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
        if not self.battery.is_input_connected():
            return 0
        ap = self.battery.get_value(self.fields['active_power_in'])
        voltage = self.battery.get_value(self.fields['voltage_l1_l2_in'])
        pf = self.get_power_factor_in()
        current = ap / (np.math.sqrt(3) * voltage * pf) * 1000 if pf else 0
        return current

    def get_current_I2_in(self):
        """
        :return: active_power_in / (sqrt(3) * voltage_l2_l3_in * power_factor_in)
        """
        if not self.battery.is_input_connected():
            return 0
        ap = self.battery.get_value(self.fields['active_power_in'])
        voltage = self.battery.get_value(self.fields['voltage_l2_l3_in'])
        pf = self.get_power_factor_in()
        current = ap / (np.math.sqrt(3) * voltage * pf) * 1000 if pf else 0
        return current

    def get_current_I3_in(self):
        """
        :return: active_power_in / (sqrt(3) * voltage_l3_l1_in * power_factor_in)
        """
        if not self.battery.is_input_connected():
            return 0
        ap = self.battery.get_value(self.fields['active_power_in'])
        voltage = self.battery.get_value(self.fields['voltage_l3_l1_in'])
        pf = self.get_power_factor_in()
        current = ap / (np.math.sqrt(3) * voltage * pf) * 1000 if pf else 0
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
        ap = self.battery.get_value(self.fields['active_power_out'])
        voltage = self.battery.get_value(self.fields['voltage_l1_l2_out'])
        pf = self.get_power_factor_out()
        current = ap / (np.math.sqrt(3) * voltage * pf) * 1000 if pf else 0
        return current

    def get_current_I2_out(self):
        """
        :return: active_power_out / (sqrt(3) * voltage_l2_l3_out * power_factor_out)
        """
        ap = self.battery.get_value(self.fields['active_power_out'])
        voltage = self.battery.get_value(self.fields['voltage_l2_l3_out'])
        pf = self.get_power_factor_out()
        current = ap / (np.math.sqrt(3) * voltage * pf) * 1000 if pf else 0
        return current

    def get_current_I3_out(self):
        """
        :return: active_power_out / (sqrt(3) * voltage_l3_l1_out * power_factor_out)
        """
        ap = self.battery.get_value(self.fields['active_power_out'])
        voltage = self.battery.get_value(self.fields['voltage_l3_l1_out'])
        pf = self.get_power_factor_out()
        current = ap / (np.math.sqrt(3) * voltage * pf) * 1000 if pf else 0
        return current

    def get_frequency_out(self):
        """
        :return: Gaussian distribution centered around 50, deviation 0.01
        """
        value = self.random_gaussian_value(50, 0.01)
        return value
