from pymodbus.payload import Endian

"""
Default configuration of the addresses

The addresses are in following format: first digit represents the type of registry
(coils = 1, discrete input = 2, holding reg = 3, input reg = 4);
remaining two digits are the actual address
"""

"""
number of fields of battery data
"""
BATTERY_DATA_VARS = 21
"""
number of fields of battery state
"""
BATTERY_STATE_VARS = 6

"""
used to separate registry type and actual address
"""
fx_addr_separator = 100
"""
means that floats are stored as ints multiplied by scaling_factor
"""
float_mode = "SCALE"        #
# float_mode = "COMB"       # uncomment if user wants to store float in IEEE  754 format
word_order = Endian.Big     # define endianness of byte in word
byte_order = Endian.Big     # define endianness of bits in byte
scaling_factor = 100        # scaling factor for floats precision, only needed if float_mode = "SCALE"

# Battery Data

soc = 310  # float   dep
active_power_in = 312  # float   in
reactive_power_in = 314  # float   in
current_l1_in = 316  # float   dep
current_l2_in = 318  # float   dep
current_l3_in = 320  # float   dep
voltage_l1_l2_in = 322  # float   semi
voltage_l2_l3_in = 324  # float   semi
voltage_l3_l1_in = 326  # float   semi
frequency_in = 328  # float   semi
active_power_out = 330  # float   in
reactive_power_out = 332  # float   in
current_l1_out = 334  # float   dep
current_l2_out = 336  # float   dep
current_l3_out = 338  # float   dep
voltage_l1_l2_out = 340  # float   semi
voltage_l2_l3_out = 342  # float   semi
voltage_l3_l1_out = 344  # float   semi
frequency_out = 346  # float   semi
active_power_converter = 348  # float   dep
reactive_power_converter = 350  # float   dep

""" Battery State """
system_status = 352  # int    const
system_mode = 354  # int    const
accept_values = 110  # bool   const
converter_started = 111  # bool   in
input_connected = 112  # bool   in
system_on_backup_battery = 113  # bool   in
