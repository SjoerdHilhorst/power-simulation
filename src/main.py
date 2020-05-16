from battery import Battery

from database import Database

from config.env import env
from simulations.simulation import Simulation

if __name__ == "__main__":

    battery = Battery(env)
    simulation = Simulation(battery, env)

    if env["database"]["enabled"]:
        db_env = env["database"]
        fields = env["fields"]
        db = Database(db_env, fields)
        simulation.db = db

    if env["graph"]["enabled"]:
        from graph import Graph

        graph_env = env["graph"]
        fields = graph_env["fields"]
        graph = Graph(fields)
        simulation.graph = graph
        simulation.run_thread()
        graph.run()
    else:
        simulation.run_simulation()
