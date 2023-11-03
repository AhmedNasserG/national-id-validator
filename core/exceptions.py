class InvalidNationalIdException(Exception):
    """
    Invalid national ID exception.
    """

    def __init__(self, message="Invalid national ID"):
        self.message = message
        super().__init__(self.message)
