"""Sensor platform for Popcorn Picker."""
from homeassistant.helpers.entity import Entity

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up sensors based on a config entry."""
    async_add_entities([PopcornPickerSensor()])

class PopcornPickerSensor(Entity):
    """Representation of a Popcorn Picker sensor."""

    def __init__(self):
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Popcorn Picker"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    async def async_update(self):
        """Fetch new state data."""
        # Logic to fetch data and update self._state
        self._state = "Example State"
