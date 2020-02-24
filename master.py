from pymodbus.client.sync import ModbusTcpClient

#get_registers

power_register_in_address = int(input("What is the power register in address?"))
current_register_in_address = int(input("What is the current register in address?"))
state_charge_address = int(input("What is the state of charge address?"))

client = ModbusTcpClient('localhost', port=5020)
print("Connected")

#Write values
client.write_registers(power_register_in_address,55)
client.write_registers(current_register_in_address,80)
client.write_registers(state_charge_address,5610)


#Read Values
input = client.read_holding_registers(power_register_in_address)
current = client.read_holding_registers(current_register_in_address)
charge = client.read_holding_registers(state_charge_address)


#Print Values
print("Input: ", input.registers[0])
print("Current: ", current.registers[0])
print("Current: ", charge.registers[0]/100, "%")

client.close()