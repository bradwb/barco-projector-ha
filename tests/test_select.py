import unittest
from unittest.mock import MagicMock
from custom_components.barco.select import BarcoInputSelect, BarcoCropSelect

class TestBarcoSelects(unittest.TestCase):
    def setUp(self):
        self.mock_hub = MagicMock()
        self.mock_hub.available = True

    def test_input_select_properties(self):
        select = BarcoInputSelect(self.mock_hub, "Test Projector")
        self.assertEqual(select.name, "Test Projector Input")
        self.assertTrue(select.available)
        self.assertEqual(select.icon, "mdi:video-input-hdmi")
        self.assertIn("HDMI", select.options)

    def test_input_select_update(self):
        select = BarcoInputSelect(self.mock_hub, "Test Projector")
        self.mock_hub.send_command.return_value = b"000008"
        
        select.update()
        self.mock_hub.send_command.assert_called_with(b":IABS?\r")
        self.assertEqual(select.current_option, "HDMI")

    def test_input_select_update_invalid(self):
        select = BarcoInputSelect(self.mock_hub, "Test Projector")
        self.mock_hub.send_command.return_value = b"999999"
        
        select.update()
        self.assertIsNone(select.current_option)

    def test_input_select_option(self):
        select = BarcoInputSelect(self.mock_hub, "Test Projector")
        select.select_option("HDMI")
        self.mock_hub.send_command.assert_called_with(b":IABS 8\r")
        self.assertEqual(select.current_option, "HDMI")

    def test_crop_select_properties(self):
        select = BarcoCropSelect(self.mock_hub, "Test Projector")
        self.assertEqual(select.name, "Test Projector Cropping Mode")
        self.assertTrue(select.available)
        self.assertEqual(select.icon, "mdi:crop")
        self.assertEqual(select.options, ["Disabled", "Auto", "2.35:1", "Manual"])

    def test_crop_select_update(self):
        select = BarcoCropSelect(self.mock_hub, "Test Projector")
        self.mock_hub.send_command.return_value = b"000002"
        
        select.update()
        self.mock_hub.send_command.assert_called_with(b":CTYP?\r")
        self.assertEqual(select.current_option, "2.35:1")

    def test_crop_select_option(self):
        select = BarcoCropSelect(self.mock_hub, "Test Projector")
        select.select_option("Manual")
        self.mock_hub.send_command.assert_called_with(b":CTYP 3\r")
        self.assertEqual(select.current_option, "Manual")
