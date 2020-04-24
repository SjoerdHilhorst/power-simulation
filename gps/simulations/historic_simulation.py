from simulations.simulation import PowerSimulation
import pandas as pd


def open_csv(csv_name):
    csv_name = "../" + csv_name + ".csv"
    file = pd.read_csv(csv_name)

    api = file["active_power_in"].tolist()
    rpi = file["reactive_power_in"].tolist()
    apo = file["active_power_out"].tolist()
    rpo = file["reactive_power_out"].tolist()
    soc = file["soc"].tolist()
    return api, rpi, apo, rpo, soc


class HistoricSimulation(PowerSimulation):
    """ Simulation where powers are fetched from csv file """

    def __init__(self, env, battery, max_iter, delay):
        super().__init__(battery, max_iter, delay)
        start_index = env["start_index"]
        api, rpi, apo, rpo, soc = open_csv(env["csv_name"])
        self.api_list = api[start_index:]
        self.rpi_list = rpi[start_index:]
        self.apo_list = apo[start_index:]
        self.rpo_list = rpo[start_index:]
        self.soc_list = soc[start_index:]
        self.start_soc = battery.set_value(battery.field["soc"], soc[0])
        self.max_iter = len(self.api_list)-1
        self.update()

    def update(self):
        self.active_power_in = self.api_list.pop(0)
        self.reactive_power_in = self.rpi_list.pop(0)
        self.active_power_out = self.apo_list.pop(0)
        self.reactive_power_out = self.rpo_list.pop(0)
        self.t += 1
        soc = self.soc_list.pop(0)

