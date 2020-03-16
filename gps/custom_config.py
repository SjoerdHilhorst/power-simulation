import config as config
from config import *


# changes the configuration;
# param addresses is the list of addresses provided by user while configuring map. Order matters
def modify(float_mode, fx_addr_separator, scaling_factor, addresses):
    config.float_mode = float_mode
    config.fx_addr_separator = fx_addr_separator
    config.scaling_factor = scaling_factor

    config.soc = addresses[0]  # float   dep
    config.active_power_in = addresses[1]  # float   in
    config.reactive_power_in = addresses[2]  # float   in
    config.current_l1_in = addresses[3]  # float   dep
    config.current_l2_in = addresses[4]  # float   dep
    config.current_l3_in = addresses[5]  # float   dep
    config.voltage_l1_l2_in = addresses[6]  # float   semi
    config.voltage_l2_l3_in = addresses[7]  # float   semi
    config.voltage_l3_l1_in = addresses[8]  # float   semi
    config.frequency_in = addresses[9]  # float   semi
    config.active_power_out = addresses[10]  # float   in
    config.reactive_power_out = addresses[11]  # float   in
    config.current_l1_out = addresses[12]  # float   dep
    config.current_l2_out = addresses[13]  # float   dep
    config.current_l3_out = addresses[14]  # float   dep
    config.voltage_l1_l2_out = addresses[15]  # float   semi
    config.voltage_l2_l3_out = addresses[16]  # float   semi
    config.voltage_l3_l1_out = addresses[17]  # float   semi
    config.frequency_out = addresses[18]  # float   semi
    config.active_power_converter = addresses[19]  # float   dep
    config.reactive_power_converter = addresses[20]  # float   dep

    # Battery State
    config.system_status = addresses[21]  # int    const
    config.system_mode = addresses[22]  # int    const
    config.accept_values = addresses[23]  # bool   const
    config.converter_started = addresses[24]  # bool   in
    config.input_connected = addresses[25]  # bool   in
    config.system_on_backup_battery = addresses[26]  # bool   in
