from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder
from config.var_names import *


class PayloadHandler:
    """
    encodes/decodes values according to the way it is stored in registry
    SCALE stands for multiplying/dividing by a scaling factor
    COMB stands for storing the value of one field in two registers
    """

    def __init__(self, env, store):
        self.byte_order = env["byte_order"]
        self.word_order = env["word_order"]
        self.d_s_factor = env["default_scaling_factor"]
        self.battery_store = store
        self.builder = BinaryPayloadBuilder(byteorder=self.byte_order, wordorder=self.word_order)

    def encode(self, value, encoding):
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
        if encoding['e_type'] == SCALE:
            encode_type[encoding['d_type']](round(value * encoding.get('s_factor', self.d_s_factor)))
        else:
            encode_type[encoding['d_type']](value)

        return self.builder.to_registers()

    def decode(self, fx, addr, encoding):
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
        if encoding['e_type'] == SCALE:
            return decode_type[encoding['d_type']]() / encoding.get('s_factor', self.d_s_factor)
        else:
            return decode_type[encoding['d_type']]()
