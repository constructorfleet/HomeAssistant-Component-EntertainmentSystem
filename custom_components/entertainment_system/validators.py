"""Extra validators for Entertainment System integration."""
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from .const import (
    CONF_DEFAULT,
    CONF_MEDIA_PLAYER,
    CONF_POWER_STATE_TEMPLATE,
    CONF_REMOTE,
    CONF_TURN_OFF_ACTION,
    CONF_TURN_ON_ACTION,
    MEDIA_PLAYER_DOMAIN,
    REMOTE_DOMAIN,
    )

POWER_CONFIG_SCHEMA = vol.Any(
        cv.entity_id,
        vol.Schema({
                vol.Optional(CONF_TURN_ON_ACTION): cv.SCRIPT_SCHEMA,
                vol.Optional(CONF_TURN_OFF_ACTION): cv.SCRIPT_SCHEMA,
                vol.Optional(CONF_POWER_STATE_TEMPLATE): cv.template
                })
        )


def entity_id_with_domain(domain):
    """Validates that the given string is a valid entity id and part of the specified domain."""

    def _validate(value):
        entity_id = cv.entity_id(value)
        if entity_id.split(".")[0] != domain:
            raise vol.Invalid(f"{value} is not part of the domain {domain}")
        return entity_id

    return _validate


MEDIA_SOURCE_CONFIG_SCHEMA = vol.Any(
        entity_id_with_domain(MEDIA_PLAYER_DOMAIN),
        vol.Schema({
                vol.Required(CONF_MEDIA_PLAYER): entity_id_with_domain(MEDIA_PLAYER_DOMAIN),
                vol.Optional(CONF_DEFAULT, default=False): cv.boolean,
                vol.Optional(CONF_REMOTE): entity_id_with_domain(REMOTE_DOMAIN)
                }))
