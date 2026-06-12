import unittest
from unittest.mock import MagicMock, patch
from custom_components.barco.hub import BarcoHub

class TestBarcoHub(unittest.TestCase):
    def setUp(self):
        self.hub = BarcoHub("127.0.0.1", 1025)

    @patch("socket.create_connection")
    def test_connect_success(self, mock_create_connection):
        mock_socket = MagicMock()
        mock_create_connection.return_value = mock_socket
        
        self.assertTrue(self.hub._connect())
        self.assertTrue(self.hub.available)
        self.assertIsNotNone(self.hub._socket)

    @patch("socket.create_connection")
    def test_connect_failure(self, mock_create_connection):
        mock_create_connection.side_effect = Exception("Connection refused")
        
        self.assertFalse(self.hub._connect())
        self.assertFalse(self.hub.available)
        self.assertIsNone(self.hub._socket)

    @patch("socket.create_connection")
    def test_disconnect(self, mock_create_connection):
        mock_socket = MagicMock()
        mock_create_connection.return_value = mock_socket
        
        self.hub._connect()
        self.hub.disconnect()
        mock_socket.close.assert_called_once()
        self.assertIsNone(self.hub._socket)
        self.assertFalse(self.hub.available)

    @patch("socket.create_connection")
    def test_send_command_success(self, mock_create_connection):
        mock_socket = MagicMock()
        mock_create_connection.return_value = mock_socket
        mock_socket.recv.return_value = b"%001 POWR 000001\r\n"
        
        self.hub._connect()
        response = self.hub.send_command(b":POWR 1\r")
        mock_socket.sendall.assert_called_with(b":POWR 1\r")
        self.assertEqual(response, b"000001")

    @patch("socket.create_connection")
    def test_send_command_error(self, mock_create_connection):
        mock_socket = MagicMock()
        mock_create_connection.return_value = mock_socket
        mock_socket.recv.return_value = b"%001 POWR !00001\r\n"
        
        self.hub._connect()
        response = self.hub.send_command(b":POWR 1\r")
        self.assertIsNone(response)

    @patch("socket.create_connection")
    def test_send_command_invalid_response(self, mock_create_connection):
        mock_socket = MagicMock()
        mock_create_connection.return_value = mock_socket
        mock_socket.recv.return_value = b"INVALID\r\n"
        
        self.hub._connect()
        response = self.hub.send_command(b":POWR 1\r")
        self.assertIsNone(response)

    @patch("socket.create_connection")
    def test_send_command_socket_exception(self, mock_create_connection):
        mock_socket = MagicMock()
        mock_create_connection.return_value = mock_socket
        mock_socket.sendall.side_effect = Exception("Socket error")
        
        self.hub._connect()
        response = self.hub.send_command(b":POWR 1\r")
        self.assertIsNone(response)
        self.assertIsNone(self.hub._socket)
        self.assertFalse(self.hub.available)
