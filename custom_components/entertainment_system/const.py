""" Constants related to Entertainment System."""
import sys


CONF_AVAILABILITY = "availability"
CONF_DISPLAY = "display"
CONF_POWER = "power"
CONF_TURN_ON_ACTION = "turn_on_action"
CONF_TURN_OFF_ACTION = "turn_off_action"
CONF_POWER_STATE_TEMPLATE = "power_state_template"
CONF_MEDIA_SOURCES = "media_sources"
CONF_MEDIA_PLAYER = "media_player"
CONF_REMOTE = "remote"
CONF_SPEAKER = "speaker"
CONF_AMBIANCE = "ambiance"
CONF_BRIGHTNESS = "brightness"
CONF_INTENSITY = "intensity"
CONF_BRIGHTNESS_SCALE = "brightness_scale"
CONF_SORT_ORDER = "sort_order"

DEFAULT_BRIGHTNESS_SCALE = (0, 255)

EPSILON = sys.float_info.epsilon

ATTR_OLD_STATE = 'old_state'
ATTR_NEW_STATE = 'new_state'
ATTR_ATTRIBUTES = 'attributes'

SCRIPT_POWER_TEMPLATE = ('service: homeassistant.{action}\n'
                         'data_template:\n'
                         '  entity_id: {entity_id}')
