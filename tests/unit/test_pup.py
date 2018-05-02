import mock
import os
import shutil
import tempfile
import unittest

from six import iteritems

from sheepdoge.config import Config
from sheepdoge.pup import (AnsibleDependencies, FsPup, GalaxyPup, GitPup,
                          Pup, PupDependencies, PupfileEntry,
                          PythonDependencies)


class PupTestCase(unittest.TestCase):
    def setUp(self, *args, **kwargs):
        super(PupTestCase, self).setUp(*args, **kwargs)

        Config.clear_config_singleton()
        Config.initialize_config_singleton()

    def test_parse_text_into_entries(self):
        """Test we parse the pupfile into the appropriate data structures from
        which to create the `Pup` instances.
        """
        pupfile_contents = """
---
- { name: "sheepdoge.pup-base", location: "fs+../../pups/pup-base" }
- { name: "sheepdoge.pup-base", location: "git+https://github.com/mattjmcnaughton/pup-base.git" }
- { name: "sheepdoge.pup-base", location: "galaxy+sheepdoge.pup-base" }
        """

        expected_entries = [
            PupfileEntry(name='sheepdoge.pup-base', path='../../pups/pup-base',
                         pup_type='fs'),
            PupfileEntry(name='sheepdoge.pup-base',
                         path='https://github.com/mattjmcnaughton/pup-base.git',
                         pup_type='git'),
            PupfileEntry(name='sheepdoge.pup-base',
                         path='sheepdoge.pup-base',
                         pup_type='galaxy')
        ]

        self.assertEqual(Pup.parse_text_into_entries(pupfile_contents),
                         expected_entries)

    def test_create_from_entries(self):
        """Test we transform the `PupfileEntry` instances into popular instances
        of `Pup` subclasses.
        """
        pupfile_entries = [
            PupfileEntry(name='sheepdoge.pup-base', path='../../pups/pup-base',
                         pup_type='fs'),
            PupfileEntry(name='sheepdoge.pup-base',
                         path='https://github.com/mattjmcnaughton/pup-base.git',
                         pup_type='git'),
            PupfileEntry(name='sheepdoge.pup-base',
                         path='sheepdoge.pup-base',
                         pup_type='galaxy')
        ]

        expected_pups = [
            FsPup('sheepdoge.pup-base', '../../pups/pup-base'),
            GitPup('sheepdoge.pup-base',
                   'https://github.com/mattjmcnaughton/pup-base.git'),
            GalaxyPup('sheepdoge.pup-base', 'sheepdoge.pup-base')
        ]

        actual_pup_dicts = [pup.to_dict() for pup in Pup.create_from_entries(pupfile_entries)]
        expected_pup_dicts = [pup.to_dict() for pup in expected_pups]

        self.assertEqual(actual_pup_dicts, expected_pup_dicts)


class BasePupTestCase(unittest.TestCase):
    def setUp(self, *args, **kwargs):
        super(BasePupTestCase, self).setUp(*args, **kwargs)

        dir_root, kennel_roles_dir, pupfile_dir = self._create_test_fs()

        self._dir_root = dir_root
        self._kennel_roles_dir = kennel_roles_dir
        self._pupfile_dir = pupfile_dir

        mock_config_options = {
            'kennel_roles_path': self._kennel_roles_dir,
            'pupfile_path': os.path.join(self._pupfile_dir, 'pupfile.yml')
        }

        Config.clear_config_singleton()
        Config.initialize_config_singleton(
            config_options=mock_config_options)

    @staticmethod
    def _create_test_fs():
        dir_root = tempfile.mkdtemp()
        pupfile_dir = dir_root

        kennel_roles_dir = os.path.join(dir_root, '.kennels')
        os.mkdir(kennel_roles_dir)

        return dir_root, kennel_roles_dir, pupfile_dir

    def tearDown(self, *args, **kwargs):
        super(BasePupTestCase, self).tearDown(*args, **kwargs)

        if os.path.isdir(self._dir_root):
            shutil.rmtree(self._dir_root)

    def _assert_pup_installed(self, pup):
        expected_pup_location = os.path.join(self._kennel_roles_dir, pup._name)
        pup_copy_exists_in_kennel = os.path.isdir(expected_pup_location)

        self.assertTrue(pup_copy_exists_in_kennel)


