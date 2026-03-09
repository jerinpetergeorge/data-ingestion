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


class SorterError(GameBaseError):
    pass


class InvalidHierarchyError(SorterError):
    """
    Raised when the hierarchy string is malformed or contains cycles.
    e.g. 'A->B->A' or 'A' or 'A -> -> C'
    """

    pass


class UnknownEntityTypeError(SorterError):
    """
    Raised when a row's type value is not declared in the hierarchy.
    e.g. hierarchy is A->B->C but a row has type=D
    """

    pass


class WriterError(GameBaseError):
    pass


class WriterBackendNotSupportedError(WriterError):
    """
    Raised when the specified writer backend is not supported.
    """

    pass
