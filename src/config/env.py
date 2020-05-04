from config.update_functions import *
from config.var_names import *

env = {
    # address of modbus server
    'server_address': ['localhost', 5030],

    # first index is function code, second index is address, third is type of float storage (applicable for holding
    # and input registers)
    'fields': {
        'soc': [holding, 10, scale],
        'active_power_in': [holding, 12, scale],
        'reactive_power_in': [holding, 14, scale],
        'current_l1_in': [holding, 16, comb],
        'current_l2_in': [holding, 18, comb],
        'current_l3_in': [holding, 20, scale],
        'voltage_l1_l2_in': [holding, 22, comb],
        'voltage_l2_l3_in': [holding, 24, comb],
        'voltage_l3_l1_in': [holding, 26, scale],
        'frequency_in': [holding, 28, scale],
        'active_power_out': [holding, 30, scale],
        'reactive_power_out': [holding, 32, comb],
        'current_l1_out': [holding, 34, comb],
        'current_l2_out': [holding, 36, scale],
        'current_l3_out': [holding, 38, comb],
        'voltage_l1_l2_out': [holding, 40, scale],
        'voltage_l2_l3_out': [holding, 42, comb],
        'voltage_l3_l1_out': [holding, 44, scale],
        'frequency_out': [holding, 46, comb],
        'active_power_converter': [holding, 48, scale],
        'reactive_power_converter': [holding, 50, scale],

        'system_status': [holding, 52, scale],
        'system_mode': [holding, 54, scale],
        'accept_values': [coil, 10],
        'converter_started': [coil, 11],
        'input_connected': [coil, 12],
        'system_on_backup_battery': [coil, 13]
    },

    'float_store': {
        # only used for SCALE, increase for more precision
        'scaling_factor': 1000,
        # Defines Endianness in modbus register,  '>' is Big Endian, '<' is Little Endian
        'word_order': '>',
        'byte_order': '>',
    },

    'battery_constants': {
        'system_status': 1,
        'system_mode': 5,
        'system_on_backup_battery': 1,
        'accept_values': 1,
        'converter_started': 1,
        'input_connected': 1,
        'battery_capacity': 330,
        'id': 'GREENER_001',
    },

    # initial soc
    'soc': 72.2,

    # simulation type must be 'historic' or 'simulation'
    # historic simulation will read I/O power from a user specified csv
    # simulation will generate I/O power from user defined functions
    'simulation_type': 'historic',

    # realtime delay in sec between iteration, set to 0 for no delay
    'update_delay': 0.1,

    # max number of iterations before simulation stops, set to None if infinite iterations
    # overridden by number of rows for historic sim
    'max_iterations': 50000,

    # only used for a historic simulation
    # the csv must be located in the power-simulation folder
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
        'active_power_in': lambda t: 0.001 * quadratic(1, 2, 3, t),
        'reactive_power_in': lambda t: 200 * sin(t),

        # my_fun and sine are imported from update functions
        'active_power_out': lambda t: 200 * sin(t),
        'reactive_power_out': lambda t: quadratic(1, 2, 3, t)
    },

    # show a realtime graph of battery fields
    # it is advised to set update_delay to at least 0.01 for smoothness
    'graph': {
        'enabled': True,
        # define which fields you want to plot
        'fields': [
            "active_power_in",
            "active_power_out",
            "reactive_power_in",
            "reactive_power_out",
            "active_power_converter",
            "reactive_power_converter",
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

}
