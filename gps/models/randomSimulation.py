from gps.models.simulationClass import PowerSimulation
import random


class RandomSimulation(PowerSimulation):

    def __init__(self, range_active_in, range_reactive_in, range_active_out, range_reactive_out):
        self.range_active_in = range_active_in
        self.range_reactive_in = range_reactive_in
        self.range_active_out = range_active_out
        self.range_reactive_out = range_reactive_out
        super().__init__()

    def update(self):
        self.reactive_power_in = round(random.uniform(*self.range_reactive_in), 1)
        self.active_power_in = round(random.uniform(*self.range_active_in), 1)
        self.reactive_power_out = round(random.uniform(*self.range_reactive_out), 1)
        self.active_power_out = round(random.uniform(*self.range_active_out), 1)
