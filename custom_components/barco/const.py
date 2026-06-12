from typing import Final

DOMAIN: Final = "barco"
DEFAULT_NAME: Final = "Barco Projector"

# Commands
CMD_POWER: Final = b"POWR"
CMD_INPUT: Final = b"IABS"
CMD_BRIGHTNESS: Final = b"BRIG"
CMD_CONTRAST: Final = b"CNTR"
CMD_MUTE: Final = b"PMUT"
CMD_LAMP_RUNTIME: Final = b"LTR1"
CMD_LAMP_REMAINING: Final = b"LRM1"
CMD_UNIT_TOTAL_TIME: Final = b"UTOT"
CMD_CROP_MODE: Final = b"CTYP"
CMD_CROP_TOP: Final = b"CTOP"
CMD_CROP_BOTTOM: Final = b"CBTM"
CMD_POWER_STATE: Final = b"POST"

# Power state mappings
POWER_STATES: Final = {
    0: "Deep sleep",
    1: "Off",
    2: "Powering up",
    3: "On",
    4: "Powering down",
    5: "Critical powering down",
    6: "Critical off",
}

# Cropping mode mappings
CROP_MODES: Final = {
    "Disabled": 0,
    "Auto": 1,
    "2.35:1": 2,
    "Manual": 3,
}
CROP_MODES_INV: Final = {v: k for k, v in CROP_MODES.items()}

# Input source mappings
INPUT_SOURCES: Final = {
    "VGA": 0,
    "DVI": 2,
    "HDMI": 8,
    "DisplayPort 1": 17,
    "DisplayPort 2": 18,
    "HDBaseT": 19,
    "SDI 1": 20,
    "SDI 2": 21
}
INPUT_SOURCES_INV: Final = {v: k for k, v in INPUT_SOURCES.items()}

ICON: Final = "mdi:projector"
