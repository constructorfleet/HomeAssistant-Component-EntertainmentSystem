"""Entertainment System media source helper class."""
import logging
from typing import (
    Iterable,
    Optional,
    Union,
    )

from homeassistant.components.media_player import (
    SUPPORT_BROWSE_MEDIA,
    SUPPORT_CLEAR_PLAYLIST,
    SUPPORT_NEXT_TRACK,
    SUPPORT_PAUSE,
    SUPPORT_PLAY,
    SUPPORT_PLAY_MEDIA,
    SUPPORT_PREVIOUS_TRACK,
    SUPPORT_REPEAT_SET,
    SUPPORT_SEEK,
    SUPPORT_SELECT_SOUND_MODE,
    SUPPORT_SELECT_SOURCE,
    SUPPORT_SHUFFLE_SET,
    SUPPORT_STOP,
    SUPPORT_TURN_OFF,
    SUPPORT_TURN_ON,
    SUPPORT_VOLUME_MUTE,
    SUPPORT_VOLUME_SET,
    )
from homeassistant.core import valid_entity_id
from homeassistant.helpers.entity_registry import async_get_registry
from homeassistant.helpers.typing import HomeAssistantType

from .const import (
    CONF_AMBIANCE,
    CONF_BRIGHTNESS,
    CONF_BRIGHTNESS_SCALE,
    CONF_INTENSITY,
    CONF_MEDIA_PLAYER,
    CONF_REMOTE,
    CONF_SORT_ORDER,
    CONF_SPEAKER,
    )

_LOGGER = logging.getLogger(__name__)


class Ambiance:
    """Class containing handlers and configuration for ambiance related to media source."""

    def __init__(self,
                 hass: HomeAssistantType,
                 ambiance_config: dict):
        """Initialize ambiance class."""
        self._hass = hass
        self._config = ambiance_config
        self._brightness_entity = None
        self._brightness_scale = ambiance_config.get(CONF_BRIGHTNESS_SCALE)
        self._intensity_entity = None

    async def async_added_to_hass(self):
        """Retrieve relative entities and set appropriate properties."""
        entity_registry = await async_get_registry(self._hass)

        self._brightness_entity = entity_registry.async_get(self._config[CONF_BRIGHTNESS])
        if CONF_INTENSITY in self._config:
            self._intensity_entity = entity_registry.async_get(self._config[CONF_INTENSITY])


class MediaSource:
    """Class containing handlers and configurations for a given media source."""

    def __init__(self,
                 hass: HomeAssistantType,
                 media_source_config: Union[str, dict]):
        """Initialize media source class."""
        self._hass = hass
        self._config = media_source_config
        self._media_player = None
        self._remote = None
        self._speaker = None
        self._ambiance = media_source_config.get(CONF_AMBIANCE, None)
        self._sort_order = 1 if isinstance(media_source_config, str) else media_source_config[CONF_SORT_ORDER]

    async def async_added_to_hass(self):
        """Retrieve relative entities and set appropriate properties."""
        entity_registry = await async_get_registry(self._hass)

        if valid_entity_id(self._config):
            self._media_player = entity_registry.async_get(self._config)
            self._remote = None
            self._speaker = None
            self._ambiance = None
        else:
            self._media_player = entity_registry.async_get(self._config[CONF_MEDIA_PLAYER])
            if CONF_REMOTE in self._config:
                self._remote = entity_registry.async_get(self._config[CONF_REMOTE])
            if CONF_SPEAKER in self._config:
                self._speaker = entity_registry.async_get(self._config[CONF_SPEAKER])

        if self._ambiance:
            await self._ambiance.async_added_to_hass()

    @property
    def supported_features(self):
        """Flag media player features that are supported."""
        return self._media_player.supported_features | (
                0
                if self._speaker is not None
                else self._speaker.supported_features)

    async def async_turn_on(self):
        await self.relay_command(
                SUPPORT_TURN_ON,
                "turn_on")

    async def async_turn_off(self):
        await self.relay_command(
                SUPPORT_TURN_OFF,
                "turn_off")

    async def async_mute_volume(self, mute):
        await self.relay_command(
                SUPPORT_VOLUME_MUTE,
                "mute_volume",
                mute,
                devices=["speaker", "media_player"])

    async def async_set_volume_level(self, volume):
        await self.relay_command(
                SUPPORT_VOLUME_SET,
                "set_volume_level",
                volume,
                devices=["speaker", "media_player"])

    async def async_media_play(self):
        await self.relay_command(
                SUPPORT_PLAY,
                "media_play")

    async def async_media_pause(self):
        await self.relay_command(
                SUPPORT_PAUSE,
                "media_pause")

    async def async_media_stop(self):
        await self.relay_command(
                SUPPORT_STOP,
                "media_stop")

    async def async_media_previous_track(self):
        await self.relay_command(
                SUPPORT_PREVIOUS_TRACK,
                "media_previous_track")

    async def async_media_next_track(self):
        await self.relay_command(
                SUPPORT_NEXT_TRACK,
                "media_next_track")

    async def async_media_seek(self, position):
        await self.relay_command(
                SUPPORT_SEEK,
                "media_seek")

    async def async_play_media(self, media_type, media_id, **kwargs):
        await self.relay_command(
                SUPPORT_PLAY_MEDIA,
                "play_media",
                media_type=media_type,
                media_id=media_id,
                **kwargs)

    async def async_select_source(self, source):
        await self.relay_command(
                SUPPORT_SELECT_SOURCE,
                "select_source",
                source)

    async def async_select_sound_mode(self, sound_mode):
        await self.relay_command(
                SUPPORT_SELECT_SOUND_MODE,
                "select_sound_mode",
                sound_mode)

    async def async_clear_playlist(self):
        await self.relay_command(
                SUPPORT_CLEAR_PLAYLIST,
                "clear_playlist")

    async def async_set_shuffle(self, shuffle):
        await self.relay_command(
                SUPPORT_SHUFFLE_SET,
                "set_shuffle",
                shuffle)

    async def async_set_repeat(self, repeat):
        await self.relay_command(
                SUPPORT_REPEAT_SET,
                "set_repeat",
                repeat)

    async def async_browse_media(self,
                                 media_content_type: Optional[str] = None,
                                 media_content_id: Optional[str] = None) -> "BrowseMedia":
        return await self.relay_command(
                SUPPORT_BROWSE_MEDIA,
                "browse_media",
                media_content_type=media_content_type,
                media_content_id=media_content_id)



    async def relay_command(self,
                            feature: int,
                            command: str,
                            *command_args,
                            devices: Iterable = None,
                            **command_kwargs) -> Optional:
        for prop in [getattr(self, device, None) for device in devices or ["media_player"]]:
            if prop is None:
                continue
            if prop.supported_features & feature:
                method = getattr(prop, f"async_{command}", None)
                if method:
                    return await method(*command_args, **command_kwargs)
                method = getattr(prop, command, None)
                if method:
                    return await self._hass.async_add_executor_job(method, *command_args, **command_kwargs)
                _LOGGER.warning(f"{prop.entity_id} does not have an implementation for '{command}'")
            else:
                _LOGGER.warning(f"{prop.entity_id} does not support '{command}'")

        _LOGGER.warning(f"Unable to perform {command}")
        return None
