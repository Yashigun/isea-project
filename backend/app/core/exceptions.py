class AuthenticationError(Exception):
    """Base exception for authentication failures."""
    pass


class InvalidTokenError(Exception):
    """Raised when a token is invalid, expired, or malformed."""
    pass


class AccountLockedError(Exception):
    """Raised when an account is temporarily locked due to too many failed attempts."""
    pass