import numpy as np

class MathEngine:

    def __init__(self, battery, address):
        self.battery = battery
        self.address = address

    def random_gaussian_value(self, mu, sigma):
        return np.random.normal(mu, sigma)

    def get_power_factor_in(self):
        """
        :return: active_power_in / sqrt(active_power_in^2 + reactive_power_in^2)
        """
        ap = self.battery.get_value(self.address['active_power_in'])
        rp = self.battery.get_value(self.address['reactive_power_in'])
        return ap / np.math.sqrt(ap * ap + rp * rp) if ap and rp else 0

    def get_power_factor_out(self):
        """
        :return: active_power_out / sqrt(active_power_out^2 + reactive_power_out^2)
        """
        ap = self.battery.get_value(self.address['active_power_out'])
        rp = self.battery.get_value(self.address['reactive_power_out'])
        return ap / np.math.sqrt(ap * ap + rp * rp) if ap and rp else 0

    def get_active_power_converter(self):
        """
        :return: active_power_in - active_power_out
        """
        apc = self.battery.get_value(self.address['active_power_in']) - self.battery.get_value(self.address['active_power_out'])
        return apc

    def get_reactive_power_converter(self):
        """
        :return: reactive_power_in - reactive_power_out
        """
        rpc = self.battery.get_value(self.address['reactive_power_in']) - self.battery.get_value(
            self.address['reactive_power_out'])
        return rpc

    def get_soc(self):
        """
        :return: previous SoC + [(active_power_converter) /
                (Some configurable max battery capacity, say 330 kWh)] * 3600.
        """
        prev_soc = self.battery.get_value(self.address['soc'])
        apc = self.battery.get_value(self.address['active_power_converter'])

        # multiply by 1000 to convert from kWh
        new_soc = prev_soc + (apc / (self.battery.max_capacity )) * 3600
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
        ap = self.battery.get_value(self.address['active_power_in'])
        voltage = self.battery.get_value(self.address['voltage_l1_l2_in'])
        pf = self.get_power_factor_in()
        current = ap / (np.math.sqrt(3) * voltage * pf) * 1000 if pf else 0  # from kW to W
        return current

    def get_current_I2_in(self):
        """
        :return: active_power_in / (sqrt(3) * voltage_l2_l3_in * power_factor_in)
        """
        ap = self.battery.get_value(self.address['active_power_in'])
        voltage = self.battery.get_value(self.address['voltage_l2_l3_in'])
        pf = self.get_power_factor_in()
        current = ap / (np.math.sqrt(3) * voltage * pf) * 1000 if pf else 0  # from kW to W
        return current

    def get_current_I3_in(self):
        """
        :return: active_power_in / (sqrt(3) * voltage_l3_l1_in * power_factor_in)
        """
        ap = self.battery.get_value(self.address['active_power_in'])
        voltage = self.battery.get_value(self.address['voltage_l3_l1_in'])
        pf = self.get_power_factor_in()
        current = ap / (np.math.sqrt(3) * voltage * pf) * 1000 if pf else 0  # from kW to W
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
        ap = self.battery.get_value(self.address['active_power_out'])
        voltage = self.battery.get_value(self.address['voltage_l1_l2_out'])
        pf = self.get_power_factor_out()
        current = ap / (np.math.sqrt(3) * voltage * pf) * 1000 if pf else 0  # from kW to W
        return current

    def get_current_I2_out(self):
        """
        :return: active_power_out / (sqrt(3) * voltage_l2_l3_out * power_factor_out)
        """
        ap = self.battery.get_value(self.address['active_power_out'])
        voltage = self.battery.get_value(self.address['voltage_l2_l3_out'])
        pf = self.get_power_factor_out()
        current = ap / (np.math.sqrt(3) * voltage * pf) * 1000 if pf else 0  # from kW to W
        return current

    def get_current_I3_out(self):
        """
        :return: active_power_out / (sqrt(3) * voltage_l3_l1_out * power_factor_out)
        """
        ap = self.battery.get_value(self.address['active_power_out'])
        voltage = self.battery.get_value(self.address['voltage_l3_l1_out'])
        pf = self.get_power_factor_out()
        current = ap / (np.math.sqrt(3) * voltage * pf) * 1000 if pf else 0  # from kW to W
        return current

    def get_frequency_out(self):
        """
        :return: Gaussian distribution centered around 50, deviation 0.01
        """
        value = self.random_gaussian_value(50, 0.01)
        return value
