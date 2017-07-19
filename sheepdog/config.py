"""Configuration parser for any command line options/files passed to
sheepdog.
"""

DEFAULTS = {
    'pupfile_path': 'pupfile.yml',
    'kennel_roles_path': '.kennel_roles'
}

class Config(object):
    """Sheepdog configuration parser.

    Eventually sheepdog will read configuration from command line arguments,
    environment variables, a configuration file, and as a last resort, defaults.

    :param config_file: The path to the `kennel.cfg` file sheepdog will use for
    this operation.
    :type config_file: str
    """
    def __init__(self, config_file=None):
        self._config_file = config_file
        self._defaults = DEFAULTS

    def get(self, field):
        """Get a configuration value. Because we fall back to defaults, we
        guarantee a value will exist.

        :param field: The config field for which we want the value.
        :type field: str
        """
        return self._defaults[field]
