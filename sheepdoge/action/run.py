"""Module for actions related to running a kennel."""

from sheepdoge.action import Action
from sheepdoge.kennel import Kennel


class RunAction(Action):
    def __init__(self, *args, **kwargs):
        super(RunAction, self).__init__(*args, **kwargs)

        self._kennel = None

    def _setup(self):
        self._kennel = Kennel()

    def _execute(self):
        self._kennel.run()
