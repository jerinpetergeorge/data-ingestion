class GameBaseError(Exception):
    def __init__(self, msg, *args, **kwargs):
        self.msg = msg

    def __repr__(self):
        return f"{self.__class__.__name__}({self.msg})"

    def __str__(self):
        return self.__repr__()


class ReaderError(GameBaseError):
    pass


class ReaderBackendNotSupportedError(ReaderError):
    """
    Raised when the specified reader backend is not supported.
    """

    pass


class FileReadError(ReaderError):
    """
    Raised when the input file cannot be opened or read.
    """

    pass


class ProcessorError(GameBaseError):
    pass


class InvalidKeySpecError(ProcessorError):
    """
    Raised when a key spec string is malformed.
    e.g. 'id:unknown_type' or 'badformat'
    """

    pass
