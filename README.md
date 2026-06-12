# Barco Projector Integration for Home Assistant

A custom Home Assistant integration to control Barco Projectors over a TCP network connection.

This integration is fully compatible with the **Home Assistant Community Store (HACS)**.

---

## Features

This integration registers the following Home Assistant entities:

*   **Power Switch (`switch`)**: Turn the projector on or off.
*   **Mute Switch (`switch`)**: Enable or disable picture mute (close or open the shutter).
*   **Input Select (`select`)**: Change the active input source (HDMI, DVI, VGA, DisplayPort, HDBaseT, SDI).
*   **Cropping Mode Select (`select`)**: Change the input cropping behavior (Disabled, Auto, 2.35:1, Manual).
*   **Brightness Controller (`number`)**: Adjust the projector brightness value (0-100).
*   **Contrast Controller (`number`)**: Adjust the projector contrast value (0-100).
*   **Cropping Top/Bottom Sliders (`number`)**: Fine-tune the manual cropping margins (0-1200 pixels).
*   **Diagnostic Sensors (`sensor`)**: Track Lamp Runtime, Estimated Remaining Lamp Time, and Total Unit Runtime.

---

## Installation

### Method 1: HACS (Recommended)
1. Ensure [HACS](https://hacs.xyz/) is installed.
2. In the HACS panel, go to **Integrations**, click the three dots in the top right, and select **Custom repositories**.
3. Enter the URL of this repository, select **Integration** as the category, and click **Add**.
4. Click **Install** on the Barco Projector card.
5. Restart Home Assistant.

### Method 2: Manual Installation
1. Copy the `custom_components/barco` directory from this repository into your Home Assistant config's `custom_components` folder (e.g. `/config/custom_components/`).
2. Restart Home Assistant.

---

## Configuration

This integration is configured using legacy YAML platforms. Add the following to your `configuration.yaml`:

```yaml
# Add Switch Entities
switch:
  - platform: barco
    ip_address: "192.168.1.50"
    port: 1025
    name: "Barco Projector"

# Add Sensor Entities
sensor:
  - platform: barco
    ip_address: "192.168.1.50"
    port: 1025
    name: "Barco Projector"

# Add Select Entities
select:
  - platform: barco
    ip_address: "192.168.1.50"
    port: 1025
    name: "Barco Projector"

# Add Number Entities
number:
  - platform: barco
    ip_address: "192.168.1.50"
    port: 1025
    name: "Barco Projector"
```

### Configuration Parameters

| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `ip_address` | String | **Yes** | — | The network IP address of the projector. |
| `port` | Integer | No | `1025` | The TCP network control port. |
| `name` | String | No | `"Barco Projector"` | Friendly name prefix for entities. |

---

## Developer Testing

To run the unit tests in this repository:
1. Initialize the virtual environment and install dependencies:
   ```bash
   pip install -r requirements_dev.txt
   ```
2. Execute pytest:
   ```bash
   pytest tests/
   ```
