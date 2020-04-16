from simulations.simulation import PowerSimulation
import random


class RandomSimulation(PowerSimulation):

    def __init__(self, random_ranges):
        self.range_active_in = tuple(random_ranges["range_active_power_in"])
        self.range_reactive_in = tuple(random_ranges["range_reactive_power_in"])
        self.range_active_out = tuple(random_ranges["range_active_power_out"])
        self.range_reactive_out = tuple(random_ranges["range_reactive_power_out"])
        super().__init__()
        self.start_soc = random_ranges["start_soc"]
        self.update()

    def rand(self, range):
        return round(random.uniform(*range), 1)

    def update(self):
        self.reactive_power_in = self.rand(self.range_reactive_in)
        self.active_power_in = self.rand(self.range_active_in)
        self.reactive_power_out = self.rand(self.range_active_out)
        self.active_power_out = self.rand(self.range_reactive_out)
        self.t += 1
