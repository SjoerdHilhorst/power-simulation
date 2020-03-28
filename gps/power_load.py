import random


class PowerFeed:
    def __init__(self):
        self

    def active_power_in(self):
        value = round(random.uniform(0,200), 1)
        return value

    def active_power_out(self):
        value = round(random.uniform(-65, 185), 1)
        return value

    def reactive_power_in(self):
        value = round(random.uniform(-11, 25), 1)
        return value

    def reactive_power_out(self):
        value = round(random.uniform(-15, 25), 1)
        return value
