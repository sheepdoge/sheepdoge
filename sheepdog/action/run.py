"""Module for actions related to running a kennel."""

from sheepdog.action import Action
from sheepdog.kennel import Kennel, KennelRunException

# @TODO(mattjmcnaughton) Add `*ActionException` exceptions for each class.
# Catch them in `app.py` and exit with the appropriate status code.
class RunActionException(Exception):
    pass


class RunAction(Action):
    def __init__(self, *args, **kwargs):
        super(RunAction, self).__init__(*args, **kwargs)

        self._kennel = None

    def _setup(self):
        self._kennel = Kennel.parse_kennel_from_config_files(
            self._config.get('kennel_playbook_path'),
            self._config.get('kennel_roles_path'),
            self._config.get('kennel_cfg_path'),
        )

    def _execute(self):
        try:
            self._kennel.run()
        except KennelRunException as err:
            raise RunActionException(err.message)
