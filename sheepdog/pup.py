from collections import namedtuple
import os
import shutil

import yaml

from sheepdog.config import Config
from sheepdog.exception import SheepdogInvalidPupTypeException

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


class Pup(object):
    """Container of all pup related logic. Contains both static methods as well
    as base methods inherited by the different types of pups.
    """
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
                raise SheepdogInvalidPupTypeException(err_msg)
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
        self._install_pup()
        self._install_pup_dependencies()

    def _install_pup(self):
        """Download the pup onto the local file system."""
        raise NotImplementedError

    def _install_pup_dependencies(self):
        """Install the dependencies for the pup (i.e. other ansible roles or
        python packages.
        """
        python_dependency_file = self._get_python_dependency_file()
        role_dependency_file = self._get_role_dependency_file()

        for dep_file in {python_dependency_file, role_dependency_file}:
            dependencies = PupDependency.parse_dependencies_from_file(dep_file)
            self._pup_dependencies.extend(dependencies)

        for dependency in self._pup_dependencies:
            dependency.install()

    @staticmethod
    def _get_python_dependency_file():
        return 'requirements.txt'

    @staticmethod
    def _get_role_dependency_file():
        return 'requirements.yaml'


class FsPup(Pup):
    """A pup for which the source code is already on the local file system (we
    predominantly use this pup for testing).

    All fs pupfile locations should be specified relative to the location of the
    pupfile.
    """
    def _install_pup(self):
        fs_pup_location = os.path.join(self._config.get('abs_pupfile_dir'),
                                       self._path)

        pup_in_kennel_location = os.path.join(
            self._config.get('abs_kennel_roles_dir'), self._name)

        shutil.copytree(fs_pup_location, pup_in_kennel_location)


class GitPup(Pup):
    """A pup for which the source lives in a remote git repo.
    """
    def _install_pup(self):
        pass


class GalaxyPup(Pup):
    """A pup for which the source lives on ansible-galaxy.
    """
    def _install_pup(self):
        pass


class PupDependency(object):
    """A base representation of a pup dependency - either a role or a pip
    package.
    """
    @staticmethod
    def parse_dependencies_from_file(dep_file):
        """Parse dependencies from a `requirements.{yml,txt} file."""
        # pylint: disable=unused-argument
        return []

    def install(self):
        """Install the pup dependency."""
        pass


class PythonDependency(PupDependency):
    """A pip package that must be installed on local machine for this kennel to
    run.
    """
    pass


class RoleDependency(PupDependency):
    """An ansible role that must be installed on local machine for this kennel
    to run.
    """
    pass
