from battery import Battery
import simulations
from database import Database

# define which environment you want to use
from config.env import env


if __name__ == "__main__":
    battery = Battery(env)

    if env["database"]["enabled"]:
        db_env = env["database"]
        address = env["address"]
        db = Database(db_env, address)
        battery.db = db

    sim_type = env["simulation_type"]
    if sim_type == "random":
        random_ranges = env["random_simulation"]
        power_sim = simulations.RandomSimulation(random_ranges)

    elif sim_type == "historic":
        env = env["historic_simulation"]
        power_sim = simulations.HistoricSimulation(env)

    elif sim_type == "simulation":
        env = env["simulation"]
        power_sim = simulations.Simulation(env)

    else:
        raise LookupError("This simulation type does not exist: ", sim_type)

    battery.connect_power(power_sim)
    battery.run()


