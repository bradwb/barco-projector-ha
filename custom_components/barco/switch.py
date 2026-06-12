import logging
import voluptuous as vol
from datetime import timedelta
from typing import Any, Optional

from homeassistant.components.switch import (
    PLATFORM_SCHEMA as SWITCH_PLATFORM_SCHEMA,
    SwitchEntity,
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
    CMD_POWER,
    CMD_MUTE,
    ICON,
)
from .hub import BarcoHub

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=5)

PLATFORM_SCHEMA = SWITCH_PLATFORM_SCHEMA.extend(
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
    """Set up the Barco projector switches."""
    ip_address = config[CONF_IP_ADDRESS]
    port = config[CONF_PORT]
    name = config[CONF_NAME]

    # Get or create shared hub for this IP address
    hass.data.setdefault(DOMAIN, {})
    if ip_address not in hass.data[DOMAIN]:
        hass.data[DOMAIN][ip_address] = BarcoHub(ip_address, port)
    hub = hass.data[DOMAIN][ip_address]

    add_entities([
        BarcoPowerSwitch(hub, name),
        BarcoMuteSwitch(hub, name)
    ])

class BarcoPowerSwitch(SwitchEntity):
    """Represents the Barco Projector Power switch."""

    _attr_icon = ICON
    _attr_has_entity_name = True

    def __init__(self, hub: BarcoHub, name: str) -> None:
        """Initialize the power switch."""
        self._hub = hub
        self._attr_name = name

    @property
    def available(self) -> bool:
        """Return True if hub is available."""
        return self._hub.available

    def update(self) -> None:
        """Get the current power state."""
        cmd = b":" + CMD_POWER + b"?\r"
        res = self._hub.send_command(cmd)
        self._attr_is_on = (res == b"000001")

    def turn_on(self, **kwargs: Any) -> None:
        """Turn the projector on."""
        cmd = b":" + CMD_POWER + b" 1\r"
        self._hub.send_command(cmd)

    def turn_off(self, **kwargs: Any) -> None:
        """Turn the projector off."""
        cmd = b":" + CMD_POWER + b" 0\r"
        self._hub.send_command(cmd)


class BarcoMuteSwitch(SwitchEntity):
    """Represents the Barco Projector Picture Mute / Shutter switch."""

    _attr_icon = "mdi:shutter"
    _attr_has_entity_name = True

    def __init__(self, hub: BarcoHub, name: str) -> None:
        """Initialize the mute switch."""
        self._hub = hub
        self._attr_name = f"{name} Mute"

    @property
    def available(self) -> bool:
        """Return True if hub is available."""
        return self._hub.available

    def update(self) -> None:
        """Get the current mute state."""
        cmd = b":" + CMD_MUTE + b"?\r"
        res = self._hub.send_command(cmd)
        self._attr_is_on = (res == b"000001")

    def turn_on(self, **kwargs: Any) -> None:
        """Mute the projector (close shutter)."""
        cmd = b":" + CMD_MUTE + b" 1\r"
        self._hub.send_command(cmd)

    def turn_off(self, **kwargs: Any) -> None:
        """Unmute the projector (open shutter)."""
        cmd = b":" + CMD_MUTE + b" 0\r"
        self._hub.send_command(cmd)
