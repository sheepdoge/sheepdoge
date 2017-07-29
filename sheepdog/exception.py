class SheepdogException(Exception):
    pass


class SheepdogCLIImproperArgumentsException(SheepdogException):
    pass


class SheepdogConfigurationAlreadyInitializedException(SheepdogException):
    pass


class SheepdogConfigurationNotInitializedException(SheepdogException):
    pass


class SheepdogInvalidPupTypeException(SheepdogException):
    pass


class SheepdogKennelRunException(SheepdogException):
    pass


class SheepdogRunActionException(SheepdogException):
    pass
