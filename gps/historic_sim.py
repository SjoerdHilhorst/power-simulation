from pymodbus.constants import Endian
from battery import Battery
import json_config
from powers import *


if __name__ == "__main__":
    env = json_config.get_custom_json("env")

    # battery is instantiated, only constants are in the input, "custom" or None is for accessing the json
    battery = Battery(env, 1, 5, 1, 1)


    # connect battery to the power
    battery.connect_power_in(power_source)

    # connect battery to the load
    battery.connect_power_out(power_load)

    # fill in all dependent fields
    battery.update()

    # at this point battery starts to update its state
    battery.run()