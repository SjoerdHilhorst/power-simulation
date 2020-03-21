
from battery import Battery

import custom_config
import config

# user chooses the option for map

#configuration = "CUSTOM"
configuration = "DEFAULT"


# if it is custom user provides information and config is modified, here it is hardcoded for now
if configuration == "CUSTOM":
    float_mode = "SCALE"
    scaling_factor = 100

    # for simplicity of example consecutive list of addresses is hardcoded
    # TODO: in future we validate provided addresses such that there is no duplicates
    addresses = list(range(350, 350 + config.BATTERY_DATA_VARS + config.BATTERY_STATE_VARS + 1))

    # this will be defined by a function based on the num of digits in address, for now hardcoded
    fx_addr_separator = 100
    custom_config.modify(float_mode, fx_addr_separator, scaling_factor, addresses)

battery = Battery(60, 60, 30, 20, 1, 1, 1)
battery.run()




