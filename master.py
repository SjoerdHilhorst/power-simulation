from pymodbus.client.sync import ModbusTcpClient



def run_master(add,port,in1,in2,in3,queue):
    # get_registers
    queue.put("started")
    power_register_in_address = in1
    current_register_in_address = in2
    state_charge_address = in3

    client = ModbusTcpClient(add, port=port)
    print("Connected")

    # Write values
    client.write_registers(power_register_in_address, 55)
    client.write_registers(current_register_in_address, 80)
    client.write_registers(state_charge_address, 5610)

    # Read Values
    input = client.read_holding_registers(power_register_in_address)
    current = client.read_holding_registers(current_register_in_address)
    charge = client.read_holding_registers(state_charge_address)
    i=0
    c=0
    cu=0
    i = input.registers[0]
    c = current.registers[0]
    cu = charge.registers[0]
    # Print Values
    print("Input: ", i)
    print("Current: ", c)
    print("Charge: ", cu, "%")
    queue.put("done")
    queue.put(str(i))
    queue.put(str(c))
    queue.put(str(cu))
    client.close()

