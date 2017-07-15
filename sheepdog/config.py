"""Configuration parser for any command line options/files passed to
sheepdog.
"""

class Config(object):
    """Sheepdog configuration parser.

    :param config_file: The path to the `kennel.cfg` file sheepdog will use for
    this operation.
    :type config_file: str
    """
    def __init__(self, config_file=None):
        self._config_file = config_file
