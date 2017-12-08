"""Module for code relating to installing pups for a kennel."""

from sheepdoge.action import Action


class InstallAction(Action):
    def __init__(self, kennel_cls, pup_cls, *args, **kwargs):
        super(InstallAction, self).__init__(*args, **kwargs)

        self._pups_to_install = []

        self._kennel_cls = kennel_cls
        self._pup_cls = pup_cls

    def _setup(self):
        self._kennel_cls.refresh_roles(self._config.get('abs_kennel_roles_dir'))
        self._pups_to_install = self._pup_cls.parse_pupfile_into_pups(
            self._config.get('pupfile_path'))

    def _execute(self):
        for pup in self._pups_to_install:
            pup.install()
