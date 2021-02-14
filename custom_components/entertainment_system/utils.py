"""Utility functionality for Entertainment System integration."""
from typing import (
    Any,
    Callable,
    Optional,
    Tuple,
    Union,
    )

from homeassistant.const import EVENT_STATE_CHANGED
from homeassistant.core import Event
from homeassistant.helpers.event import (
    async_track_state_change_event,
    )
from homeassistant.helpers.typing import HomeAssistantType

from .const import (
    ATTR_ATTRIBUTES,
    ATTR_NEW_STATE,
    ATTR_OLD_STATE,
    ATTR_STATE,
    EPSILON,
    )


def are_different(value1: Optional, value2: Optional) -> bool:
    """Determines where the two given values are considered divergent."""
    if (value1 is None or value2 is None) and value1 != value2:
        return True
    if isinstance(value1, str) and isinstance(value2, str):
        return value1 == value2
    # TODO: Units, other conversions
    return are_divergent(value1, value2)


def are_divergent(value1: Optional[Union[int, float]], value2: Optional[Union[int, float]]) -> bool:
    """Determines whether the two given values are within epsilon."""
    if (value2 is None or value2 is None) and value1 != value2:
        return True
    return abs(value1 - value2) > EPSILON


def map_value_to_range(
        input_value: Union[int, float],
        input_range: Tuple[Union[int, float], Union[int, float]],
        output_range: Tuple[Union[int, float], Union[int, float]]):
    """Scales the input value proportionately to match the output range."""
    input_spread = input_range[1] - input_range[0]
    output_spread = output_range[1] - output_range[0]

    value_scaled = float(input_value - input_range[0]) / float(input_spread)

    return output_range[0] + (value_scaled * output_spread)


def track_state(hass: HomeAssistantType,
                entity_id: str,
                state_change_callback: Callable[[str, Optional[Any], Optional[Any]], Optional[Any]],
                attribute: Optional[str] = None) -> Callable:
    """Track state/attribute changes for entity."""

    def _on_state_changed(event: Event):
        """Intermediate handler to facilitate logic in the entity handlers."""
        if event.event_type != EVENT_STATE_CHANGED:
            return
        if not event.data or ATTR_NEW_STATE not in event.data:
            return

        new_state_obj = event.data.get(ATTR_NEW_STATE, {})
        old_state_obj = event.data.get(ATTR_OLD_STATE, {})

        if not attribute:
            new_state = new_state_obj.get(ATTR_STATE, None)
            old_state = old_state_obj.get(ATTR_STATE, None)
        else:
            new_state = new_state_obj.get(ATTR_ATTRIBUTES, {}).get(attribute, None)
            old_state = old_state_obj.get(ATTR_ATTRIBUTES, {}).get(attribute, None)

        if not are_different(new_state, old_state):
            return

        state_change_callback(entity_id,
                              new_state,
                              old_state)

    return async_track_state_change_event(hass,
                                          entity_ids=entity_id,
                                          action=_on_state_changed)
