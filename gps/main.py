
from battery import Battery
import json_config
import simulations


if __name__ == "__main__":
    #env = json_config.get_custom_json('env')
    env = json_config.get_custom_json('default')

    battery = Battery(env)

    sim_type = env["simulation_type"]
    if sim_type == "random":
        power_sim = simulations.RandomSimulation((0, 200), (-65, 185), (-11, 25), (-15, 25))
    elif sim_type == "historic":
        power_sim = simulations.HistoricSimulation()
    elif sim_type == "simulation":
        power_sim = simulations.Simulation()

    battery.connect_power(power_sim)

    battery.update()
    battery.run()


