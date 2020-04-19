from battery import Battery
import simulations
import socket
import json
from database import Database

# define which environment you want to use
from config.env import env


if __name__ == "__main__":

    # finds an availabe port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost',0))
    address = sock.getsockname()
    env['server_address'] = address
    # saves port for session (so client knows which port
    with open('./config/current_address.json','w') as outfile:
        json.dump(address,outfile)
    sock.close()

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

    battery.run_server()
    power_sim.run()


