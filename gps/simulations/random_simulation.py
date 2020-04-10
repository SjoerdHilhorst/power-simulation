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

    def update(self):
        self.reactive_power_in = round(random.uniform(*self.range_reactive_in), 1)
        self.active_power_in = round(random.uniform(*self.range_active_in), 1)
        self.reactive_power_out = round(random.uniform(*self.range_reactive_out), 1)
        self.active_power_out = round(random.uniform(*self.range_active_out), 1)
