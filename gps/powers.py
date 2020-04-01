import random


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
