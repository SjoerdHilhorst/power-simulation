
from battery import Battery
import json_config
import simulations
from database import Database

json_file = 'env'


if __name__ == "__main__":
    env = json_config.get_custom_json(json_file)

    battery = Battery(env)

    if env["database"]["enabled"]:
        db_env = env["database"]
        address = env["address"]
        db = Database(db_env, address)
        battery.db = db
    sim_type = env["simulation_type"]
    if sim_type == "random":
        random_ranges = env["random_ranges"]
        power_sim = simulations.RandomSimulation(random_ranges)

    elif sim_type == "historic":
        csv_name = env["historic_csv_name"]
        start_index = env["start_index"]
        power_sim = simulations.HistoricSimulation(csv_name, start_index)

    elif sim_type == "simulation":
        initial_values = env["initial_values"]
        power_sim = simulations.Simulation(initial_values)

    else:
        raise LookupError("This simulation type does not exist: ", sim_type)

    battery.connect_power(power_sim)
    battery.run()


