from config.var_names import *

env = {
    # address of modbus server
    'server_address': ['localhost', 5030],

    # first index is function code, second index is address, third is type of float storage (applicable for holding
    # and input registers)
    'fields': {
        'soc': {'reg_type': holding, 'address': 10, 'encode': [scale, INT32]},
        'active_power_in': {'reg_type': holding, 'address': 12, 'encode': [scale, FLOAT32]},
        'reactive_power_in': {'reg_type': holding, 'address': 14, 'encode': [scale, FLOAT32]},
        'current_l1_in': {'reg_type': holding, 'address': 16, 'encode': [comb, FLOAT32]},
        'current_l2_in': {'reg_type': holding, 'address': 18, 'encode': [comb, FLOAT32]},
        'current_l3_in': {'reg_type': holding, 'address': 20, 'encode': [scale, FLOAT32]},
        'voltage_l1_l2_in': {'reg_type': holding, 'address': 22, 'encode': [comb, FLOAT32]},
        'voltage_l2_l3_in': {'reg_type': holding, 'address': 24, 'encode': [comb, FLOAT32]},
        'voltage_l3_l1_in': {'reg_type': holding, 'address': 26, 'encode': [scale, FLOAT32]},
        'frequency_in': {'reg_type': holding, 'address': 28, 'encode': [scale, INT32]},
        'active_power_out': {'reg_type': holding, 'address': 30, 'encode': [scale, FLOAT32]},
        'reactive_power_out': {'reg_type': holding, 'address': 32, 'encode': [comb, FLOAT32]},
        'current_l1_out': {'reg_type': holding, 'address': 34, 'encode': [comb, FLOAT32]},
        'current_l2_out': {'reg_type': holding, 'address': 36, 'encode': [scale, FLOAT32]},
        'current_l3_out': {'reg_type': holding, 'address': 38, 'encode': [comb, FLOAT32]},
        'voltage_l1_l2_out': {'reg_type': holding, 'address': 40, 'encode': [scale, FLOAT32]},
        'voltage_l2_l3_out': {'reg_type': holding, 'address': 42, 'encode': [comb, FLOAT32]},
        'voltage_l3_l1_out': {'reg_type': holding, 'address': 44, 'encode': [scale, FLOAT32]},
        'frequency_out': {'reg_type': holding, 'address': 46, 'encode': [comb, INT16]},
        'active_power_converter': {'reg_type': holding, 'address': 48, 'encode': [scale, FLOAT32]},
        'reactive_power_converter': {'reg_type': holding, 'address': 50, 'encode': [scale, FLOAT32]},

        'system_status': {'reg_type': holding, 'address': 52, 'encode': [scale, INT16]},
        'system_mode': {'reg_type': holding, 'address': 54, 'encode': [scale, INT16]},
        'accept_values': {'reg_type': holding, 'address': 10, 'encode': [scale, INT8]},
        'converter_started': {'reg_type': coil, 'address': 11, 'encode': [scale, INT8]},
        'input_connected': {'reg_type': coil, 'address': 12, 'encode': [scale, INT8]},
        'system_on_backup_battery': {'reg_type': coil, 'address': 13, 'encode': [scale, INT8]},

        'custom': {'reg_type': holding, 'address': 58, 'encode': [comb, INT32]},
        'custom1': {'reg_type': holding, 'address': 70, 'encode': [comb, INT32]},

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

    # a pair should be provided in a format field_name: csv_name (csv is stores in folders csvs)
    'from_csv': {
        'active_power_in': 'historic_battery_data2',
        'reactive_power_out': 'historic_battery_data'
    },

    # realtime delay in sec between iteration, set to 0 for no delay
    'update_delay': 0.1,

    # max number of iterations before simulation stops, set to None if infinite iterations
    # overridden by number of rows for historic sim
    'max_iterations': 50000,

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
            "soc",
            "custom",
            "custom1"
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
