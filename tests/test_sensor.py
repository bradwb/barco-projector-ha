import unittest
from unittest.mock import MagicMock
from custom_components.barco.sensor import BarcoProjectorSensor
from custom_components.barco.const import CMD_LAMP_RUNTIME, CMD_POWER_STATE

class TestBarcoSensors(unittest.TestCase):
    def setUp(self):
        self.mock_hub = MagicMock()
        self.mock_hub.available = True

    def test_sensor_properties(self):
        sensor = BarcoProjectorSensor(self.mock_hub, "Test Projector", "Lamp Runtime", CMD_LAMP_RUNTIME, "mdi:timer-sand")
        self.assertEqual(sensor.name, "Test Projector Lamp Runtime")
        self.assertTrue(sensor.available)
        self.assertEqual(sensor.icon, "mdi:timer-sand")
        self.assertEqual(sensor.native_unit_of_measurement, "h")

    def test_sensor_update_success(self):
        sensor = BarcoProjectorSensor(self.mock_hub, "Test Projector", "Lamp Runtime", CMD_LAMP_RUNTIME, "mdi:timer-sand")
        self.mock_hub.send_command.return_value = b"000123"
        
        sensor.update()
        self.mock_hub.send_command.assert_called_with(b":LTR1?\r")
        self.assertEqual(sensor.native_value, 123)

    def test_sensor_update_invalid_int(self):
        sensor = BarcoProjectorSensor(self.mock_hub, "Test Projector", "Lamp Runtime", CMD_LAMP_RUNTIME, "mdi:timer-sand")
        self.mock_hub.send_command.return_value = b"ABC"
        
        sensor.update()
        self.assertIsNone(sensor.native_value)

    def test_sensor_update_none_response(self):
        sensor = BarcoProjectorSensor(self.mock_hub, "Test Projector", "Lamp Runtime", CMD_LAMP_RUNTIME, "mdi:timer-sand")
        self.mock_hub.send_command.return_value = None
        
        sensor.update()
        self.assertIsNone(sensor.native_value)

    def test_power_state_sensor_properties(self):
        sensor = BarcoProjectorSensor(self.mock_hub, "Test Projector", "Power State", CMD_POWER_STATE, "mdi:power-settings", unit_of_measurement=None)
        self.assertEqual(sensor.name, "Test Projector Power State")
        self.assertEqual(sensor.icon, "mdi:power-settings")
        self.assertIsNone(sensor.native_unit_of_measurement)

    def test_power_state_sensor_update_success(self):
        sensor = BarcoProjectorSensor(self.mock_hub, "Test Projector", "Power State", CMD_POWER_STATE, "mdi:power-settings", unit_of_measurement=None)
        
        # Test state "Powering up" (value 2)
        self.mock_hub.send_command.return_value = b"000002"
        sensor.update()
        self.mock_hub.send_command.assert_called_with(b":POST?\r")
        self.assertEqual(sensor.native_value, "Powering up")

        # Test state "On" (value 3)
        self.mock_hub.send_command.return_value = b"000003"
        sensor.update()
        self.assertEqual(sensor.native_value, "On")

        # Test unknown state code
        self.mock_hub.send_command.return_value = b"000099"
        sensor.update()
        self.assertEqual(sensor.native_value, "Unknown (99)")
