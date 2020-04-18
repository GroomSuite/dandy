class UnsuportedRelationTypeError(Exception):
    """Raised when defined type of relation is not supported"""
    pass


class ModelDoesNotExistError(Exception):
    """Raised when defined model for relation does not exist"""
    pass


class ModelInstanceDoesNotExistError(Exception):
    """Raised when model instance does not exist"""
    pass


class IdValueNotFoundError(Exception):
    """Raised when id value not found"""
    pass
