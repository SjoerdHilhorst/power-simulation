from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder


class FloatHandler:
    """
    encodes/decodes float according to the way it is stored in registry
    SCALE stands for multiplying/dividing by scaling factor method, I.E. 32bit int
    COMB stands for storing the float in two registers, I.E. 32bit float
    """

    def __init__(self, env, store):
        self.byte_order = env["byte_order"]
        self.word_order = env["word_order"]
        self.scaling_factor = env["scaling_factor"]
        self.battery_store = store
        self.builder = BinaryPayloadBuilder(byteorder=self.byte_order, wordorder=self.word_order)

    def encode_float(self, value, mode):
        self.builder.reset()
        encode_type = {
            'int8': lambda x: self.builder.add_8bit_int(x),
            'uint8': lambda x: self.builder.add_8bit_uint(x),
            'int16': lambda x: self.builder.add_16bit_int(x),
            'uint16': lambda x: self.builder.add_16bit_uint(x),
            'int32': lambda x: self.builder.add_32bit_int(x),
            'uint32': lambda x: self.builder.add_32bit_uint(x),
            'float32': lambda x: self.builder.add_32bit_float(x),
        }
        if mode[0] == "SCALE" and mode[1] != 'int8':
            encode_type[mode[1]](round(value * self.scaling_factor))
        else:
            encode_type[mode[1]](value)
        return self.builder.to_registers()

    def decode_float(self, fx, addr, mode):
        encoded_value = self.battery_store.getValues(fx, addr, 2)
        decoder = BinaryPayloadDecoder.fromRegisters(encoded_value, byteorder=self.byte_order,
                                                     wordorder=self.word_order)
        decode_type = {
            'int8': lambda: decoder.decode_8bit_int(),
            'uint8': lambda: decoder.decode_8bit_uint(),
            'int16': lambda: decoder.decode_16bit_int(),
            'uint16': lambda: decoder.decode_16bit_uint(),
            'int32': lambda: decoder.decode_32bit_int(),
            'uint32': lambda: decoder.decode_32bit_uint(),
            'float32': lambda: decoder.decode_32bit_float(),
        }
        if mode[0] == "SCALE" and mode[1] != 'int8':
            return decode_type[mode[1]]() / self.scaling_factor
        else:
            return decode_type[mode[1]]()
