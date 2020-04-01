from pymodbus.constants import Endian

from battery import Battery
import json_config
from powers import *

# Uncomment the option you want to test

#configuration = "CUSTOM"
filename = "custom"
configuration = "DEFAULT"  # default configuration; floats are stored in "SCALE"

# if it is custom user provides information and config is modified, here it is hardcoded for now
if configuration == "CUSTOM":
    float_mode = "SCALE"  # uncomment if user wants to store float using scaling and one register
    # float_mode = "COMB"  # uncomment if user wants to store float in IEEE  754 format
    endian = Endian.Big
    scaling_factor = 100
    addresses = list(range(310, 355, 2)) + list(range(110, 114))
    # this will be defined by a function based on the num of digits in address, for now hardcoded
    fx_addr_separator = 100
    # makes a new json with these variables at "Config/filename.json"
    json_config.set_custom_json(filename, fx_addr_separator, float_mode, endian, endian, scaling_factor, addresses)

address = ("localhost", 5030)
id = "GREENER_001"

# battery is instantiated, only constants are in the input, "custom" or None is for accessing the json
battery = Battery(id, address, None if configuration == "DEFAULT" else "custom", 1, 5, 1, 1)

power_source = PowerIn((0, 200), (-65, 185))
power_load = PowerOut((-11, 25), (-15, 25))

battery.connect_power_in(power_source)

battery.connect_power_out(power_load)

battery.update()

battery.run()
