""" Default configuration of the addresses

The addresses are in following format: first digit represents the type of registry
(coils = 1, discrete input = 2, holding reg = 3, input reg = 4);
remaining two digits are the actual address """

# CONSTANTS
BATTERY_DATA_VARS = 21  # number of fields of battery data
BATTERY_STATE_VARS = 6  # number of fields of battery state

fx_addr_separator = 100  # used to separate registry type and actual address
float_mode = "SCALE"  # means that floats are stored as ints multiplied by scaling_factor
scaling_factor = 100  # scaling factor for floats precision
# TODO: add needed fields for 'COMB', eg endianness

# Battery Data :
soc = 310  # float   dep
active_power_in = 311  # float   in
reactive_power_in = 312  # float   in
current_l1_in = 313  # float   dep
current_l2_in = 314  # float   dep
current_l3_in = 315  # float   dep
voltage_l1_l2_in = 316  # float   semi
voltage_l2_l3_in = 317  # float   semi
voltage_l3_l1_in = 318  # float   semi
frequency_in = 319  # float   semi
active_power_out = 320  # float   in
reactive_power_out = 321  # float   in
current_l1_out = 322  # float   dep
current_l2_out = 323  # float   dep
current_l3_out = 324  # float   dep
voltage_l1_l2_out = 325  # float   semi
voltage_l2_l3_out = 326  # float   semi
voltage_l3_l1_out = 327  # float   semi
frequency_out = 328  # float   semi
active_power_converter = 329  # float   dep
reactive_power_converter = 330  # float   dep

# Battery State
system_status = 331  # int    const
system_mode = 332  # int    const
accept_values = 110  # bool   const
converter_started = 111  # bool   in
input_connected = 112  # bool   in
system_on_backup_battery = 113  # bool   in
