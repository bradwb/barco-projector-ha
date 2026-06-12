import unittest
from unittest.mock import MagicMock
from custom_components.barco.switch import BarcoPowerSwitch, BarcoMuteSwitch

class TestBarcoSwitches(unittest.TestCase):
    def setUp(self):
        self.mock_hub = MagicMock()
        self.mock_hub.available = True

    def test_power_switch_properties(self):
        switch = BarcoPowerSwitch(self.mock_hub, "Test Projector")
        self.assertEqual(switch.name, "Test Projector")
        self.assertTrue(switch.available)
        self.assertEqual(switch.icon, "mdi:projector")

    def test_power_switch_update_on(self):
        switch = BarcoPowerSwitch(self.mock_hub, "Test Projector")
        self.mock_hub.send_command.return_value = b"000001"
        
        switch.update()
        self.mock_hub.send_command.assert_called_with(b":POWR?\r")
        self.assertTrue(switch.is_on)

    def test_power_switch_update_off(self):
        switch = BarcoPowerSwitch(self.mock_hub, "Test Projector")
        self.mock_hub.send_command.return_value = b"000000"
        
        switch.update()
        self.mock_hub.send_command.assert_called_with(b":POWR?\r")
        self.assertFalse(switch.is_on)

    def test_power_switch_turn_on(self):
        switch = BarcoPowerSwitch(self.mock_hub, "Test Projector")
        switch.turn_on()
        self.mock_hub.send_command.assert_called_with(b":POWR 1\r")

    def test_power_switch_turn_off(self):
        switch = BarcoPowerSwitch(self.mock_hub, "Test Projector")
        switch.turn_off()
        self.mock_hub.send_command.assert_called_with(b":POWR 0\r")

    def test_mute_switch_properties(self):
        switch = BarcoMuteSwitch(self.mock_hub, "Test Projector")
        self.assertEqual(switch.name, "Test Projector Mute")
        self.assertTrue(switch.available)
        self.assertEqual(switch.icon, "mdi:shutter")

    def test_mute_switch_update_on(self):
        switch = BarcoMuteSwitch(self.mock_hub, "Test Projector")
        self.mock_hub.send_command.return_value = b"000001"
        
        switch.update()
        self.mock_hub.send_command.assert_called_with(b":PMUT?\r")
        self.assertTrue(switch.is_on)

    def test_mute_switch_update_off(self):
        switch = BarcoMuteSwitch(self.mock_hub, "Test Projector")
        self.mock_hub.send_command.return_value = b"000000"
        
        switch.update()
        self.mock_hub.send_command.assert_called_with(b":PMUT?\r")
        self.assertFalse(switch.is_on)

    def test_mute_switch_turn_on(self):
        switch = BarcoMuteSwitch(self.mock_hub, "Test Projector")
        switch.turn_on()
        self.mock_hub.send_command.assert_called_with(b":PMUT 1\r")

    def test_mute_switch_turn_off(self):
        switch = BarcoMuteSwitch(self.mock_hub, "Test Projector")
        switch.turn_off()
        self.mock_hub.send_command.assert_called_with(b":PMUT 0\r")
