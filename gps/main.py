from battery import Battery
import simulations
from database import Database
import threading

# define which environment you want to use
from config.env import env


if __name__ == "__main__":
    battery = Battery(env)
    max_iter = env["max_iterations"]
    print(max_iter)
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
        env_sim = env["historic_simulation"]
        power_sim = simulations.HistoricSimulation(env_sim, battery, max_iter, delay)

    elif sim_type == "simulation":
        env_sim = env["simulation"]
        power_sim = simulations.Simulation(env_sim, battery, max_iter, delay)

    else:
        raise LookupError("This simulation type does not exist: ", sim_type)

    battery.run_server()

    
    
    if env["graph"]["enabled"]:
        from graph import Graph
        graph_env = env["graph"]
        fields = graph_env["fields"]
        graph = Graph(fields)
        battery.graph = graph
        power_sim.run_thread()
        graph.run()
    else:
        power_sim.run_simulation()







