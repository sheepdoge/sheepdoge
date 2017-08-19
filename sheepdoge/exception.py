class SheepdogeException(Exception):
    pass


class SheepdogeConfigurationAlreadyInitializedException(SheepdogeException):
    pass


class SheepdogeConfigurationNotInitializedException(SheepdogeException):
    pass


class SheepdogeInvalidPupTypeException(SheepdogeException):
    pass


class SheepdogeShellRunnerException(SheepdogeException):
    pass
