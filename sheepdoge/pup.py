from collections import namedtuple
from contextlib import contextmanager
import os
import shutil
import tempfile

import yaml

from sheepdoge.config import Config
from sheepdoge.exception import SheepdogeInvalidPupTypeException
from sheepdoge.utils import ShellRunner

# The character used in the `location` in the pupfile to split between
# `pup_type` and `path`.
LOCATION_SPLIT_CHAR = '+'

PupfileEntry = namedtuple('PupfileEntry', 'name path pup_type')


def _pup_types_to_classes():
    return {
        'fs': FsPup,
        'galaxy': GalaxyPup,
        'git': GitPup
    }


def _dependency_types_to_classes():
    return {
        'txt': PythonDependencies,
        'yml': AnsibleDependencies
    }


class Pup(object):
    """Container of all pup related logic. Contains both static methods as well
    as base methods inherited by the different types of pups.
    """

    PYTHON_DEP_FILE = 'requirements.txt'
    ANSIBLE_DEP_FILE = 'requirements.yml'

    @classmethod
    def parse_pupfile_into_pups(cls, pupfile_path):
        """Return a list of `Pup` objects for each pup we wish to install."""
        # Read in file and parse with yml
        with open(pupfile_path, 'r') as pupfile:
            entries_from_file = cls.parse_text_into_entries(pupfile.read())

        return cls.create_from_entries(entries_from_file)

    @classmethod
    def parse_text_into_entries(cls, file_contents):
        """Given the text of `pupfile.yml`, return the structured data we will
        iterate through to create individual `Pup` instances.

        :param file_contents: A string containing the contents of `pupfile.yml`.
        :type file_contents: str
        :return: A list of structured pupfile entries.
        :rtype: list of PupfileEntry
        """
        entries = []

        for dict_entry in yaml.load(file_contents):
            name = dict_entry['name']
            pup_type, path = cls._parse_location(dict_entry['location'])

            if pup_type not in _pup_types_to_classes().keys():
                err_msg = '{} is not a valid pup type.'.format(pup_type)
                raise SheepdogeInvalidPupTypeException(err_msg)
            entries.append(PupfileEntry(name=name, path=path, pup_type=pup_type))

        return entries

    @staticmethod
    def _parse_location(location):
        split_location = location.split(LOCATION_SPLIT_CHAR)

        return split_location[0], split_location[1]

    @classmethod
    def create_from_entries(cls, entries):
        """Create a pup based on a line in a `pupfile.yml`.

        Instantiates and returns a subclass of `Pup` for the specific type of
        pup we are installing (i.e. from local filesystem, git, ansible-galaxy).

        :param entries: The input entries from the parsed pupfile.
        :type entries: list of dict
        :return: The specific pup instances we are installing.
        :rtype: list of pup
        """
        pups = []

        for entry in entries:
            pup_cls = _pup_types_to_classes()[entry.pup_type]
            pup = pup_cls(entry.name, entry.path)
            pups.append(pup)

        return pups

    def __init__(self, name, path, config=None):
        self._name = name
        self._path = path
        self._pup_dependencies = []

        self._config = config or Config.get_config_singleton()

    def to_dict(self):
        """Return a readable version of the pup"""
        # @TODO(mattjmcnaughton) Determine the best long term solution. Is it
        # defining `__repr__` or maybe `__eq__`?
        return {
            'name': self._name,
            'pup_type': self.__class__,
            'path': self._path
        }

    def install(self):
        """Install all aspects of the pup.
        """
        pup_in_kennel_path = self._install_pup()
        self._install_pup_dependencies(pup_in_kennel_path)

    def _install_pup(self):
        """Download the pup onto the local file system."""
        raise NotImplementedError

    def _install_pup_dependencies(self, pup_in_kennel_path):
        """Install the dependencies for the pup (i.e. other ansible roles or
        python packages.
        """
        python_dependency_file, ansible_dependency_file = self._get_dep_files(
            pup_in_kennel_path
        )

        for dep_file_path in {python_dependency_file, ansible_dependency_file}:
            if dep_file_path is not None:
                dependencies = PupDependencies.create_from_dep_file_path(dep_file_path)
                dependencies.install()

    @classmethod
    def _get_dep_files(cls, pup_in_kennel_path):
        python_dep_file = os.path.join(pup_in_kennel_path, cls.PYTHON_DEP_FILE)
        ansible_dep_file = os.path.join(pup_in_kennel_path, cls.ANSIBLE_DEP_FILE)

        if not os.path.isfile(python_dep_file):
            python_dep_file = None

        if not os.path.isfile(ansible_dep_file):
            ansible_dep_file = None

        return python_dep_file, ansible_dep_file

    @staticmethod
    @contextmanager
    def _with_tmp_dir():
        tmp_dir_path = tempfile.mkdtemp()

        yield tmp_dir_path

        shutil.rmtree(tmp_dir_path)


