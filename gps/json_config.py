import json

"""
for the 'address' dictionary the values should be of the form  of the list of size 2, where [0] element is the 
register type (1: coils; 2: discrete input; 3: input registers; 4: holding registers) and [1] element is the actual 
address
"""


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
