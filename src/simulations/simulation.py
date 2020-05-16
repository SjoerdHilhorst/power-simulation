
from numpy.ma import sin

from util.csv_reader import CSVReader
from simulations.simulation_super import SimulationSuper

"""A class where a client can override any functions or specify that he wants a value from csv. At least methods of 
re(active)_power_in/out  HAS TO BE PROVIDED """


class Simulation(SimulationSuper):

    def __init__(self, battery, env):
        super().__init__(battery, env)
        self.csv_reader = CSVReader(env['from_csv'])

    # examples
    def get_active_power_in(self):
        api = self.csv_reader.get_from_csv('active_power_in')
        if not self.battery.is_input_connected():
            api = 0
        return api

    def get_reactive_power_in(self):
        rpi = self.csv_reader.get_from_csv('reactive_power_in')
        if not self.battery.is_input_connected():
            rpi = 0
        return rpi

    def get_active_power_out(self):
        apo = self.csv_reader.get_from_csv('active_power_out')
        return apo

    def get_reactive_power_out(self):
        rpo = self.csv_reader.get_from_csv('reactive_power_out')
        return rpo

    def get_custom(self):
        return sin(self.time_elapsed)



    def update_custom(self):
        self.battery.set_value(self.fields['custom'], self.get_custom())
