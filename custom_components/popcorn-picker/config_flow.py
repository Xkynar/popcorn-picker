from homeassistant import config_entries
from .const import DOMAIN


class PopcornPickerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Popcorn Picker."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle user setup."""
        if user_input is not None:
            return self.async_create_entry(title="Popcorn Picker", data=user_input)

        return self.async_show_form(step_id="user")
