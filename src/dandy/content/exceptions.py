class UnsuportedRelationTypeError(Exception):
    """Raised when defined type of relation is not supported"""
    pass


class ModelDoesNotExistError(Exception):
    """Raised when defined model for relation does not exist"""
    pass
