from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder


class FloatHandler:
    """
    encodes/decodes float according to the way it is stored in registry
    SCALE stands for multiplying/dividing by scaling factor method, I.E. 32bit int
    COMB stands for storing the float in two registers, I.E. 32bit float
    :param value: float which should be handled
    :param mode: "SCALE" or "COMB"
    :return: float rounded to integer
    """

    def __init__(self, env, store):
        self.byte_order = env["byte_order"]
        self.word_order = env["word_order"]
        self.scaling_factor = env["scaling_factor"]
        self.battery_store = store
        self.builder = BinaryPayloadBuilder(byteorder=self.byte_order, wordorder=self.word_order)

    def encode_float(self, value, mode):
        if mode == "SCALE":
            self.builder.reset()
            self.builder.add_32bit_int((round(value * self.scaling_factor)))
        else:
            self.builder.reset()
            self.builder.add_32bit_float(value)
        return self.builder.to_registers()

    def decode_float(self, fx, addr, mode):
        if mode == "SCALE":
            encoded_value = self.battery_store.getValues(fx, addr, 2)
            decoder = BinaryPayloadDecoder.fromRegisters(encoded_value, byteorder=self.byte_order,
                                                         wordorder=self.word_order)
        else:
            encoded_value = self.battery_store.getValues(fx, addr, 2)
            decoder = BinaryPayloadDecoder.fromRegisters(encoded_value, byteorder=self.byte_order,
                                                         wordorder=self.word_order)
        return decoder.decode_32bit_int() / self.scaling_factor
