import random

# I know it seems kinda redundant to have to classes. But i guess in future they might have different behaviour

class PowerIn:
    def __init__(self, range_active, range_reactive):
        self.range_active = range_active
        self.range_reactive = range_reactive

    def get_active_power(self):
        value = round(random.uniform(*self.range_active), 1)
        return value

    def get_reactive_power(self):
        value = round(random.uniform(*self.range_reactive), 1)
        return value


class PowerOut:
    def __init__(self, range_active, range_reactive):
        self.range_active = range_active
        self.range_reactive = range_reactive

    def get_active_power(self):
        value = round(random.uniform(*self.range_active), 1)
        return value

    def get_reactive_power(self):
        value = round(random.uniform(*self.range_reactive), 1)
        return value

def random_simulation(battery):

    power_source = PowerIn((0, 200), (-65, 185))
    power_load = PowerOut((-11, 25), (-15, 25))

    # connect battery to the power
    battery.connect_power_in(power_source)

    # connect battery to the load
    battery.connect_power_out(power_load)

    # at this point battery starts to update its state
    battery.run()

    # fill in all dependent fields
    battery.update()
