from configparser import ConfigParser, NoOptionError
import os

from sheepdoge.exception import (SheepdogeConfigurationAlreadyInitializedException,
                                 SheepdogeConfigurationNotInitializedException)


class KennelRunModes(object):
    # Include everything except bootstrap tasks
    NORMAL = 'normal'
    # Run all tasks (including bootstrap tasks)
    BOOTSTRAP = 'bootstrap'
    # Run only the nightly cron tasks
    CRON = 'cron'


RUN_MODE_TO_TAGS = {
    KennelRunModes.NORMAL: '--skip-tags="bootstrap"',
    KennelRunModes.BOOTSTRAP: '',
    KennelRunModes.CRON: '--tags="cron"'
}


DEFAULTS = {
    'kennel_playbook_path': 'kennel.yml',
    'kennel_roles_path': '.kennel_roles',
    'kennel_run_mode': KennelRunModes.NORMAL,
    'pupfile_path': 'pupfile.yml',
    'vault_password_file': '~/.sheepdoge/vault_password_file.txt'
}


class Config(object):
    """Config class for which there should only be one instance at anytime.
    Additionally, we can only set the config values during initialization.
    Multiple different classes can access this single instance at a time.
    """
    _config = None

    @classmethod
    def clear_config_singleton(cls):
        """Delete the current configuration singleton to allow the
        initialization of a new one. This method is predominantly used during test.
        """
        cls._config = None

    @classmethod
    def get_config_singleton(cls):
        """Return the current config singleton instance. We must initialize
        the singleton before calling this method.

        :return: The singleton instance.
        :rtype: Config
        """
        if cls._config is None:
            raise SheepdogeConfigurationNotInitializedException
        return cls._config

    @classmethod
    def initialize_config_singleton(cls, config_file_contents=None,
                                    config_options=None):
        """Initialize the config singleton with the proper values. If we
        specify no additional values during configuration, then the config
        will contain all defaults. We can, in priority order, pass in the
        contents of a *.cfg file and a dictionary of options. Typically we
        derive this dictionary of options from the command line.

        Finally, after setting all of the base configuration values,
        we compute additional configuration values which are useful
        throughout the program.

        :param config_file_contents: The str contents of the .cfg file
        containing kennel configuration.
        :type: str
        :param config_options: The dict specifying the highest priority
        configuration values.
        :type config_options: dict
        """
        if cls._config is not None:
            raise SheepdogeConfigurationAlreadyInitializedException()

        config_dict = {}

        cls._set_config_default_values(config_dict)

        if config_file_contents:
            cls._set_config_file_values(config_dict, config_file_contents)

        if config_options:
            cls._set_config_option_values(config_dict, config_options)

        cls._set_calculated_config_values(config_dict)

        config_instance = cls(config_dict)

        cls._config = config_instance

    @classmethod
    def _set_config_default_values(cls, config_dict):
        """Set defaults for all views here - they will be overwritten in the
        following steps if necessary.
        """
        config_dict.update(DEFAULTS)

    @classmethod
    def _set_config_file_values(cls, config_dict, config_file_contents):
        config_parser = ConfigParser()
        config_parser.read_string(config_file_contents.decode('utf-8'))

        kennel_cfg_section = 'kennel'

        for currently_defined_key in config_dict.keys():
            try:
                config_file_value = config_parser.get(kennel_cfg_section,
                                                      currently_defined_key)

                config_dict[currently_defined_key] = config_file_value
            except NoOptionError:
                pass # If the value isn't specified, skip

    @classmethod
    def _set_config_option_values(cls, config_dict, config_options):
        config_dict.update(config_options)

    @classmethod
    def _set_calculated_config_values(cls, config_dict):
        pupfile_path = config_dict['pupfile_path']
        pupfile_dir = os.path.dirname(os.path.realpath(pupfile_path))

        kennel_roles_path = config_dict['kennel_roles_path']
        abs_kennel_roles_dir = os.path.realpath(kennel_roles_path)

        calculated_config = {
            'abs_pupfile_dir': pupfile_dir,
            'abs_kennel_roles_dir': abs_kennel_roles_dir
        }

        config_dict.update(calculated_config)

    def __init__(self, config_dict):
        self._config_dict = config_dict

    def get(self, key):
        """Retrieve the value for the given configuration key.

        :param key: One of the available configuration options.
        :type key: str
        """
        return self._config_dict[key]
