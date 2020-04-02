
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder





class FloatHandler:
    def __init__(self, byte_order, word_order, float_mode, scaling_factor, store):
        self.builder = BinaryPayloadBuilder(byteorder=byte_order, wordorder=word_order)
        self.byte_order = byte_order
        self.word_order = word_order
        self.float_mode = float_mode
        self.scaling_factor = scaling_factor
        self.battery_store = store

    def encode_float(self, value):
        """
        encodes float according to the way it is stored in registry
        SCALE stands for multiplying/dividing by scaling factor method, I.E. 32bit int
        COMB stands for storing the float in two registers, I.E. 32bit float
        :param value: float which should be handled
        :return: float rounded to integer
        """
        self.builder.reset()
        if self.float_mode == "SCALE":
            self.builder.add_32bit_int(round(value * self.scaling_factor))
        elif self.float_mode == "COMB":
            self.builder.add_32bit_float(value)
        return self.builder.to_registers()

    def decode_float(self, fx, addr):
        """
        decodes float value, the way specified in address
        """
        encoded_value = self.battery_store.getValues(fx, addr, 2)
        decoder = BinaryPayloadDecoder.fromRegisters(encoded_value, byteorder=self.byte_order,
                                                     wordorder=self.word_order)
        if self.float_mode == "SCALE":
            value = decoder.decode_32bit_int() / self.scaling_factor
        elif self.float_mode == "COMB":
            value = decoder.decode_32bit_float()
        return value

