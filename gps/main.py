
from battery import Battery
import json_config
import simulations

json_file = 'env'


if __name__ == "__main__":
    env = json_config.get_custom_json(json_file)

    battery = Battery(env)

    sim_type = env["simulation_type"]
    if sim_type == "random":
        power_sim = simulations.RandomSimulation((0, 200), (-65, 185), (-11, 25), (-15, 25))
    elif sim_type == "historic":
        csv_name = env["historic_csv_name"]
        start_index = env["start_index"]
        power_sim = simulations.HistoricSimulation(csv_name, start_index)
    elif sim_type == "simulation":
        power_sim = simulations.Simulation()
    else:
        raise LookupError("This simulation type does not exist: ", sim_type)

    battery.connect_power(power_sim)
    battery.run()


