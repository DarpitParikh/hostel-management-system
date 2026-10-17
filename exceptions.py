"""Our own exception classes."""


class HostelError(Exception):
    """Base class for all our errors."""


class InvalidInputError(HostelError):
    """Wrong or missing input."""


class RoomFullError(HostelError):
    """No bed left in the room."""
