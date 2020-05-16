from config.var_names import *

env = {

    # Device information
    'server_address': ['localhost', 5030],
    'id': 'GREENER_001',
    'battery_capacity': 330,

    # Simulation parameters

    # realtime delay in sec between iterations (set to 0 for no delay)
    'update_delay': 0.1,

    # max number of iterations before simulation stops (set to None for infinite iterations)
    # overridden by number of rows if csv is used
    'max_iterations': 5000,


    # Map of the registers of the form "field_name": configuration:
    #           * reg_type: type of the register (coil/discrete input/holding register/input register)
    #           * address: actual address
    #           * encode:
    #               - e_type: encoding type (SCALE/COMB)
    #               - s_factor: scaling factor (optional)
    #               - d_type: data type ((U)INT8, (U)INT16, (U)INT32, FLOAT32)
    #           * init: initial value (optional)

    'fields': {
        'active_power_in':
            {'reg_type': HOLD_REG, 'address': 12, 'encode': {'e_type': SCALE, 'd_type': FLOAT32}},
        'reactive_power_in':
            {'reg_type': HOLD_REG, 'address': 14, 'encode': {'e_type': SCALE, 'd_type': FLOAT32}},
        'current_l1_in':
            {'reg_type': HOLD_REG, 'address': 16, 'encode': {'e_type': COMB, 'd_type': FLOAT32}},
        'current_l2_in':
            {'reg_type': HOLD_REG, 'address': 18, 'encode': {'e_type': COMB, 'd_type': FLOAT32}},
        'current_l3_in':
            {'reg_type': HOLD_REG, 'address': 20, 'encode': {'e_type': SCALE, 'd_type': FLOAT32}},
        'voltage_l1_l2_in':
            {'reg_type': HOLD_REG, 'address': 22, 'encode': {'e_type': COMB, 'd_type': FLOAT32}},
        'voltage_l2_l3_in':
            {'reg_type': HOLD_REG, 'address': 24, 'encode': {'e_type': COMB, 'd_type': FLOAT32}},
        'voltage_l3_l1_in':
            {'reg_type': HOLD_REG, 'address': 26, 'encode': {'e_type': SCALE, 'd_type': FLOAT32}},
        'frequency_in':
            {'reg_type': HOLD_REG, 'address': 28, 'encode': {'e_type': SCALE, 'd_type': INT32}},
        'active_power_out':
            {'reg_type': HOLD_REG, 'address': 30, 'encode': {'e_type': SCALE, 'd_type': FLOAT32}},
        'reactive_power_out':
            {'reg_type': HOLD_REG, 'address': 32, 'encode': {'e_type': COMB, 'd_type': FLOAT32}},
        'current_l1_out':
            {'reg_type': HOLD_REG, 'address': 34, 'encode': {'e_type': COMB, 'd_type': FLOAT32}},
        'current_l2_out':
            {'reg_type': HOLD_REG, 'address': 36, 'encode': {'e_type': SCALE, 'd_type': FLOAT32}},
        'current_l3_out':
            {'reg_type': HOLD_REG, 'address': 38, 'encode': {'e_type': COMB, 'd_type': FLOAT32}},
        'voltage_l1_l2_out':
            {'reg_type': HOLD_REG, 'address': 40, 'encode': {'e_type': SCALE, 'd_type': FLOAT32}},
        'voltage_l2_l3_out':
            {'reg_type': HOLD_REG, 'address': 42, 'encode': {'e_type': COMB, 'd_type': FLOAT32}},
        'voltage_l3_l1_out':
            {'reg_type': HOLD_REG, 'address': 44, 'encode': {'e_type': SCALE, 'd_type': FLOAT32}},
        'frequency_out':
            {'reg_type': HOLD_REG, 'address': 46, 'encode': {'e_type': COMB, 'd_type': FLOAT32}},
        'active_power_converter':
            {'reg_type': HOLD_REG, 'address': 48, 'encode': {'e_type': SCALE, 'd_type': FLOAT32}},
        'reactive_power_converter':
            {'reg_type': HOLD_REG, 'address': 50, 'encode': {'e_type': SCALE, 'd_type': FLOAT32}},


        'system_status':
            {'reg_type': HOLD_REG, 'address': 52, 'encode': {'e_type': SCALE, 'd_type': INT16}, 'init': 1},
        'system_mode':
            {'reg_type': HOLD_REG, 'address': 54, 'encode': {'e_type': SCALE, 'd_type': INT16}, 'init': 5},
        'accept_values':
            {'reg_type': HOLD_REG, 'address': 10, 'encode': {'e_type': SCALE, 's_factor': 1, 'd_type': INT8},
             'init': 1},
        'converter_started':
            {'reg_type': COIL, 'address': 11, 'encode': {'e_type': SCALE, 's_factor': 1, 'd_type': INT8}, 'init': 1},
        'input_connected':
            {'reg_type': COIL, 'address': 12, 'encode': {'e_type': SCALE, 's_factor': 1, 'd_type': INT8}, 'init': 1},
        'system_on_backup_battery':
            {'reg_type': COIL, 'address': 13, 'encode': {'e_type': SCALE, 's_factor': 1, 'd_type': INT8}, 'init': 1},
        'soc':
            {'reg_type': HOLD_REG, 'address': 10, 'encode': {'e_type': SCALE, 'd_type': INT32}, 'init': 72.2},


        'custom':
            {'reg_type': HOLD_REG, 'address': 58, 'encode': {'e_type': COMB, 'd_type': FLOAT32}, 'init': 200},
        'custom1':
            {'reg_type': HOLD_REG, 'address': 70, 'encode': {'e_type': COMB, 'd_type': FLOAT32}, 'init': 100},

    },

    'float_store': {
        # only used for SCALE, increase for more precision
        'default_scaling_factor': 1000,
        # Defines Endianness in modbus register,  '>' is Big Endian, '<' is Little Endian
        'word_order': '>',
        'byte_order': '>',
    },

    # a pair should be provided in a format field_name: csv_name (csv is stores in folders csvs)
    'from_csv': {
        'active_power_in': 'historic_battery_data',
        'reactive_power_in': 'historic_battery_data',
        'active_power_out': 'historic_battery_data',
        'reactive_power_out': 'historic_battery_data',
    },



    # show a realtime graph of battery fields
    'graph': {
        'enabled': True,
        # define which fields to plot
        'fields': [
            "active_power_in",
            "active_power_out",
            "reactive_power_in",
            "reactive_power_out",
            "soc",
            "custom",
        ]
    },

    # for debugging purposes
    'database': {
        # disable for better performance
        'enabled': True,
        'db_name': 'power_simulation',
        'drop_table_on_start': True
    },

}
