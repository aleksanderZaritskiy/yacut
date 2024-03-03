import re


def valid_custom_id(custom_id):
    return len(custom_id) > 16 or not re.match("^[a-zA-Z0-9]+$", custom_id)
