class CollectorError(Exception):
    """Base Collector exception."""


class CollectorValidationError(CollectorError):
    """Raised when input fails Collector validation."""


class CollectorConflictError(CollectorError):
    """Raised when an identity conflict is detected."""