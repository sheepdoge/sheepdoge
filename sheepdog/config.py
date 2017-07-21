"""Configuration parser for any command line options/files passed to
sheepdog.
"""

import os

DEFAULTS = {
    'pupfile_path': 'pupfile.yml',
    'kennel_roles_path': '.kennel_roles'
}


class SheepdogConfigurationNotFoundException(Exception):
    pass


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
        first_order_config_preferences = [
            DEFAULTS
        ]

        for config in first_order_config_preferences:
            if field in config:
                return config[field]

        second_order_config_preferences = [
            self._calculate_configuration()
        ]

        for config in second_order_config_preferences:
            if field in config:
                return config[field]

        raise SheepdogConfigurationNotFoundException(
            '{} does not exit in configuration'.format(field))

    def _calculate_configuration(self):
        """Configuration values we use throughout the application, but don't
        have the user specify.

        Importantly, this can only access "first-order" config preferences,
        or else we'll have infinite recursion.
        """
        pupfile_path = self.get('pupfile_path')
        pupfile_dir = os.path.dirname(os.path.realpath(pupfile_path))

        kennel_roles_path = self.get('kennel_roles_path')
        abs_kennel_roles_dir = os.path.realpath(kennel_roles_path)

        return {
            'abs_pupfile_dir': pupfile_dir,
            'abs_kennel_roles_dir': abs_kennel_roles_dir
        }
