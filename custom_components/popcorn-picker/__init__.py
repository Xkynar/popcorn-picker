from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from dataclasses import dataclass
from .coordinator import PopcornCoordinator
from .const import DOMAIN

# Define a type alias for the config entry runtime data
type PopcornConfigEntry = ConfigEntry["PopcornData"]


@dataclass
class PopcornData:
    coordinator: PopcornCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: PopcornConfigEntry) -> bool:
    """Set up Popcorn Picker from a config entry."""
    # Initialize the coordinator
    coordinator = PopcornCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()

    # Assign the runtime_data
    entry.runtime_data = PopcornData(coordinator=coordinator)

    # Forward setup to platforms
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    return True
