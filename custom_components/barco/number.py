import logging
from datetime import timedelta
from typing import Optional

import voluptuous as vol

from homeassistant.components.number import (
    PLATFORM_SCHEMA as NUMBER_PLATFORM_SCHEMA,
    NumberEntity,
)
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.const import (
    CONF_NAME,
    CONF_IP_ADDRESS,
    CONF_PORT,
)

from .const import (
    DOMAIN,
    DEFAULT_NAME,
    CMD_BRIGHTNESS,
    CMD_CONTRAST,
    CMD_CROP_TOP,
    CMD_CROP_BOTTOM,
)
from .hub import BarcoHub

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=5)

PLATFORM_SCHEMA = NUMBER_PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_IP_ADDRESS): cv.string,
        vol.Optional(CONF_PORT, default=1025): cv.port,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    }
)

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: Optional[DiscoveryInfoType] = None,
) -> None:
    """Set up the Barco projector numbers."""
    ip_address = config[CONF_IP_ADDRESS]
    port = config[CONF_PORT]
    name = config[CONF_NAME]

    # Get or create shared hub for this IP address
    hass.data.setdefault(DOMAIN, {})
    if ip_address not in hass.data[DOMAIN]:
        hass.data[DOMAIN][ip_address] = BarcoHub(ip_address, port)
    hub = hass.data[DOMAIN][ip_address]

    add_entities([
        BarcoProjectorNumber(hub, name, "Brightness", CMD_BRIGHTNESS, "mdi:brightness-5"),
        BarcoProjectorNumber(hub, name, "Contrast", CMD_CONTRAST, "mdi:contrast"),
        BarcoProjectorNumber(
            hub, name, "Cropping Top", CMD_CROP_TOP, "mdi:crop-portrait", min_value=0.0, max_value=1200.0
        ),
        BarcoProjectorNumber(
            hub, name, "Cropping Bottom", CMD_CROP_BOTTOM, "mdi:crop-portrait", min_value=0.0, max_value=1200.0
        ),
    ])

class BarcoProjectorNumber(NumberEntity):
    """Representation of a Barco Projector setting (brightness/contrast/cropping) as a NumberEntity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        hub: BarcoHub,
        name: str,
        label: str,
        cmd_byte: bytes,
        icon: str,
        min_value: float = 0.0,
        max_value: float = 100.0,
        step: float = 1.0,
    ) -> None:
        """Initialize the number entity."""
        self._hub = hub
        self._attr_name = f"{name} {label}"
        self._cmd_byte = cmd_byte
        self._attr_icon = icon
        self._attr_native_min_value = min_value
        self._attr_native_max_value = max_value
        self._attr_native_step = step

    @property
    def available(self) -> bool:
        """Return True if hub is available."""
        return self._hub.available

    @property
    def native_step(self) -> float:
        """Return the increment/decrement step."""
        return self._attr_native_step

    def update(self) -> None:
        """Fetch the current value from the projector."""
        cmd = b":" + self._cmd_byte + b"?\r"
        res = self._hub.send_command(cmd)
        if res is not None:
            try:
                self._attr_native_value = float(int(res))
            except ValueError:
                _LOGGER.warning("Could not parse numeric response for %s: %s", self._cmd_byte.decode(), res)
                self._attr_native_value = None
        else:
            self._attr_native_value = None

    def set_native_value(self, value: float) -> None:
        """Set a new value on the projector."""
        val_int = int(value)
        cmd = b":" + self._cmd_byte + b" " + str(val_int).encode() + b"\r"
        self._hub.send_command(cmd)
        self._attr_native_value = value
