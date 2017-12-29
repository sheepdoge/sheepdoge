"""Module for code relating to installing pups for a kennel."""

from concurrent.futures import ThreadPoolExecutor, wait
import multiprocessing

from sheepdoge.action import Action


class InstallAction(Action):
    def __init__(self, kennel_cls, pup_cls, *args, **kwargs):
        super(InstallAction, self).__init__(*args, **kwargs)

        self._pups_to_install = []

        self._kennel_cls = kennel_cls
        self._pup_cls = pup_cls

    def _setup(self):
        self._kennel_cls.refresh_roles(
            self._config.get('abs_kennel_roles_dir'))
        self._pups_to_install = self._pup_cls.parse_pupfile_into_pups(
            self._config.get('pupfile_path'))

    def _execute(self):
        for pup in self._pups_to_install:
            pup.install()


class ParallelInstallAction(InstallAction):
    """An InstallAction which downloads pups in parallel."""
    def __init__(self, kennel_cls, pup_cls, max_workers=None, **kwargs):
        super(ParallelInstallAction, self).__init__(
            kennel_cls, pup_cls, **kwargs)

        self._max_workers = (max_workers or
                             self._get_default_max_workers_from_cores())

    @staticmethod
    def _get_default_max_workers_from_cores():
        return multiprocessing.cpu_count()

    def _execute(self):
        with ThreadPoolExecutor(max_workers=self._max_workers) as executor:
            install_futures = {
                executor.submit(pup.install) for pup in self._pups_to_install
            }

            wait(install_futures)
