from pymodbus.constants import Endian

from battery import Battery
import json_config
from models import historic_sim, random_sim, sim
from models.rand_sim_class import  RandomSimulation, HistoricSimulation, Simulation

if __name__ == "__main__":
    env = json_config.get_custom_json(filename)

    # battery is instantiated, only constants are in the input, "custom" or None is for accessing the json
    battery = Battery(env)

    sim_type = env["simulation_type"]
    if sim_type == "random":
        power_sim = RandomSimulation((0, 200), (-65, 185), (-11, 25), (-15, 25))
    if sim_type == "historic":
        historic_sim.historic_simulation(battery)
    if sim_type == "simulation":
        sim.simulation(battery)

    battery.connect_power(power_sim)

    battery.update()
    battery.run()