class FsPupTestCase(BasePupTestCase):
    def test_install_pup_no_dependencies(self):
        no_dep_pup = self._create_fs_pup('sheepdoge.no-dependencies-pup')
        no_dep_pup.install()

        self._assert_pup_installed(no_dep_pup)

    def _create_fs_pup(self, name):
        pups_dir = os.path.join(self._dir_root, 'pups')
        os.mkdir(pups_dir)

        name_suffix = name.split('.')[1]
        pup_dir = os.path.join(pups_dir, name_suffix)
        os.mkdir(pup_dir)

        scratch_file_in_pup_dir = os.path.join(pup_dir, 'README.md')
        with open(scratch_file_in_pup_dir, 'w') as scratch_file:
            scratch_file.write('test')

        relative_pup_path = os.path.join('.', 'pups', name_suffix)
        return FsPup(name, relative_pup_path)


class GitPupTestCase(BasePupTestCase):
    @unittest.skip('Tested in integration test.')
    def test_install_git_pup(self):
        pass


class GalaxyPupTestCase(BasePupTestCase):
    @unittest.skip('Tested in integration tests.')
    def test_install_galaxy_pup(self):
        pass


class PupDependenciesTestCase(unittest.TestCase):
    def setUp(self, *args, **kwargs):
        super(PupDependenciesTestCase, self).setUp(*args, **kwargs)

        Config.clear_config_singleton()
        Config.initialize_config_singleton()

    def test_create_from_dep_file_path(self):
        filename_to_expected_type = {
            'requirements.txt': PythonDependencies,
            'requirements.yml': AnsibleDependencies
        }

        for filename, expected_type in iteritems(filename_to_expected_type):
            self.assertIsInstance(
                PupDependencies.create_from_dep_file_path(filename),
                expected_type
            )


class PythonDependenciesTestCase(unittest.TestCase):
    def setUp(self, *args, **kwargs):
        super(PythonDependenciesTestCase, self).setUp(*args, **kwargs)

        Config.clear_config_singleton()
        Config.initialize_config_singleton()

    @mock.patch('subprocess.check_call')
    def test_install(self, mock_check_call):
        python_dep_file_path = '/tmp/requirements.txt'

        deps = PupDependencies.create_from_dep_file_path(python_dep_file_path)
        deps.install()

        self.assertEqual(mock_check_call.call_count, 1)

        check_call_args, check_call_kwargs = mock_check_call.call_args
        pip_cmd = check_call_args[0]

        for cmd_line in {'pip', '-r {}'.format(python_dep_file_path)}:
            self.assertIn(cmd_line, pip_cmd)


class AnsibleDependenciesTestCase(unittest.TestCase):
    def setUp(self, *args, **kwargs):
        super(AnsibleDependenciesTestCase, self).setUp(*args, **kwargs)

        Config.clear_config_singleton()
        Config.initialize_config_singleton()

    @mock.patch('subprocess.check_call')
    def test_install(self, mock_check_call):
        ansible_dep_file_path = '/tmp/requirements.yml'

        deps = PupDependencies.create_from_dep_file_path(ansible_dep_file_path)
        deps.install()

        self.assertEqual(mock_check_call.call_count, 1)

        check_call_args, check_call_kwargs = mock_check_call.call_args
        ansible_galaxy_cmd = check_call_args[0]

        config = Config.get_config_singleton()

        expected_cmds = {
            'ansible-galaxy',
            'install',
            '-r {}'.format(ansible_dep_file_path),
            '-p {}'.format(config.get('abs_kennel_roles_dir'))
        }

        for cmd_line in expected_cmds:
            self.assertIn(cmd_line, ansible_galaxy_cmd)

if __name__ == '__main__':
    unittest.main()
