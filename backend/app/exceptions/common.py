class NotFoundException(Exception):
    """Exception to raise when an object is not found.

    Args:
        Exception (Exception): Base exception class.
    """

    def __init__(
        self,
        message="Not found",
    ):
        self.message = message
        super().__init__(self.message)
