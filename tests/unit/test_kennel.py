import mock
import os
import tempfile
import unittest

from sheepdog.kennel import Kennel


class KennelTestCase(unittest.TestCase):
    def test_refresh_roles_dir_exists(self):
        """Test `refresh_roles` properly refreshes the kennel roles path
        when the kennel roles dir already exists."""
        mock_kennel_path = tempfile.mkdtemp()
        os.mkdir(os.path.join(mock_kennel_path, 'pup-test'))

        Kennel.refresh_roles(mock_kennel_path)

        self.assertEqual(os.listdir(mock_kennel_path), [])
        self.assertTrue(os.path.isdir(mock_kennel_path))

    @mock.patch('subprocess.check_call')
    def test_kennel_run(self, mock_check_call):
        """Test running the kennel. We only test that it passes the correct
        arguments to `subprocess.check_call`. We rely on the integration
        tests for checking the playbook ran successfully.
        """
        mock_kennel_playbook_path = 'mock_kennel.yml'
        mock_kennel_roles_path = '.mock_kennel_roles'
        mock_kennel_config = {
            'vault_password_file': 'mock_vault_password_file'
        }

        kennel = Kennel(mock_kennel_playbook_path, mock_kennel_roles_path,
                        mock_kennel_config)

        kennel.run()

        self.assertEqual(mock_check_call.call_count, 1)

        check_call_args, check_call_kwargs = mock_check_call.call_args
        ansible_playbook_cmd = check_call_args[0]

        for expected_arg in {'ansible-playbook',
                             'mock_kennel.yml',
                             '--vault-password-file=mock_vault_password_file'}:
            self.assertIn(expected_arg, ansible_playbook_cmd)

        self.assertTrue(check_call_kwargs['shell'])
        self.assertIn('ANSIBLE_ROLES_PATH', check_call_kwargs['env'])
