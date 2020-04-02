from pymodbus.constants import Endian

from battery import Battery
import json_config
from models import historic_sim, random_sim, sim


address = ("localhost", 5030)
id = "GREENER_001"
filename = "custom"
float_mode = "SCALE"
endian = Endian.Big
scaling_factor = 100
fx_addr_separator = 100
sim_type = "random"
addresses = list(range(310, 355, 2)) + list(range(110, 114))


if __name__ == "__main__":
    json_config.set_custom_json(filename, fx_addr_separator, address, id, sim_type, float_mode, endian, endian, scaling_factor, addresses)
    env = json_config.get_custom_json(filename)

    # battery is instantiated, only constants are in the input, "custom" or None is for accessing the json
    battery = Battery(env, 1, 5, 1, 1)

    sim_type = env["simulation_type"]
    if sim_type == "random":
        random_sim.random_simulation(battery)
    if sim_type == "historic":
        historic_sim.historic_simulation(battery)
    if sim_type == "simulation":
        sim.simulation(battery)


