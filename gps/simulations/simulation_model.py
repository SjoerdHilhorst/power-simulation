from simulations.simulation import PowerSimulation


class Simulation(PowerSimulation):

    def __init__(self, initial_values):
        self.start_soc = initial_values["soc"]
        self.active_power_in = initial_values["active_power_in"]
        self.reactive_power_in = initial_values["reactive_power_in"]
        self.active_power_out = initial_values["active_power_out"]
        self.reactive_power_out = initial_values["reactive_power_out"]

    def update(self):
        # code for how to update the simulation 
        # maybe most essential part of project ? :)
        pass
