"""Module for code relating to installing pups for a kennel."""

from collections import namedtuple

from sheepdog.action import Action
from sheepdog.kennel import Kennel
from sheepdog.pup import Pup

InstallDirectories = namedtuple('InstallDirectories', 'pupfile_dir kennel_roles_dir')


class InstallAction(Action):
    """`sheepdog install`"""
    def __init__(self, *args, **kwargs):
        super(InstallAction, self).__init__(*args, **kwargs)

        self._install_dirs = InstallDirectories(
            pupfile_dir=self._config.get('abs_pupfile_dir'),
            kennel_roles_dir=self._config.get('abs_kennel_roles_dir')
        )

        self._pups_to_install = None

    def _setup(self):
        Kennel.refresh_roles(self._install_dirs.kennel_roles_dir)
        self._pups_to_install = Pup.parse_pupfile_into_pups(
            self._config.get('pupfile_path'))

    def _execute(self):
        for pup in self._pups_to_install:
            pup.install(self._install_dirs)
