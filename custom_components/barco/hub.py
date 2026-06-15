import logging
import socket
import threading
from typing import Optional

_LOGGER = logging.getLogger(__name__)

class BarcoHub:
    """Thread-safe connection hub to communicate with the Barco projector."""

    def __init__(self, ip_address: str, port: int) -> None:
        """Initialize the hub."""
        self._ip_address = ip_address
        self._port = port
        self._socket = None
        self._lock = threading.Lock()
        self.available = False

    def _connect(self) -> bool:
        """Establish TCP socket connection with the projector."""
        if self._socket is not None:
            return True
        try:
            self._socket = socket.create_connection((self._ip_address, self._port), timeout=1.0)
            self.available = True
            _LOGGER.debug("Connected to Barco projector at %s:%s", self._ip_address, self._port)
            return True
        except Exception:
            self._socket = None
            self.available = False
            _LOGGER.exception("Failed to connect to Barco projector at %s:%s", self._ip_address, self._port)
            return False

    def disconnect(self) -> None:
        """Close the socket connection."""
        with self._lock:
            if self._socket is not None:
                try:
                    self._socket.close()
                except Exception:
                    pass
                self._socket = None
                self.available = False
                _LOGGER.debug("Disconnected from Barco projector")

    def send_command(self, command: bytes) -> Optional[bytes]:
        """Send a raw command to the projector and return the parsed value response."""
        with self._lock:
            if self._socket is None:
                if not self._connect():
                    return None
            try:
                self._socket.sendall(command)
                response = self._socket.recv(1024).rstrip()
                _LOGGER.debug("Sent: %s, Received: %s", command, response)
                
                parts = response.split()
                if len(parts) >= 3:
                    val = parts[2]
                    if val.startswith(b"!"):
                        if val.startswith(b"!00002"):
                            _LOGGER.debug("Command %s not available in current state (error !00002)", command.decode())
                        else:
                            _LOGGER.warning("Projector returned error %s for command %s", val.decode(), command.decode())
                        return None
                    return val
                else:
                    _LOGGER.warning("Invalid response format received: %s", response)
                    return None
            except Exception:
                _LOGGER.exception("Error communicating with Barco projector")
                if self._socket is not None:
                    try:
                        self._socket.close()
                    except Exception:
                        pass
                    self._socket = None
                self.available = False
                return None
