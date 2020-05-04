from simulations.simulation import PowerSimulation
import pandas as pd
from os.path import dirname, normpath, join


def open_csv(csv_name):
    dirpath = normpath(join(dirname(__file__), "../../"))
    csv_name = csv_name + ".csv"
    filepath = join(dirpath, csv_name)
    try:
        file = pd.read_csv(filepath)
    except FileNotFoundError:
        print("FileNotFoundError: file %s not found in %s" % (csv_name, dirpath))
        exit(1)

    api = file["active_power_in"].tolist()
    rpi = file["reactive_power_in"].tolist()
    apo = file["active_power_out"].tolist()
    rpo = file["reactive_power_out"].tolist()
    return api, rpi, apo, rpo


class HistoricSimulation(PowerSimulation):
    """ Simulation where powers are fetched from csv file """

    def __init__(self, env, battery, max_iter, delay):
        super().__init__(battery, max_iter, delay)
        start_index = env["start_index"]
        api, rpi, apo, rpo = open_csv(env["csv_name"])
        self.api_list = api[start_index:]
        self.rpi_list = rpi[start_index:]
        self.apo_list = apo[start_index:]
        self.rpo_list = rpo[start_index:]

        self.max_iter = len(self.api_list) - 1
        self.update()

    def update(self):
        self.active_power_in = self.api_list.pop(0)
        self.reactive_power_in = self.rpi_list.pop(0)
        self.active_power_out = self.apo_list.pop(0)
        self.reactive_power_out = self.rpo_list.pop(0)
        self.t += 1
