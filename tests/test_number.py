import unittest
from unittest.mock import MagicMock
from custom_components.barco.number import BarcoProjectorNumber
from custom_components.barco.const import CMD_BRIGHTNESS, CMD_CROP_TOP

class TestBarcoNumbers(unittest.TestCase):
    def setUp(self):
        self.mock_hub = MagicMock()
        self.mock_hub.available = True

    def test_brightness_properties(self):
        num = BarcoProjectorNumber(self.mock_hub, "Test Projector", "Brightness", CMD_BRIGHTNESS, "mdi:brightness-5")
        self.assertEqual(num.name, "Test Projector Brightness")
        self.assertTrue(num.available)
        self.assertEqual(num.icon, "mdi:brightness-5")
        self.assertEqual(num.native_min_value, 0.0)
        self.assertEqual(num.native_max_value, 100.0)
        self.assertEqual(num.native_step, 1.0)

    def test_cropping_top_properties(self):
        num = BarcoProjectorNumber(
            self.mock_hub, "Test Projector", "Cropping Top", CMD_CROP_TOP, "mdi:crop-portrait",
            min_value=0.0, max_value=1200.0
        )
        self.assertEqual(num.name, "Test Projector Cropping Top")
        self.assertEqual(num.native_min_value, 0.0)
        self.assertEqual(num.native_max_value, 1200.0)
        self.assertEqual(num.native_step, 1.0)

    def test_number_update(self):
        num = BarcoProjectorNumber(self.mock_hub, "Test Projector", "Brightness", CMD_BRIGHTNESS, "mdi:brightness-5")
        self.mock_hub.send_command.return_value = b"000050"
        
        num.update()
        self.mock_hub.send_command.assert_called_with(b":BRIG?\r")
        self.assertEqual(num.native_value, 50.0)

    def test_number_update_invalid(self):
        num = BarcoProjectorNumber(self.mock_hub, "Test Projector", "Brightness", CMD_BRIGHTNESS, "mdi:brightness-5")
        self.mock_hub.send_command.return_value = b"INVALID"
        
        num.update()
        self.assertIsNone(num.native_value)

    def test_number_set_value(self):
        num = BarcoProjectorNumber(self.mock_hub, "Test Projector", "Brightness", CMD_BRIGHTNESS, "mdi:brightness-5")
        num.set_native_value(65.0)
        self.mock_hub.send_command.assert_called_with(b":BRIG 65\r")
        self.assertEqual(num.native_value, 65.0)
