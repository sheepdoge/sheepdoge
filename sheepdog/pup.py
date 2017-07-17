import yaml

class Pup(object):
    """Container of all pup related logic. Contains both static methods as well
    as base methods inherited by the different types of pups.
    """
    @classmethod
    def parse_pupfile_into_pups(cls, pupfile_path):
        """Return a list of `Pup` objects for each pup we wish to install."""
        # Read in file and parse with yml
        with open(pupfile_path, 'r') as pupfile:
            pupfile_yaml = yaml.load(pupfile.read())

        return cls.create_from_parameters(pupfile_yaml)

    @staticmethod
    def create_from_parameters(parameters):
        """Create a pup based on a line in a `pupfile.yml`.

        Instantiates and returns a subclass of `Pup` for the specific type of
        pup we are installing (i.e. from local filesystem, git, ansible-galaxy)."""
        # Instantiate instance of subclass based on the parameters
        return [parameters]

    def __init__(self):
        self._pup_dependencies = []

    def install(self):
        """Install all aspects of the pup."""
        self._install_pup()
        self._install_pup_dependencies()

    def _install_pup(self):
        """Download the pup onto the local file system."""
        pass

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
    """
    pass

class GitPup(Pup):
    """A pup for which the source lives in a remote git repo.
    """
    pass

class GalaxyPup(Pup):
    """A pup for which the source lives on ansible-galaxy.
    """
    pass

class PupDependency(object):
    """A base representation of a pup dependency - either a role or a pip
    package.
    """
    @staticmethod
    def parse_dependencies_from_file(dep_file):
        """Parse dependencies from a `requirements.{yml,txt} file."""
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
