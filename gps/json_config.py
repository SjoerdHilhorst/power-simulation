import json

def get_data(addr=None):
    """
    Gets the addresses for the simulation/client/battery
    If addr has a variable then it will get the custom json of that pathname
    """
    if addr:
        address = get_custom_json(addr)
    else:
        address = get_default()
    return address

def get_default():
    """
    returns the default json as a dictionary
    """
    with open('config/default.json') as f:
        address = json.load(f)
    return address

def get_custom_json(addr):
    """
    returns a custom json as a dictionary
    addr: should not include path or .json, e.g. filename : 'my_custom_addresses'
    """
    with open('config/' + addr + '.json') as f:
        address = json.load(f)
    return address

def set_custom_json(filename, fx_addr_separator, server_adress, id, sim_type, float_mode, word_order, byte_order, scaling_factor, addresses):
    """
        Fill a json with custom addresses, note: byte_order and word_order should be stored with 'Endian.Big'
        or 'Endian.Little' from 'from pymodbus.payload import Endian'.
        File name should not include the path o .json, e.g. filename : 'my_custom_addresses'
    """
    config_dict = {

        "server_address": list(server_adress),
        "id": id,
        "simulation_type": sim_type,


        'BATTERY_DATA_VARS': 21,
        'BATTERY_STATE_VARS': 6,

        'fx_addr_separator': fx_addr_separator,

        'float_mode': float_mode,
        'word_order': word_order,
        'byte_order': byte_order,
        'scaling_factor': scaling_factor,

        'address': {
            'soc': addresses[0],
            'active_power_in': addresses[1],
            'reactive_power_in': addresses[2],
            'current_l1_in': addresses[3],
            'current_l2_in': addresses[4],
            'current_l3_in': addresses[5],
            'voltage_l1_l2_in': addresses[6],
            'voltage_l2_l3_in': addresses[7],
            'voltage_l3_l1_in': addresses[8],
            'frequency_in': addresses[9],
            'active_power_out': addresses[10],
            'reactive_power_out': addresses[11],
            'current_l1_out': addresses[12],
            'current_l2_out': addresses[13],
            'current_l3_out': addresses[14],
            'voltage_l1_l2_out': addresses[15],
            'voltage_l2_l3_out': addresses[16],
            'voltage_l3_l1_out': addresses[17],
            'frequency_out': addresses[18],
            'active_power_converter': addresses[19],
            'reactive_power_converter': addresses[20],

            'system_status': addresses[21],
            'system_mode': addresses[22],
            'accept_values': addresses[23],
            'converter_started': addresses[24],
            'input_connected': addresses[25],
            'system_on_backup_battery': addresses[26]
        }
    }

    with open('config/' + filename + '.json', 'w', encoding='utf-8') as json_file:
        json.dump(config_dict, json_file, ensure_ascii=False, indent=4)
