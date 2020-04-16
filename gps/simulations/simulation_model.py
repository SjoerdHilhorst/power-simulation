from simulations.simulation import PowerSimulation


class Simulation(PowerSimulation):

    def __init__(self, env):
        super().__init__()
        self.t = 0
        self.start_soc = env["start_soc"]
        self.api_fun = env["active_power_in"]
        self.rpi_fun = env["reactive_power_in"]
        self.apo_fun = env["active_power_out"]
        self.rpo_fun = env["reactive_power_out"]
        self.update()

    def update(self):
        t = self.t
        self.active_power_in = self.api_fun(t)
        self.reactive_power_in = self.rpi_fun(t)
        self.active_power_out = self.apo_fun(t)
        self.reactive_power_out = self.rpo_fun(t)
        self.t += 1
