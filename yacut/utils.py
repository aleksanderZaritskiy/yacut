import re

from .constants import PATTERN


def valid_custom_id(custom_id):
    return not re.match(PATTERN, custom_id)
