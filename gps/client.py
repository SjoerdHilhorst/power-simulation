""" Client == master == GreenerEye """

from pymodbus.client.sync import ModbusTcpClient as ModbusClient

import config as address


class GreenerEye:

    def __init__(self):
        self.client = ModbusClient('localhost', port=5030)

    def read_value(self, addr):
        fx = addr // address.fx_addr_separator
        addr = addr % address.fx_addr_separator
        if fx == 1:
            val = self.client.read_coils(addr).bits[0]
        elif fx == 2:
            val = self.client.read_discrete_inputs(addr).bits[0]
        elif fx == 3:
            val = self.client.read_holding_registers(addr).registers[0] / address.scaling_factor
        else:
            val = self.client.read_input_registers(addr).registers[0] / address.scaling_factor
        return val

    def run(self):
        self.client.connect()

        print("CLIENT: is running")
        print("active power in: ", self.read_value(address.active_power_in))
        print("reactive power in: ", self.read_value(address.reactive_power_in))
        print("active power out: ", self.read_value(address.active_power_out))
        print("reactive power out: ", self.read_value(address.reactive_power_out))
        print("converter started: ", self.read_value(address.converter_started))
        print("active power out: ", self.read_value(address.active_power_out))
        print("input connected: ", self.read_value(address.input_connected))
        print("system on backup battery: ", self.read_value(address.system_on_backup_battery))
        print("system status: ", self.read_value(address.system_status))
        print("system mode: ", self.read_value(address.system_mode))
        print("accept values: ", self.read_value(address.accept_values))
        print("active power converter: ", self.read_value(address.active_power_converter))
        print("reactive power converter: ", self.read_value(address.reactive_power_converter))
        print("voltage I1 I2 in: ", self.read_value(address.voltage_l1_l2_in))
        print("voltage I2 I3 in: ", self.read_value(address.voltage_l2_l3_in))
        print("voltage I3 I1 in: ", self.read_value(address.voltage_l3_l1_in))
        print("current I1 in: ", self.read_value(address.current_l1_in))
        print("current I2 in: ", self.read_value(address.current_l2_in))
        print("current I3 in: ", self.read_value(address.current_l3_in))
        print("frequency in: ", self.read_value(address.frequency_in))
        print("voltage I1 I2 out: ", self.read_value(address.voltage_l1_l2_out))
        print("voltage I2 I3 out: ", self.read_value(address.voltage_l2_l3_out))
        print("voltage I3 I1 out: ", self.read_value(address.voltage_l3_l1_out))
        print("current I1 out: ", self.read_value(address.current_l1_out))
        print("current I2 out: ", self.read_value(address.current_l2_out))
        print("current I3 out: ", self.read_value(address.current_l3_out))
        print("frequency out: ", self.read_value(address.frequency_out))

        # PROBLEM HERE
        print("soc: ", self.read_value(address.soc))
        self.client.close()


eye = GreenerEye()
eye.run()
