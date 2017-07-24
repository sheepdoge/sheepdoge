"""Module for code relating to installing pups for a kennel."""

from sheepdog.action import Action
from sheepdog.kennel import Kennel
from sheepdog.pup import Pup


class InstallAction(Action):
    def __init__(self, *args, **kwargs):
        super(InstallAction, self).__init__(*args, **kwargs)

        self._pups_to_install = []

    def _setup(self):
        Kennel.refresh_roles(self._config.get('abs_kennel_roles_dir'))
        self._pups_to_install = Pup.parse_pupfile_into_pups(
            self._config.get('pupfile_path'))

    def _execute(self):
        # @TODO(mattjmcnaughton) Add error handling.
        for pup in self._pups_to_install:
            pup.install()
