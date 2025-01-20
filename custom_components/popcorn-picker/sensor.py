"""Popcorn Picker sensor platform."""

import datetime
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .const import DOMAIN, RATING_UPDATE_INTERVAL
from .coordinator import MovieSensorCoordinator
from .types import Movie

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = datetime.timedelta(seconds=RATING_UPDATE_INTERVAL)


async def async_setup_platform(hass: HomeAssistant, config, async_add_entities):
    """Set up sensors from YAML."""
    if DOMAIN not in hass.data:
        return

    # Get the API from the YAML setup
    api = hass.data[DOMAIN]["yaml"]

    # Fetch initial movie list
    movies = await api.fetch_movies()
    sensors = [MovieSensorEntity(api, movie) for movie in movies]
    async_add_entities(sensors, update_before_add=True)


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up sensors from UI."""
    api = hass.data[DOMAIN][config_entry.entry_id]

    # Create the coordinator
    coordinator = MovieSensorCoordinator(hass, api)
    hass.data[DOMAIN]["coordinator"] = coordinator

    # Perform the first update
    await coordinator.async_refresh()

    # Track the existing sensors
    existing_sensors: dict[int, MovieSensorEntity] = {}

    # Handle dynamic entity updates
    async def update_entities():
        """Update sensors dynamically based on new data."""
        new_movie_ids: set[int] = {movie.uuid for movie in coordinator.data or []}
        current_movie_ids: set[int] = set(existing_sensors.keys())

        # Add new sensors
        to_add = new_movie_ids - current_movie_ids
        new_entities = []
        for movie_id in to_add:
            movie = next(movie for movie in coordinator.data if movie.uuid == movie_id)
            sensor = MovieSensorEntity(coordinator, movie)
            existing_sensors[movie_id] = sensor
            new_entities.append(sensor)
        if new_entities:
            async_add_entities(new_entities)

        # Remove obsolete sensors
        to_remove = current_movie_ids - new_movie_ids
        for movie_id in to_remove:
            sensor = existing_sensors.pop(movie_id)

            # Remove the entity from Home Assistant
            entity_registry = er.async_get(hass)
            entity_registry.async_remove(sensor.entity_id)

            # Optionally call the entity's async_remove method
            await sensor.async_remove()

    # Run the update_entities function after every coordinator update
    coordinator.async_add_listener(lambda: hass.async_create_task(update_entities()))

    # Initial entity update
    await update_entities()


class MovieSensorEntity(SensorEntity):
    """Representation of a movie sensor."""

    def __init__(self, coordinator: MovieSensorCoordinator, movie: Movie) -> None:
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._movie = movie
        self._rating = None
        self._attr_name = f"movie_{movie.originaltitle}"
        self._attr_unique_id = movie.uuid

    async def async_update(self):
        """Fetch additional data for the movie."""
        movie_name = self._movie.originaltitle
        movie_date = datetime.datetime.strptime(
            self._movie.releasedate, "%Y-%m-%dT%H:%M"
        )
        rating = await self.coordinator.api.fetch_movie_details(
            movie_name, movie_date.year
        )
        self._rating = rating

    async def async_remove(self):
        """Remove the entity when it's no longer needed."""
        self.coordinator.existing_sensors.pop(self._movie["uuid"], None)
        await super().async_remove()

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._rating.criticsscore

    @property
    def extra_state_attributes(self):
        """Return extra state attributes."""
        return {
            "title": self._movie.originaltitle,
            "genre": self._movie.genre,
            "classification": self._movie.classification,
            "criticsrating": self._rating.criticsrating,
            "criticsscore": self._rating.criticsscore,
            "audiencerating": self._rating.audiencerating,
            "audiencescore": self._rating.audiencescore,
        }
