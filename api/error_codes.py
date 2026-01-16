"""FavQs API Error Codes."""
from enum import IntEnum


class ErrorCode(IntEnum):
    """API error codes."""
    NO_SESSION = 20
    INVALID_CREDENTIALS = 21
    INACTIVE_ACCOUNT = 22
    MISSING_CREDENTIALS = 23
    USER_NOT_FOUND = 30
    SESSION_EXISTS = 31
    VALIDATION_ERROR = 32
    INVALID_TOKEN = 33


class Msg:
    """Error message patterns."""
    EMAIL_INVALID = "not a valid email"
    EMAIL_TAKEN = "has already been taken"
    PWD_SHORT = "too short"
    PWD_LONG = "too long"
    LOGIN_LONG = "too long"
    LOGIN_TAKEN = "already been taken"
    LOGIN_CHARS = "username"
    SESSION = "session"
    PIC_INVALID = "not a valid pic"
    UPDATED = "successfully updated"
