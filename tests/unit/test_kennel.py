import mock
import os
import tempfile
import unittest

from sheepdoge.config import Config
from sheepdoge.kennel import Kennel, KennelRunModes


class KennelTestCase(unittest.TestCase):
    def setUp(self, *args, **kwargs):
        super(KennelTestCase, self).setUp(*args, **kwargs)

        Config.clear_config_singleton()
        Config.initialize_config_singleton()

    def test_refresh_roles_dir_exists(self):
        """Test `refresh_roles` properly refreshes the kennel roles path
        when the kennel roles dir already exists."""
        mock_kennel_path = tempfile.mkdtemp()
        os.mkdir(os.path.join(mock_kennel_path, 'pup-test'))

        Kennel.refresh_roles(mock_kennel_path)

        self.assertEqual(os.listdir(mock_kennel_path), [])
        self.assertTrue(os.path.isdir(mock_kennel_path))

    # @TODO(mattjmcnaughton) Consider using dependency injection for
    # `ShellRunner` instead of patching `subprocess.check_call`.
    @mock.patch('subprocess.check_call')
    def test_kennel_run(self, mock_check_call):
        """Test running the kennel. We only test that it passes the correct
        arguments to `subprocess.check_call`. We rely on the integration
        tests for checking the playbook ran successfully.
        """
        kennel = Kennel(KennelRunModes.NORMAL)
        kennel.run()

        self.assertEqual(mock_check_call.call_count, 1)

        check_call_args, check_call_kwargs = mock_check_call.call_args
        ansible_playbook_cmd = check_call_args[0]

        for expected_arg in {'ansible-playbook',
                             'kennel.yml',
                             '--skip-tags="bootstrap"'}:
            self.assertIn(expected_arg, ansible_playbook_cmd)

        self.assertTrue(check_call_kwargs['shell'])
        self.assertIn('ANSIBLE_ROLES_PATH', check_call_kwargs['env'])

    @mock.patch('subprocess.check_call')
    def test_kennel_run_normal_proper_tags(self, mock_check_call):
        """Test we pass the correct tags parameters to ansible-playbook in
        the normal run.
        """
        kennel = Kennel(KennelRunModes.NORMAL)
        kennel.run()

        self.assertEqual(mock_check_call.call_count, 1)

        check_call_args, check_call_kwargs = mock_check_call.call_args
        ansible_playbook_cmd = check_call_args[0]

        self.assertIn('--skip-tags="bootstrap"', ansible_playbook_cmd)

    @mock.patch('subprocess.check_call')
    def test_kennel_run_bootstrap_proper_tags(self, mock_check_call):
        """Test we pass the correct tags parameters to ansible-playbook in
        the bootstrap run.
        """
        kennel = Kennel(KennelRunModes.BOOTSTRAP)
        kennel.run()

        self.assertEqual(mock_check_call.call_count, 1)

        check_call_args, check_call_kwargs = mock_check_call.call_args
        ansible_playbook_cmd = check_call_args[0]

        self.assertNotIn('tags', ansible_playbook_cmd)

    @mock.patch('subprocess.check_call')
    def test_kennel_run_cron_proper_tags(self, mock_check_call):
        """Test we pass the correct tags parameters to ansible-playbook in
        the cron run.
        """
        kennel = Kennel(KennelRunModes.CRON)
        kennel.run()

        self.assertEqual(mock_check_call.call_count, 1)

        check_call_args, check_call_kwargs = mock_check_call.call_args
        ansible_playbook_cmd = check_call_args[0]

        self.assertIn('--tags="cron"', ansible_playbook_cmd)

    @mock.patch('subprocess.check_call')
    def test_kennel_run_include_vault_password_file(self, mock_check_call):
        """Test that we do attempt to pass a vault password file to ansible
        when we have configured one.
        """
        Config.clear_config_singleton()
        Config.initialize_config_singleton(config_options={
            'vault_password_file': '/tmp/fake-password.txt'
        })

        kennel = Kennel(KennelRunModes.NORMAL)
        kennel.run()

        self.assertEqual(mock_check_call.call_count, 1)

        check_call_args, check_call_kwargs = mock_check_call.call_args
        ansible_playbook_cmd = check_call_args[0]

        self.assertTrue('--vault-password-file' in ansible_playbook_cmd)

    @mock.patch('subprocess.check_call')
    def test_kennel_run_not_include_vault_password_file(self, mock_check_call):
        """Test that we don't attempt to pass a vault password file to ansible
        when we haven't configured one.
        """
        kennel = Kennel(KennelRunModes.NORMAL)
        kennel.run()

        self.assertEqual(mock_check_call.call_count, 1)

        check_call_args, check_call_kwargs = mock_check_call.call_args
        ansible_playbook_cmd = check_call_args[0]

        self.assertFalse('--vault-password-file' in ansible_playbook_cmd)
