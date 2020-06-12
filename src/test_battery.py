import unittest
from server.battery import Battery
from config.var_names import *


class TestBattery(unittest.TestCase):

    def test_get_value(self):
        test_env = {
            'server_address': ['localhost', 5030],
            'id': 'GREENER_TEST_001',
            'battery_capacity': 330,
            'fields': {
                'system_status_test':
                    {'reg_type': HR, 'address': 52, 'encode': {'e_type': SCALE, 'd_type': INT16}, 'init': 0},
                'accept_values_test':
                    {'reg_type': HR, 'address': 10, 'encode': {'e_type': SCALE, 's_factor': 1, 'd_type': INT8}, 'init': 2},
                'input_connected_test':
                    {'reg_type': CO, 'address': 12, 'encode': {'e_type': SCALE, 's_factor': 1, 'd_type': INT8}, 'init': 1},
            },
            'float_store': {
                # only used for SCALE, increase for more precision
                'default_scaling_factor': 1000,
                # Defines Endianness in modbus register,  '>' is Big Endian, '<' is Little Endian
                'word_order': '>',
                'byte_order': '>',
            },
        }
        test_battery = Battery(test_env)
        self.assertEqual(test_battery.get_value(test_battery.fields['system_status_test']), 0)
        self.assertEqual(test_battery.get_value(test_battery.fields['accept_values_test']), 2)
        self.assertEqual(test_battery.get_value(test_battery.fields['input_connected_test']), 1)

    def test_set_value(self):
        test_env = {
            'server_address': ['localhost', 5040],
            'id': 'GREENER_TEST_002',
            'battery_capacity': 330,
            'fields': {
                'system_status_test':
                    {'reg_type': HR, 'address': 52, 'encode': {'e_type': SCALE, 'd_type': INT16}, 'init': 0},
                'accept_values_test':
                    {'reg_type': HR, 'address': 10, 'encode': {'e_type': SCALE, 's_factor': 1, 'd_type': INT8},
                     'init': 2},
                'input_connected_test':
                    {'reg_type': CO, 'address': 12, 'encode': {'e_type': SCALE, 's_factor': 1, 'd_type': INT8},
                     'init': 1},
            },
            'float_store': {
                # only used for SCALE, increase for more precision
                'default_scaling_factor': 1000,
                # Defines Endianness in modbus register,  '>' is Big Endian, '<' is Little Endian
                'word_order': '>',
                'byte_order': '>',
            },
        }
        test_battery = Battery(test_env)
        test_battery.set_value(test_battery.fields['system_status_test'], 1)
        test_battery.set_value(test_battery.fields['accept_values_test'], 50)
        test_battery.set_value(test_battery.fields['input_connected_test'], 0)
        self.assertEqual(1, test_battery.get_value(test_battery.fields['system_status_test']))
        self.assertEqual(50, test_battery.get_value(test_battery.fields['accept_values_test']))
        self.assertEqual(0, test_battery.get_value(test_battery.fields['input_connected_test']))

    def test_is_input_connected(self):
        test_env = {
            'server_address': ['localhost', 5050],
            'id': 'GREENER_TEST_003',
            'battery_capacity': 330,
            'fields': {
                'input_connected':
                    {'reg_type': CO, 'address': 12, 'encode': {'e_type': SCALE, 's_factor': 1, 'd_type': INT8},
                     'init': 1},
            },
            'float_store': {
                # only used for SCALE, increase for more precision
                'default_scaling_factor': 1000,
                # Defines Endianness in modbus register,  '>' is Big Endian, '<' is Little Endian
                'word_order': '>',
                'byte_order': '>',
            },
        }
        test_battery = Battery(test_env)
        self.assertTrue(test_battery.is_input_connected())
        test_battery.set_value(test_battery.fields['input_connected'], 0)
        self.assertFalse(test_battery.is_input_connected())

    def test_is_converter_started(self):
        test_env = {
            'server_address': ['localhost', 5060],
            'id': 'GREENER_TEST_004',
            'battery_capacity': 330,
            'fields': {
                'converter_started':
                    {'reg_type': CO, 'address': 11, 'encode': {'e_type': SCALE, 's_factor': 1, 'd_type': INT8},
                     'init': 1},
            },
            'float_store': {
                # only used for SCALE, increase for more precision
                'default_scaling_factor': 1000,
                # Defines Endianness in modbus register,  '>' is Big Endian, '<' is Little Endian
                'word_order': '>',
                'byte_order': '>',
            },
        }
        test_battery = Battery(test_env)
        self.assertTrue(test_battery.is_converter_started())
        test_battery.set_value(test_battery.fields['converter_started'], 0)
        self.assertFalse(test_battery.is_converter_started())

    def test_set_initial_values(self):
        test_env = {
            'server_address': ['localhost', 5070],
            'id': 'GREENER_TEST_004',
            'battery_capacity': 330,
            'fields': {
                'converter_started':
                    {'reg_type': CO, 'address': 11, 'encode': {'e_type': SCALE, 's_factor': 1, 'd_type': INT8},
                     'init': 1},
                'input_connected':
                    {'reg_type': CO, 'address': 12, 'encode': {'e_type': SCALE, 's_factor': 1, 'd_type': INT8},
                     'init': 1},
                'system_status':
                    {'reg_type': HR, 'address': 52, 'encode': {'e_type': SCALE, 'd_type': INT16}, 'init': 1},
                'system_mode':
                    {'reg_type': HR, 'address': 54, 'encode': {'e_type': SCALE, 'd_type': INT16}, 'init': 5},
                'system_on_backup_battery':
                    {'reg_type': CO, 'address': 13, 'encode': {'e_type': SCALE, 's_factor': 1, 'd_type': INT8},
                     'init': 1},
                'soc':
                    {'reg_type': HR, 'address': 10, 'encode': {'e_type': SCALE, 'd_type': INT32}, 'init': 5.2},
                'custom':
                    {'reg_type': HR, 'address': 58, 'encode': {'e_type': COMB, 'd_type': FLOAT32}, 'init': 1500},
            },
            'float_store': {
                # only used for SCALE, increase for more precision
                'default_scaling_factor': 1000,
                # Defines Endianness in modbus register,  '>' is Big Endian, '<' is Little Endian
                'word_order': '>',
                'byte_order': '>',
            },
        }
        test_battery = Battery(test_env)
        test_battery.set_initial_values()
        self.assertEqual(5.2, test_battery.get_value(test_battery.fields['soc']))
        self.assertEqual(1, test_battery.get_value(test_battery.fields['system_status']))
        self.assertEqual(5, test_battery.get_value(test_battery.fields['system_mode']))
        self.assertEqual(1, test_battery.get_value(test_battery.fields['converter_started']))
        self.assertEqual(1, test_battery.get_value(test_battery.fields['input_connected']))
        self.assertEqual(1, test_battery.get_value(test_battery.fields['system_on_backup_battery']))
        self.assertEqual(1500, test_battery.get_value(test_battery.fields['custom']))


if __name__ == '__main__':
    unittest.main()

