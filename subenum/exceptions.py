class EnumeratorException(Exception):
    def __init__(self, message: str, code: int):
        super().__init__(message)
        self.code = code


class InvalidTargetSpecification(EnumeratorException):
    def __init__(self, message: str, code: int = 1):
        super().__init__(f"{self.__class__.__name__}: {message}", code)
