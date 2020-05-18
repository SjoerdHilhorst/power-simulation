from battery import Battery

from database import Database
from graph import Graph
from config.env import env
from simulations.simulation import Simulation

if __name__ == "__main__":

    """
    Instantiation of the device and a simulation
    """
    battery = Battery(env)
    simulation = Simulation(battery, env)

    """
    Setting the database (if enabled in env)
    """
    if env["database"]["enabled"]:
        db_env = env["database"]
        fields = env["fields"]
        db = Database(db_env, fields)
        simulation.db = db

    """
    Setting the graph (if enabled in env)
    """
    if env["graph"]["enabled"]:
        graph_env = env["graph"]
        fields = graph_env["fields"]
        graph = Graph(fields)
        simulation.graph = graph
        simulation.run_thread()
        graph.run()
    else:
        simulation.run_simulation()
