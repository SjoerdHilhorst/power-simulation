import random


from numpy.ma import sin

from csv_reader import CSVReader
from simulations.simulation_model import SimulationSuper

"""A class where a client can override any functions or specify that he wants a value from csv. At least methods of 
re(active)_power_in/out  HAS TO BE PROVIDED """


class Simulation(SimulationSuper):

    def __init__(self, battery, address):
        super().__init__(battery, address)
        self.csv_reader = CSVReader(self.env['from_csv'])

# examples
    def get_active_power_in(self):
        api = self.csv_reader.get_from_csv('active_power_in')
        if not self.battery.is_input_connected():
            api = 0
        return api

    def get_reactive_power_in(self):
        rpi = 59
        if not self.battery.is_input_connected():
            rpi = 0
        return rpi

    def get_active_power_out(self):
        apo = random.randint(1,3) * sin(self.t + random.randint(0,15)) + random.randint(1,40)
        return float(apo)

    def get_reactive_power_out(self):
        rpo = self.csv_reader.get_from_csv('reactive_power_out')
        return rpo

    def get_current_I1_in(self):
        return 200