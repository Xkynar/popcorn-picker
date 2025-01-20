import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, NAME


class PopcornPickerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for the Popcorn Picker Integration."""

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial setup."""
        if user_input is None:
            # Show form
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required("param1"): str,
                    }
                ),
            )

        # Validate input here

        # Save the config entry
        return self.async_create_entry(title=NAME, data=user_input)
