"""The Popcorn Picker integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .api import MovieAPI
from .const import DOMAIN

PLATFORMS = [Platform.SENSOR]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the integration from YAML."""
    if DOMAIN not in config:
        return True

    # Extract YAML config
    yaml_config = config[DOMAIN]
    param1 = yaml_config["param1"]

    # Initialize API
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN]["yaml"] = MovieAPI(param1)

    # Trigger platform loading
    hass.async_create_task(
        hass.helpers.discovery.async_load_platform("sensor", DOMAIN, {}, config)
    )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the integration from UI."""
    # Extract UI config
    param1 = entry.data["param1"]

    # Initialize API
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = MovieAPI(param1)

    # Forward entry to sensor platform
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
