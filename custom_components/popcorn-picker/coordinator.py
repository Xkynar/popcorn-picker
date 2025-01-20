"""The Movie Sensor Coordinator."""

import datetime
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import MovieAPI
from .const import CATALOG_UPDATE_INTERVAL, DOMAIN
from .types import Movie

_LOGGER = logging.getLogger(__name__)


class MovieSensorCoordinator(DataUpdateCoordinator[list[Movie]]):
    """Coordinator to manage movie data updates."""

    def __init__(self, hass: HomeAssistant, api: MovieAPI) -> None:
        """Initialize the coordinator."""
        self.api = api
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=datetime.timedelta(seconds=CATALOG_UPDATE_INTERVAL),
        )

    async def _async_setup(self) -> None:
        pass

    async def _async_update_data(self) -> list[Movie]:
        """Fetch the latest movie list."""
        try:
            return await self.api.fetch_movies()
        except Exception as e:
            _LOGGER.error("Error fetching movies", extra={"error": e})
            return []
