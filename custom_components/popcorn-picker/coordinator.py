from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import HomeAssistant
import asyncio
import datetime
import logging

_LOGGER = logging.getLogger(__name__)


class PopcornCoordinator(DataUpdateCoordinator):
    """Coordinator to fetch and update movie data."""

    def __init__(self, hass: HomeAssistant):
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Popcorn Picker Coordinator",
            update_interval=datetime.timedelta(seconds=30),
            always_update=True,
        )
        self.data = []

    async def _async_update_data(self):
        """Fetch data from APIs."""
        # Mock API data - Replace with real API calls
        mock_movies = [
            {
                "uuid": "1",
                "title": "Movie A",
                "rating": "85%",
                "genre": "Drama",
                "duration": "120",
            },
            {
                "uuid": "2",
                "title": "Movie B",
                "rating": "92%",
                "genre": "Action",
                "duration": "110",
            },
        ]
        await asyncio.sleep(1)  # Simulate API call delay
        return mock_movies
