from battery.payload_handler import *
from pymodbus.datastore import ModbusSlaveContext, ModbusSequentialDataBlock
import unittest
from config.var_names import *


class TestUtil(unittest.TestCase):

    def test_encode(self):
        test_store = ModbusSlaveContext(t=ModbusSequentialDataBlock.create())
        test_env = {'fields':
                        {'scale_8_int':
                             {'reg_type': CO, 'address': 1,
                              'encode': {'e_type': SCALE, 's_factor': 10, 'd_type': INT8}
                              },
                         'scale_8_uint':
                             {'reg_type': CO, 'address': 2,
                              'encode': {'e_type': SCALE, 's_factor': 10, 'd_type': UINT8}
                              },
                         'scale_16_int':
                             {'reg_type': CO, 'address': 3,
                              'encode': {'e_type': SCALE, 's_factor': 100, 'd_type': INT16}
                              },
                         'scale_16_uint':
                             {'reg_type': CO, 'address': 4,
                              'encode': {'e_type': SCALE, 's_factor': 100, 'd_type': UINT16}
                              },
                         'scale_32_int':
                             {'reg_type': CO, 'address': 5, 'encode': {'e_type': SCALE, 'd_type': INT32}
                              },
                         'scale_32_uint':
                             {'reg_type': CO, 'address': 6, 'encode': {'e_type': SCALE, 'd_type': UINT32}
                              },
                         'scale_32_float':
                             {'reg_type': CO, 'address': 7,
                              'encode': {'e_type': SCALE, 's_factor': 10, 'd_type': FLOAT32}
                              },
                         'comb_32_float':
                             {'reg_type': CO, 'address': 8, 'encode': {'e_type': COMB, 'd_type': FLOAT32}
                              }},
                    'byte_order': '<',
                    'word_order': '<',
                    'default_scaling_factor': 1000}
        test_fields = test_env['fields']
        test_handler = PayloadHandler(test_env, test_store)
        self.assertEqual(100, BinaryPayloadDecoder.fromRegisters(
            test_handler.encode(10, test_fields['scale_8_int']['encode']),
            byteorder='<', wordorder='<').decode_8bit_int())
        self.assertEqual(100, BinaryPayloadDecoder.fromRegisters(
            test_handler.encode(10, test_fields['scale_8_uint']['encode']),
            byteorder='<', wordorder='<').decode_8bit_uint())
        self.assertEqual(1250, BinaryPayloadDecoder.fromRegisters(
            test_handler.encode(12.5, test_fields['scale_16_int']['encode']),
            byteorder='<', wordorder='<').decode_16bit_int())
        self.assertEqual(3299, BinaryPayloadDecoder.fromRegisters(
            test_handler.encode(32.991, test_fields['scale_16_uint']['encode']),
            byteorder='<', wordorder='<').decode_16bit_uint())
        self.assertEqual(1000000, BinaryPayloadDecoder.fromRegisters(
            test_handler.encode(1000, test_fields['scale_32_int']['encode']),
            byteorder='<', wordorder='<').decode_32bit_int())
        self.assertEqual(63200, BinaryPayloadDecoder.fromRegisters(
            test_handler.encode(63.2, test_fields['scale_32_uint']['encode']),
            byteorder='<', wordorder='<').decode_32bit_uint())
        self.assertEqual(13, BinaryPayloadDecoder.fromRegisters(
            test_handler.encode(1.333, test_fields['scale_32_float']['encode']),
            byteorder='<', wordorder='<').decode_32bit_float())
        self.assertAlmostEqual(789.4375, BinaryPayloadDecoder.fromRegisters(
            test_handler.encode(789.4375, test_fields['comb_32_float']['encode']),
            byteorder='<', wordorder='<').decode_32bit_float())

    def test_decode(self):
        test_store = ModbusSlaveContext(t=ModbusSequentialDataBlock.create())
        test_env = {'fields':
                        {'scale_8_int':
                             {'reg_type': CO, 'address': 1,
                              'encode': {'e_type': SCALE, 's_factor': 10, 'd_type': INT8}
                              },
                         'scale_8_uint':
                             {'reg_type': CO, 'address': 2,
                              'encode': {'e_type': SCALE, 's_factor': 10, 'd_type': UINT8}
                              },
                         'scale_16_int':
                             {'reg_type': CO, 'address': 3,
                              'encode': {'e_type': SCALE, 's_factor': 100, 'd_type': INT16}
                              },
                         'scale_16_uint':
                             {'reg_type': CO, 'address': 4,
                              'encode': {'e_type': SCALE, 's_factor': 100, 'd_type': UINT16}
                              },
                         'scale_32_int':
                             {'reg_type': CO, 'address': 5, 'encode': {'e_type': SCALE, 'd_type': INT32}
                              },
                         'scale_32_uint':
                             {'reg_type': CO, 'address': 6, 'encode': {'e_type': SCALE, 'd_type': UINT32}
                              },
                         'scale_32_float':
                             {'reg_type': CO, 'address': 7,
                              'encode': {'e_type': SCALE, 's_factor': 10, 'd_type': FLOAT32}
                              },
                         'comb_32_float':
                             {'reg_type': CO, 'address': 8, 'encode': {'e_type': COMB, 'd_type': FLOAT32}
                              }},
                    'byte_order': '<',
                    'word_order': '<',
                    'default_scaling_factor': 1000}
        test_fields = test_env['fields']
        test_handler = PayloadHandler(test_env, test_store)

    def test_combo(self):
        test_store = ModbusSlaveContext(t=ModbusSequentialDataBlock.create())
        test_env = {'fields':
                        {'scale_8_int':
                             {'reg_type': CO, 'address': 1,
                              'encode': {'e_type': SCALE, 's_factor': 10, 'd_type': INT8}
                              },
                         'scale_8_uint':
                             {'reg_type': CO, 'address': 2,
                              'encode': {'e_type': SCALE, 's_factor': 10, 'd_type': UINT8}
                              },
                         'scale_16_int':
                             {'reg_type': CO, 'address': 3,
                              'encode': {'e_type': SCALE, 's_factor': 100, 'd_type': INT16}
                              },
                         'scale_16_uint':
                             {'reg_type': CO, 'address': 4,
                              'encode': {'e_type': SCALE, 's_factor': 100, 'd_type': UINT16}
                              },
                         'scale_32_int':
                             {'reg_type': CO, 'address': 5, 'encode': {'e_type': SCALE, 'd_type': INT32}
                              },
                         'scale_32_uint':
                             {'reg_type': CO, 'address': 6, 'encode': {'e_type': SCALE, 'd_type': UINT32}
                              },
                         'scale_32_float':
                             {'reg_type': CO, 'address': 7,
                              'encode': {'e_type': SCALE, 's_factor': 10, 'd_type': FLOAT32}
                              },
                         'comb_32_float':
                             {'reg_type': CO, 'address': 8, 'encode': {'e_type': COMB, 'd_type': FLOAT32}
                              }},
                    'byte_order': '<',
                    'word_order': '<',
                    'default_scaling_factor': 1000}
        test_fields = test_env['fields']
        test_handler = PayloadHandler(test_env, test_store)


if __name__ == '__main__':
    unittest.main()
