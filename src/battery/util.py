from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder
from src.config.var_names import *

class FloatHandler:
    """
    encodes/decodes float according to the way it is stored in registry
    SCALE stands for multiplying/dividing by scaling factor method, I.E. 32bit int
    COMB stands for storing the float in two registers, I.E. 32bit float
    """

    def __init__(self, env, store):
        self.byte_order = env["byte_order"]
        self.word_order = env["word_order"]
        self.d_s_factor = env["default_scaling_factor"]
        self.battery_store = store
        self.builder = BinaryPayloadBuilder(byteorder=self.byte_order, wordorder=self.word_order)

    def encode_float(self, value, mode):
        self.builder.reset()
        encode_type = {
            INT8: lambda x: self.builder.add_8bit_int(x),
            UINT8: lambda x: self.builder.add_8bit_uint(x),
            INT16: lambda x: self.builder.add_16bit_int(x),
            UINT16: lambda x: self.builder.add_16bit_uint(x),
            INT32: lambda x: self.builder.add_32bit_int(x),
            UINT32: lambda x: self.builder.add_32bit_uint(x),
            FLOAT32: lambda x: self.builder.add_32bit_float(x),
        }
        if mode['e_type'] == scale:
            encode_type[mode['d_type']](round(value * mode.get('s_factor', self.d_s_factor)))
        else:
            encode_type[mode['d_type']](value)
        return self.builder.to_registers()

    def decode_float(self, fx, addr, mode):
        encoded_value = self.battery_store.getValues(fx, addr, 2)
        decoder = BinaryPayloadDecoder.fromRegisters(encoded_value, byteorder=self.byte_order,
                                                     wordorder=self.word_order)
        decode_type = {
            INT8: lambda: decoder.decode_8bit_int(),
            UINT8: lambda: decoder.decode_8bit_uint(),
            INT16: lambda: decoder.decode_16bit_int(),
            UINT16: lambda: decoder.decode_16bit_uint(),
            INT32: lambda: decoder.decode_32bit_int(),
            UINT32: lambda: decoder.decode_32bit_uint(),
            FLOAT32: lambda: decoder.decode_32bit_float(),
        }
        if mode['e_type'] == scale:
            return decode_type[mode['d_type']]() / mode.get('s_factor', self.d_s_factor)
        else:
            return decode_type[mode['d_type']]()
