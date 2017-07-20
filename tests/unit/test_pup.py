import os
import shutil
import tempfile
import unittest

from sheepdog.action.install import InstallDirectories
from sheepdog.pup import FsPup, GalaxyPup, GitPup, Pup, PupfileEntry


class PupTestCase(unittest.TestCase):
    def test_parse_text_into_entries(self):
        """Test we parse the pupfile into the appropriate data structures from
        which to create the `Pup` instances.
        """
        pupfile_contents = """
---
- { name: "sheepdog.pup-base", location: "fs+../../pups/pup-base" }
- { name: "sheepdog.pup-base", location: "git+https://github.com/mattjmcnaughton/pup-base.git" }
- { name: "sheepdog.pup-base", location: "galaxy+sheepdog.pup-base" }
        """

        expected_entries = [
            PupfileEntry(name='sheepdog.pup-base', path='../../pups/pup-base',
                         pup_type='fs'),
            PupfileEntry(name='sheepdog.pup-base',
                         path='https://github.com/mattjmcnaughton/pup-base.git',
                         pup_type='git'),
            PupfileEntry(name='sheepdog.pup-base',
                         path='sheepdog.pup-base',
                         pup_type='galaxy')
        ]

        self.assertEqual(Pup.parse_text_into_entries(pupfile_contents),
                         expected_entries)

    def test_create_from_entries(self):
        """Test we transform the `PupfileEntry` instances into popular instances
        of `Pup` subclasses.
        """
        pupfile_entries = [
            PupfileEntry(name='sheepdog.pup-base', path='../../pups/pup-base',
                         pup_type='fs'),
            PupfileEntry(name='sheepdog.pup-base',
                         path='https://github.com/mattjmcnaughton/pup-base.git',
                         pup_type='git'),
            PupfileEntry(name='sheepdog.pup-base',
                         path='sheepdog.pup-base',
                         pup_type='galaxy')
        ]

        expected_pups = [
            FsPup('sheepdog.pup-base', '../../pups/pup-base'),
            GitPup('sheepdog.pup-base',
                   'https://github.com/mattjmcnaughton/pup-base.git'),
            GalaxyPup('sheepdog.pup-base', 'sheepdog.pup-base')
        ]

        actual_pup_dicts = [pup.to_dict() for pup in Pup.create_from_entries(pupfile_entries)]
        expected_pup_dicts = [pup.to_dict() for pup in expected_pups]

        self.assertEqual(actual_pup_dicts, expected_pup_dicts)


class FsPupTestCase(unittest.TestCase):
    def setUp(self, *args, **kwargs):
        super(FsPupTestCase, self).setUp(*args, **kwargs)

        dir_root, kennel_roles_dir, pupfile_dir = self._create_test_fs()

        self._dir_root = dir_root
        self._kennels_roles_dir = kennel_roles_dir
        self._pupfile_dir = pupfile_dir

    @staticmethod
    def _create_test_fs():
        dir_root = tempfile.mkdtemp()
        pupfile_dir = dir_root

        kennel_roles_dir = os.path.join(dir_root, '.kennels')
        os.mkdir(kennel_roles_dir)

        return dir_root, kennel_roles_dir, pupfile_dir

    def tearDown(self, *args, **kwargs):
        super(FsPupTestCase, self).tearDown(*args, **kwargs)

        if os.path.isdir(self._dir_root):
            shutil.rmtree(self._dir_root)

    def test_install_pup_no_dependencies(self):
        no_dep_pup = self._create_pup('sheepdog.no-dependencies-pup')

        install_dirs = InstallDirectories(
            pupfile_dir=self._pupfile_dir,
            kennel_roles_dir=self._kennels_roles_dir
        )
        no_dep_pup.install(install_dirs)

        self._assert_pup_installed(no_dep_pup)

    def _create_pup(self, name, python_dependencies=None,
                    role_dependencies=None):
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

    def _assert_pup_installed(self, pup):
        expected_pup_location = os.path.join(self._kennels_roles_dir, pup._name)
        pup_copy_exists_in_kennel = os.path.isdir(expected_pup_location)

        self.assertTrue(pup_copy_exists_in_kennel)

