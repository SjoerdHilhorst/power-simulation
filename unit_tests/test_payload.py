from battery.payload_handler import *
from pymodbus.datastore import ModbusSlaveContext, ModbusSequentialDataBlock
import unittest
from config.var_names import *


class TestPayload(unittest.TestCase):

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
        self.assertEqual(789.4375, BinaryPayloadDecoder.fromRegisters(
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
                             {'reg_type': CO, 'address': 7, 'encode': {'e_type': SCALE, 'd_type': FLOAT32}
                              },
                         'comb_32_float':
                             {'reg_type': CO, 'address': 8, 'encode': {'e_type': COMB, 'd_type': FLOAT32}
                              }},
                    'byte_order': '<',
                    'word_order': '<',
                    'default_scaling_factor': 1000}
        test_fields = test_env['fields']
        test_handler = PayloadHandler(test_env, test_store)
        test_builder = BinaryPayloadBuilder('<', '<')
        test_builder.reset()
        test_builder.add_8bit_int(100)
        test_store.setValues(1, 1, test_builder.to_registers())
        self.assertEqual(10,
                         test_handler.decode(1, 1, test_fields['scale_8_int']['encode']))
        test_builder.reset()
        test_builder.add_8bit_uint(100)
        test_store.setValues(1, 2, test_builder.to_registers())
        self.assertEqual(10,
                         test_handler.decode(1, 2, test_fields['scale_8_uint']['encode']))
        test_builder.reset()
        test_builder.add_16bit_int(1350)
        test_store.setValues(1, 3, test_builder.to_registers())
        self.assertEqual(13.5,
                         test_handler.decode(1, 3, test_fields['scale_16_int']['encode']))
        test_builder.reset()
        test_builder.add_16bit_uint(3287)
        test_store.setValues(1, 4, test_builder.to_registers())
        self.assertEqual(32.87,
                         test_handler.decode(1, 4, test_fields['scale_16_uint']['encode']))
        test_builder.reset()
        test_builder.add_32bit_int(1000)
        test_store.setValues(1, 5, test_builder.to_registers())
        self.assertEqual(1,
                         test_handler.decode(1, 5, test_fields['scale_32_int']['encode']))
        test_builder.reset()
        test_builder.add_32bit_uint(63200)
        test_store.setValues(1, 6, test_builder.to_registers())
        self.assertEqual(63.2,
                         test_handler.decode(1, 6, test_fields['scale_32_uint']['encode']))
        test_builder.reset()
        test_builder.add_32bit_float(1333)
        test_store.setValues(1, 7, test_builder.to_registers())
        self.assertEqual(1.333,
                         test_handler.decode(1, 7, test_fields['scale_32_float']['encode']))
        test_builder.reset()
        test_builder.add_32bit_float(789.4375)
        test_store.setValues(1, 8, test_builder.to_registers())
        self.assertEqual(789.4375,
                         test_handler.decode(1, 8, test_fields['comb_32_float']['encode']))
        test_builder.reset()

    def test_combo(self):
        test_store = ModbusSlaveContext(t=ModbusSequentialDataBlock.create())
        test_env = {'fields':
                        {'scale_8_int':
                             {'reg_type': CO, 'address': 1,
                              'encode': {'e_type': SCALE, 's_factor': 100, 'd_type': INT8}
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
        test_store.setValues(1, 1, test_handler.encode(1, test_fields['scale_8_int']['encode']))
        self.assertEqual(1, test_handler.decode(1, 1, test_fields['scale_8_int']['encode']))
        test_store.setValues(1, 2, test_handler.encode(10, test_fields['scale_8_uint']['encode']))
        self.assertEqual(10, test_handler.decode(1, 2, test_fields['scale_8_uint']['encode']))
        test_store.setValues(1, 3, test_handler.encode(12.5, test_fields['scale_16_int']['encode']))
        self.assertEqual(12.5, test_handler.decode(1, 3, test_fields['scale_16_int']['encode']))
        test_store.setValues(1, 4, test_handler.encode(32.991, test_fields['scale_16_uint']['encode']))
        self.assertEqual(32.99, test_handler.decode(1, 4, test_fields['scale_16_uint']['encode']))
        test_store.setValues(1, 5, test_handler.encode(1000, test_fields['scale_32_int']['encode']))
        self.assertEqual(1000, test_handler.decode(1, 5, test_fields['scale_32_int']['encode']))
        test_store.setValues(1, 6, test_handler.encode(63.2, test_fields['scale_32_int']['encode']))
        self.assertEqual(63.2, test_handler.decode(1, 6, test_fields['scale_32_int']['encode']))
        test_store.setValues(1, 7, test_handler.encode(1.333, test_fields['scale_32_float']['encode']))
        self.assertEqual(1.3, test_handler.decode(1, 7, test_fields['scale_32_float']['encode']))
        test_store.setValues(1, 8, test_handler.encode(789.4375, test_fields['comb_32_float']['encode']))
        self.assertEqual(789.4375, test_handler.decode(1, 8, test_fields['comb_32_float']['encode']))


if __name__ == '__main__':
    unittest.main()