class FsPup(Pup):
    """A pup for which the source code is already on the local file system (we
    predominantly use this pup for testing).

    All fs pupfile locations should be specified relative to the location of the
    pupfile.
    """
    def _install_pup(self):
        fs_pup_location = os.path.join(self._config.get('abs_pupfile_dir'),
                                       self._path)

        pup_in_kennel_path = os.path.join(
            self._config.get('abs_kennel_roles_dir'), self._name)

        shutil.copytree(fs_pup_location, pup_in_kennel_path)

        return pup_in_kennel_path


class GitPup(Pup):
    """A pup for which the source lives in a remote git repo.
    """
    def _install_pup(self):
        with self._with_tmp_dir() as install_dir:
            install_path = os.path.join(install_dir, self._name)

            git_cmd = [
                'git',
                'clone',
                self._path,
                install_path
            ]

            ShellRunner(git_cmd).run()

            pup_in_kennel_path = os.path.join(
                self._config.get('abs_kennel_roles_dir'),
                self._name
            )

            shutil.copytree(install_path, pup_in_kennel_path)

            return pup_in_kennel_path


class GalaxyPup(Pup):
    """A pup for which the source lives on ansible-galaxy.
    """
    def _install_pup(self):
        with self._with_tmp_dir() as install_dir:
            ansible_galaxy_cmd = [
                'ansible-galaxy',
                'install',
                self._path,
                '-p',
                install_dir
            ]

            ShellRunner(ansible_galaxy_cmd).run()

            role_name = os.listdir(install_dir)[0]

            install_path = os.path.join(
                install_dir,
                role_name
            )

            pup_in_kennel_path = os.path.join(
                self._config.get('abs_kennel_roles_dir'),
                self._name
            )

            shutil.copytree(install_path, pup_in_kennel_path)

            return pup_in_kennel_path


class PupDependencies(object):
    """A base representation of a collection of pup dependencies. Either
    python packages or ansible roles.
    """
    @staticmethod
    def create_from_dep_file_path(dep_file_path):
        """Given the path to a pup's dependency file, instantiate an instance of
        the appropriate subclass based on the given `dep_file_path`.

        :param dep_file_path: The path to the dependency file.
        :type dep_file_path: str
        :return: Instance of subclass of `PupDependencies`.
        :rtype: PupDependencies
        """
        file_extension = dep_file_path.split('.')[-1]

        return _dependency_types_to_classes()[file_extension](dep_file_path)

    def __init__(self, dep_file_path, config=None):
        self._dep_file_path = dep_file_path

        self._config = config or Config.get_config_singleton()

    def install(self):
        """Install the pup dependency."""
        raise NotImplementedError


class PythonDependencies(PupDependencies):
    """Pip packages that must be installed on local machine for this kennel to
    run.
    """
    def install(self):
        pip_cmd = [
            'pip',
            'install',
            '-r',
            self._dep_file_path
        ]

        ShellRunner(pip_cmd).run()


class AnsibleDependencies(PupDependencies):
    """Ansible roles that must be installed on local machine for this kennel
    to run.
    """
    def install(self):
        ansible_galaxy_cmd = [
            'ansible-galaxy',
            'install',
            '-r',
            self._dep_file_path,
            '-p',
            self._config.get('abs_kennel_roles_dir')
        ]

        ShellRunner(ansible_galaxy_cmd).run()
