import logging
from datetime import timedelta
from typing import Optional

import voluptuous as vol

from homeassistant.components.select import (
    PLATFORM_SCHEMA as SELECT_PLATFORM_SCHEMA,
    SelectEntity,
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
    CMD_INPUT,
    INPUT_SOURCES,
    INPUT_SOURCES_INV,
    CMD_CROP_MODE,
    CROP_MODES,
    CROP_MODES_INV,
)
from .hub import BarcoHub

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=5)

PLATFORM_SCHEMA = SELECT_PLATFORM_SCHEMA.extend(
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
    """Set up the Barco projector input select."""
    ip_address = config[CONF_IP_ADDRESS]
    port = config[CONF_PORT]
    name = config[CONF_NAME]

    # Get or create shared hub for this IP address
    hass.data.setdefault(DOMAIN, {})
    if ip_address not in hass.data[DOMAIN]:
        hass.data[DOMAIN][ip_address] = BarcoHub(ip_address, port)
    hub = hass.data[DOMAIN][ip_address]

    add_entities([
        BarcoInputSelect(hub, name),
        BarcoCropSelect(hub, name)
    ])

class BarcoInputSelect(SelectEntity):
    """Representation of a Barco Projector input select entity."""

    _attr_icon = "mdi:video-input-hdmi"
    _attr_has_entity_name = True

    def __init__(self, hub: BarcoHub, name: str) -> None:
        """Initialize the input select."""
        self._hub = hub
        self._attr_name = f"{name} Input"
        self._attr_options = list(INPUT_SOURCES.keys())

    @property
    def available(self) -> bool:
        """Return True if hub is available."""
        return self._hub.available

    def update(self) -> None:
        """Fetch the current input source from the projector."""
        cmd = b":" + CMD_INPUT + b"?\r"
        res = self._hub.send_command(cmd)
        if res is not None:
            try:
                val = int(res)
                self._attr_current_option = INPUT_SOURCES_INV.get(val)
            except ValueError:
                _LOGGER.warning("Could not parse input response: %s", res)
                self._attr_current_option = None
        else:
            self._attr_current_option = None

    def select_option(self, option: str) -> None:
        """Change the active input source."""
        if option in INPUT_SOURCES:
            val = INPUT_SOURCES[option]
            cmd = b":" + CMD_INPUT + b" " + str(val).encode() + b"\r"
            self._hub.send_command(cmd)
            self._attr_current_option = option


class BarcoCropSelect(SelectEntity):
    """Representation of a Barco Projector input cropping mode select entity."""

    _attr_icon = "mdi:crop"
    _attr_has_entity_name = True

    def __init__(self, hub: BarcoHub, name: str) -> None:
        """Initialize the cropping select."""
        self._hub = hub
        self._attr_name = f"{name} Cropping Mode"
        self._attr_options = list(CROP_MODES.keys())

    @property
    def available(self) -> bool:
        """Return True if hub is available."""
        return self._hub.available

    def update(self) -> None:
        """Fetch the current cropping mode from the projector."""
        cmd = b":" + CMD_CROP_MODE + b"?\r"
        res = self._hub.send_command(cmd)
        if res is not None:
            try:
                val = int(res)
                self._attr_current_option = CROP_MODES_INV.get(val)
            except ValueError:
                _LOGGER.warning("Could not parse cropping mode response: %s", res)
                self._attr_current_option = None
        else:
            self._attr_current_option = None

    def select_option(self, option: str) -> None:
        """Change the active cropping mode."""
        if option in CROP_MODES:
            val = CROP_MODES[option]
            cmd = b":" + CMD_CROP_MODE + b" " + str(val).encode() + b"\r"
            self._hub.send_command(cmd)
            self._attr_current_option = option
