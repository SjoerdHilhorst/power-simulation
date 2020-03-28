from pymodbus.constants import Endian

from battery import Battery
import custom_config
import config

# Uncomment the option you want to test

# configuration = "CUSTOM"
configuration = "DEFAULT" # default configuration; floats are stored in "SCALE"

# if it is custom user provides information and config is modified, here it is hardcoded for now
if configuration == "CUSTOM":
    # float_mode = "SCALE" # uncomment if user wants to store float using scaling and one register
    float_mode = "COMB"  # uncomment if user wants to store float in IEEE  754 format
    endian = Endian.Big
    scaling_factor = 100
    addresses = list(range(310, 355, 2)) + list(range(110, 114))

    # this will be defined by a function based on the num of digits in address, for now hardcoded
    fx_addr_separator = 100
    custom_config.modify(float_mode, fx_addr_separator, scaling_factor, endian, endian, addresses)

battery = Battery(300.69, 60, 30, 20, 1, 1, 1)
battery.store.validate(3, 10, 1)
battery.print_all_values()
battery.run()
