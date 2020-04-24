from math import sin
from config.update_functions import *

env = {
    # address of modbus server
    'server_address': ['localhost', 5030],
    # simulation type must be 'historic' 'random' 'simulation'
    'simulation_type': 'simulation',

    # historic simulation will read I/O power from a user specified csv
    # random simulation will generate random I/O power from user defined ranges
    # simulation will generate I/O power from user defined functions

    # realtime delay in sec between iteration, set to 0 for no delay
    'update_delay': 0.001,

    # max number of iterations before simulation stops, set to None if infinite iterations
    # overriden by number of rows for historic sim
    'max_iterations': 50000,

    'battery_constants': {
        'system_status': 1,
        'system_mode': 5,
        'system_on_backup_battery': 1,
        'accept_values': 1,
        'battery_capacity': 330,
        'id': 'GREENER_001',
    },

    # show a realtime graph of battery fields
    # it is adviced to set update_delay to at least 0.01 for smoothness
    'graph': {
        'enabled': True,
        # define which fields you want to plot
        'fields': [
            "active_power_in",
            "active_power_out",
            "reactive_power_in",
            "reactive_power_out",
            "frequency_in",
            "soc"
        ]
    },

    # for debugging purposes
    'database': {
        # disable for better performance
        'enabled': False,
        'db_name': 'power_simulation',
        'drop_table_on_start': True
    },


    'float_store': {
        # COMB for 2 register float storage or SCALE for storing floats with scaling factor
        'float_mode': 'COMB',
        # only used for SCALE, increase for more precision
        'scaling_factor': 1000,
        # Defines Endianness in modbus register,  '>' is Big Endian, '<' is Little Endian
        'word_order': '>',
        'byte_order': '>',
    },

    # only used for random simulation
    # define the ranges in where the random values should be
    'random_simulation': {
        'start_soc': 50.0,
        'range_active_power_in': [0, 200],
        'range_reactive_power_in': [-65, 185],
        'range_active_power_out': [0, 200],
        'range_reactive_power_out': [-65, 185]
    },

    # only used for a historic simulation
    # the csv_name is without .csv
    'historic_simulation': {
        'csv_name': 'historic_battery_data',
        'start_index': 0,
    },

    # only used for simulation
    # define update functions for user inputs as lambda function, always have one argument (t)
    # for example to do a constant: lambda t: 400
    # you can also define more complex functions in update_functions and import them here
    'simulation': {
        'start_soc': 72.2,
        'active_power_in': lambda t: 0.001*quadratic(1,2,3,t),
        'reactive_power_in': lambda t: 200 * sin(t),

        # my_fun and sine are imported from update functions
        'active_power_out': lambda t: 200 * sin(t),
        'reactive_power_out': lambda t: quadratic(1,2,3, t)
    },

    # first index is function code, second index is address
    'address': {
        'soc': [3, 10],
        'active_power_in': [3, 12],
        'reactive_power_in': [3, 14],
        'current_l1_in': [3, 16],
        'current_l2_in': [3, 18],
        'current_l3_in': [3, 20],
        'voltage_l1_l2_in': [3, 22],
        'voltage_l2_l3_in': [3, 24],
        'voltage_l3_l1_in': [3, 26],
        'frequency_in': [3, 28],
        'active_power_out': [3, 30],
        'reactive_power_out': [3, 32],
        'current_l1_out': [3, 34],
        'current_l2_out': [3, 36],
        'current_l3_out': [3, 38],
        'voltage_l1_l2_out': [3, 40],
        'voltage_l2_l3_out': [3, 42],
        'voltage_l3_l1_out': [3, 44],
        'frequency_out': [3, 46],
        'active_power_converter': [3, 48],
        'reactive_power_converter': [3, 50],
        'system_status': [3, 52],
        'system_mode': [3, 54],
        'accept_values': [1, 10],
        'converter_started': [1, 11],
        'input_connected': [1, 12],
        'system_on_backup_battery': [1, 13]}
}
