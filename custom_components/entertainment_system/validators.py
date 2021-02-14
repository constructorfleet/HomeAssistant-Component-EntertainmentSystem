"""Extra validators for Entertainment System integration."""
import sys

import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from .const import (
    CONF_AMBIANCE,
    CONF_BRIGHTNESS,
    CONF_BRIGHTNESS_SCALE,
    CONF_INTENSITY,
    CONF_MEDIA_PLAYER,
    CONF_MEDIA_SOURCES,
    CONF_NAME,
    CONF_POWER,
    CONF_POWER_STATE_TEMPLATE,
    CONF_REMOTE,
    CONF_SORT_ORDER,
    CONF_SPEAKER,
    CONF_TURN_OFF_ACTION,
    CONF_TURN_ON_ACTION,
    DEFAULT_BRIGHTNESS_SCALE,
    LIGHT_DOMAIN,
    MEDIA_PLAYER_DOMAIN,
    REMOTE_DOMAIN,
    )


def entity_id_with_domain(domain):
    """Validates that the given string is a valid entity id and part of the specified domain."""

    def _validate(value):
        entity_id = cv.entity_id(value)
        if entity_id.split(".")[0] != domain:
            raise vol.Invalid(f"{value} is not part of the domain {domain}")
        return entity_id

    return _validate


POWER_CONFIG_SCHEMA = vol.Any(
        cv.entity_id,
        vol.Schema({
                vol.Required(CONF_TURN_ON_ACTION): cv.SCRIPT_SCHEMA,
                vol.Required(CONF_TURN_OFF_ACTION): cv.SCRIPT_SCHEMA,
                vol.Required(CONF_POWER_STATE_TEMPLATE): cv.template
                })
        )
AMBIANCE_CONFIG_SCHEMA = vol.Schema({
        vol.Required(CONF_BRIGHTNESS): entity_id_with_domain(LIGHT_DOMAIN),
        vol.Optional(CONF_BRIGHTNESS_SCALE, default=DEFAULT_BRIGHTNESS_SCALE): vol.Schema(
                (
                        vol.All(vol.Coerce(float), vol.Range(0, 255)),
                        vol.All(vol.Coerce(float), vol.Range(0, 255)))),
        vol.Optional(CONF_INTENSITY): entity_id_with_domain(LIGHT_DOMAIN)
        })
MEDIA_SOURCE_CONFIG_SCHEMA = vol.Any(
        entity_id_with_domain(MEDIA_PLAYER_DOMAIN),
        vol.Schema({
                vol.Required(CONF_MEDIA_PLAYER): entity_id_with_domain(MEDIA_PLAYER_DOMAIN),
                vol.Optional(CONF_SORT_ORDER): vol.Range(1),
                vol.Optional(CONF_REMOTE): entity_id_with_domain(REMOTE_DOMAIN),
                vol.Optional(CONF_SPEAKER): entity_id_with_domain(MEDIA_PLAYER_DOMAIN),
                vol.Optional(CONF_AMBIANCE): AMBIANCE_CONFIG_SCHEMA
                }))

ENTERTAINMENT_SYSTEM_SCHEMA = vol.Schema({
        vol.Required(CONF_NAME): cv.string,
        vol.Required(CONF_POWER): POWER_CONFIG_SCHEMA,
        vol.Required(CONF_MEDIA_SOURCES): vol.Any(
                entity_id_with_domain(MEDIA_PLAYER_DOMAIN),
                vol.Schema({
                        cv.string: MEDIA_SOURCE_CONFIG_SCHEMA
                        })
                )
        })
