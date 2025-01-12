"""Popcorn Picker integration."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "popcorn_picker"

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Popcorn Picker integration."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Popcorn Picker from a config entry."""
    hass.data[DOMAIN] = {}
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    hass.data.pop(DOMAIN, None)
    return True
