from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .entity import MovieSensor
from . import PopcornConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,
    entry: PopcornConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up movie sensors for Popcorn Picker."""
    # Access coordinator from runtime_data
    coordinator = entry.runtime_data.coordinator

    # Create MovieSensor entities for all movies
    entities = [MovieSensor(movie) for movie in coordinator.data]
    async_add_entities(entities)
