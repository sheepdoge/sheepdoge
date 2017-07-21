import os
import unittest

from sheepdog.config import DEFAULTS, Config


class ConfigTestCase(unittest.TestCase):
    def setUp(self, *args, **kwargs):
        super(ConfigTestCase, self).setUp(*args, **kwargs)

        self._only_default_config = Config()

    def test_config_hierarchy_default_final_option(self):
        """Test if we specify no additional config, we'll return all default
        values.
        """
        for field, default_value in DEFAULTS.iteritems():
            self.assertEqual(self._only_default_config.get(field),
                             default_value)

    def test_calculated_configurations(self):
        """Test the configurations we calculate on the fly based on other
        configuration values.
        """
        current_directory = os.path.realpath('.')

        self.assertEqual(self._only_default_config.get('abs_pupfile_dir'),
                         current_directory)
        self.assertEqual(self._only_default_config.get('abs_kennel_roles_dir'),
                         os.path.join(current_directory, DEFAULTS['kennel_roles_path']))
