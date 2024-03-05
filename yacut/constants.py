import string

MIN_LENGHT = 1
SHORT_LENGTH = 16
PATTERN = f'^[a-zA-Z0-9]{{{MIN_LENGHT},{SHORT_LENGTH}}}$'
CHARS_FOR_BULD_URI = string.ascii_letters + string.digits
LENGTH_SHORT_URI = 6
ORIGINAL_LENGTH = 256
MAX_ITERATION_DEPT = 26 * 36 * 6
