import json

def get_data(addr=None):
    """
    Gets the addresses for the simulation/client/battery
    If addr has a variable then it will get the custom json of that pathname
    """
    if addr:
        address = get_custom_json(addr)["address"]
    return address

def get_custom_json(addr):
    """
    returns a custom json as a dictionary
    addr: should not include path or .json, e.g. filename : 'my_custom_addresses'
    """
    with open('config/' + addr + '.json') as f:
        address = json.load(f)
    return address
