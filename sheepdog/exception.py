class SheepdogException(Exception):
    pass


class SheepdogAnsibleDependenciesInstallException(SheepdogException):
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


class SheepdogPythonDependenciesInstallException(SheepdogException):
    pass


class SheepdogRunActionException(SheepdogException):
    pass
