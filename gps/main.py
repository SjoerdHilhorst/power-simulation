from battery import Battery
import simulations
from database import Database
import threading
import sys
# define which environment you want to use
from config.env import env


if __name__ == "__main__":
    battery = Battery(env)
    max_iter = env["max_iterations"]
    delay = env["update_delay"]

    if env["database"]["enabled"]:
        db_env = env["database"]
        address = env["address"]
        db = Database(db_env, address)
        battery.db = db

    sim_type = env["simulation_type"]
    if sim_type == "random":
        random_ranges = env["random_simulation"]
        power_sim = simulations.RandomSimulation(random_ranges, battery, max_iter, delay)

    elif sim_type == "historic":
        env = env["historic_simulation"]
        power_sim = simulations.HistoricSimulation(env, battery, max_iter, delay)

    elif sim_type == "simulation":
        env = env["simulation"]
        power_sim = simulations.Simulation(env, battery, max_iter, delay)

    else:
        raise LookupError("This simulation type does not exist: ", sim_type)

    if True:
        from graph import MainWindow
        graph = MainWindow()

    power_sim.graph = graph

    battery.run_server()
    x = threading.Thread(target=power_sim.run)
    x.start()
    graph.run()







