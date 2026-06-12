import logging
from datetime import timedelta
from typing import Optional

import voluptuous as vol

from homeassistant.components.sensor import (
    PLATFORM_SCHEMA as SENSOR_PLATFORM_SCHEMA,
    SensorEntity,
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
    CMD_LAMP_RUNTIME,
    CMD_LAMP_REMAINING,
    CMD_UNIT_TOTAL_TIME,
    CMD_POWER_STATE,
    POWER_STATES,
)
from .hub import BarcoHub

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=15) # Sensors can be updated less frequently

PLATFORM_SCHEMA = SENSOR_PLATFORM_SCHEMA.extend(
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
    """Set up the Barco projector sensors."""
    ip_address = config[CONF_IP_ADDRESS]
    port = config[CONF_PORT]
    name = config[CONF_NAME]

    # Get or create shared hub for this IP address
    hass.data.setdefault(DOMAIN, {})
    if ip_address not in hass.data[DOMAIN]:
        hass.data[DOMAIN][ip_address] = BarcoHub(ip_address, port)
    hub = hass.data[DOMAIN][ip_address]

    add_entities([
        BarcoProjectorSensor(hub, name, "Lamp Runtime", CMD_LAMP_RUNTIME, "mdi:timer-sand"),
        BarcoProjectorSensor(hub, name, "Lamp Remaining", CMD_LAMP_REMAINING, "mdi:timer-sand-empty"),
        BarcoProjectorSensor(hub, name, "Total Unit Runtime", CMD_UNIT_TOTAL_TIME, "mdi:clock-outline"),
        BarcoProjectorSensor(hub, name, "Power State", CMD_POWER_STATE, "mdi:power-settings", unit_of_measurement=None)
    ])

class BarcoProjectorSensor(SensorEntity):
    """Representation of a Barco Projector diagnostic sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        hub: BarcoHub,
        name: str,
        label: str,
        cmd_byte: bytes,
        icon: str,
        unit_of_measurement: Optional[str] = "h",
    ) -> None:
        """Initialize the sensor."""
        self._hub = hub
        self._attr_name = f"{name} {label}"
        self._cmd_byte = cmd_byte
        self._attr_icon = icon
        self._attr_native_unit_of_measurement = unit_of_measurement

    @property
    def available(self) -> bool:
        """Return True if hub is available."""
        return self._hub.available

    def update(self) -> None:
        """Fetch the current value from the projector."""
        cmd = b":" + self._cmd_byte + b"?\r"
        res = self._hub.send_command(cmd)
        if res is not None:
            try:
                val = int(res)
                if self._cmd_byte == CMD_POWER_STATE:
                    self._attr_native_value = POWER_STATES.get(val, f"Unknown ({val})")
                else:
                    self._attr_native_value = val
            except ValueError:
                _LOGGER.warning("Could not parse sensor response for %s: %s", self._cmd_byte.decode(), res)
                self._attr_native_value = None
        else:
            self._attr_native_value = None
