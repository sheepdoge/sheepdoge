import unittest
from mock import MagicMock

from sheepdoge.config import Config
from sheepdoge.action.install import InstallAction, ParallelInstallAction


class InstallActionTestCase(unittest.TestCase):
    def setUp(self, *args, **kwargs):
        super(InstallActionTestCase, self).setUp(*args, **kwargs)

        Config.clear_config_singleton()
        Config.initialize_config_singleton()

    def test_install_action_installs_pups(self):
        self._test_install_action_installs_pups(InstallAction)

    def test_parallel_install_action_installs_pups(self):
        self._test_install_action_installs_pups(ParallelInstallAction)

    def _test_install_action_installs_pups(self, install_action_cls):
        mock_kennel_cls = MagicMock()

        individual_pup_mocks = [
            MagicMock() for _ in range(10)
        ]

        mock_pup_cls = MagicMock()
        mock_pup_cls.parse_pupfile_into_pups.return_value = individual_pup_mocks

        install_action = install_action_cls(kennel_cls=mock_kennel_cls,
                                            pup_cls=mock_pup_cls)

        install_action.run()

        mock_kennel_cls.refresh_roles.assert_called_once()
        for mock_pup in individual_pup_mocks:
            mock_pup.install.assert_called_once()

if __name__ == '__main__':
    unittest.main()
