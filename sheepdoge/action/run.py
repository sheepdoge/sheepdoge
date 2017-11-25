"""Module for actions related to running a kennel."""

from sheepdoge.action import Action


class RunAction(Action):
    def __init__(self, kennel, *args, **kwargs):
        super(RunAction, self).__init__(*args, **kwargs)

        self._kennel = kennel

    def _execute(self):
        self._kennel.run()
