""" Default configuration of the addresses

The addresses are in following format: first digit represents the type of registry
(coils = 1, discrete input = 2, holding reg = 3, input reg = 4);
remaining two digits are the actual address """

fx_addr_separator = 100 # used to separate registry type and actual address

float_mode = "SCALE"  # means that floats are stored as ints multiplied by scaling_factor
scaling_factor = 100  # scaling factor for floats precision

# Battery Data:

battery_id = 310  # str     config
soc = 311  # float   dep
active_power_in = 312  # float   in
reactive_power_in = 313  # float   in
current_l1_in = 314  # float   dep
current_l2_in = 315  # float   dep
current_l3_in = 316  # float   dep
voltage_l1_l2_in = 317  # float   semi
voltage_l2_l3_in = 318  # float   semi
voltage_l3_l1_in = 319  # float   semi
frequency_in = 320  # float   semi
active_power_out = 321  # float   in
reactive_power_out = 322  # float   in
current_l1_out = 323  # float   dep
current_l2_out = 324  # float   dep
current_l3_out = 325  # float   dep
voltage_l1_l2_out = 326  # float   semi
voltage_l2_l3_out = 327  # float   semi
voltage_l3_l1_out = 328  # float   semi
frequency_out = 329  # float   semi
active_power_converter = 330  # float   dep
reactive_power_converter = 331  # float   dep

# Battery State

time = 332
system_status = 333  # int    const
system_mode = 334  # int    const
accept_values = 110  # bool   const
converter_started = 111  # bool   in
input_connected = 112  # bool   in
system_on_backup_battery = 113  # bool   in
