class SheepdogException(Exception):
    pass


class SheepdogConfigurationAlreadyInitializedException(SheepdogException):
    pass


class SheepdogConfigurationNotInitializedException(SheepdogException):
    pass


class SheepdogInvalidPupTypeException(SheepdogException):
    pass


class SheepdogShellRunnerException(SheepdogException):
    pass
