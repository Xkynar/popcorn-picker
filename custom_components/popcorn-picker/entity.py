from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback


class MovieSensor(SensorEntity):
    """Representation of a movie sensor."""

    def __init__(self, movie):
        """Initialize the movie sensor."""
        self._movie = movie
        self._attr_name = movie["title"]
        self._attr_unique_id = movie["uuid"]
        self._attr_state = movie.get("rating", "N/A")

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        return {
            "genre": self._movie.get("genre"),
            "duration": self._movie.get("duration"),
        }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._state = self.coordinator.data
        self.async_write_ha_state()
