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
    def __init__(self, csv_name, start_index):
        api, rpi, apo, rpo, soc = open_csv(csv_name)
        self.api_list = api[start_index:]
        self.rpi_list = rpi[start_index:]
        self.apo_list = apo[start_index:]
        self.rpo_list = rpo[start_index:]
        self.soc_list = soc[start_index:]
        super().__init__()

    def update(self):
        try:
            self.active_power_in = self.api_list.pop(0)
            self.reactive_power_in = self.rpi_list.pop(0)
            self.active_power_out = self.apo_list.pop(0)
            self.reactive_power_out = self.rpo_list.pop(0)
            soc = self.soc_list.pop(0)

            #print("update api",  self.active_power_in, "rpi", self.reactive_power_in, "apo", self.active_power_out, "rpo", self.reactive_power_out)
            #print("SOC: ", soc)
        except IndexError:
            print("historic file is empty, simulation done")
            exit(0)
        pass
