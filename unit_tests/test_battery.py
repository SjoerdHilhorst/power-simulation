import unittest
from src.battery.battery import Battery
from src.config.env import env


class TestBattery(unittest.TestCase):

    def test_get_value(self):
        battery = Battery(env)
        value = battery.get_value(battery.fields['system_status'])
        self.assertEqual(value, 1.0)

    def test_set_value(self):
        battery = Battery(env)
        battery.set_value(battery.fields['system_status'], 0)
        self.assertEqual(0, battery.get_value(battery.fields['system_status']))

    def test_is_input_connected(self):
        battery = Battery(env)
        battery.set_value(battery.fields['input_connected'], 1)
        self.assertTrue(battery.is_input_connected())

    def test_is_converter_started(self):
        battery = Battery(env)
        battery.set_value(battery.fields['converter_started'], 1)
        self.assertTrue(battery.is_converter_started())

    def test_set_initial_values(self):
        battery = Battery(env)
        battery.set_initial_values()
        self.assertAlmostEqual(72.2, battery.get_value(battery.fields['soc']), 3)
        self.assertEqual(1, battery.get_value(battery.fields['system_status']))
        self.assertEqual(5, battery.get_value(battery.fields['system_mode']))
        self.assertEqual(1, battery.get_value(battery.fields['converter_started']))
        self.assertEqual(1, battery.get_value(battery.fields['input_connected']))
        self.assertEqual(1, battery.get_value(battery.fields['system_on_backup_battery']))

if __name__ == '__main__':
    unittest.main()