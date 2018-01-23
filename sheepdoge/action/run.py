"""Module for actions related to running a kennel."""

from typing import Any # pylint: disable=unused-import

from sheepdoge.action import Action
from sheepdoge.kennel import Kennel # pylint: disable=unused-import

class RunAction(Action):
    def __init__(self, kennel, *args, **kwargs):
        # type: (Kennel, *Any, **Any) -> None
        super(RunAction, self).__init__(*args, **kwargs)

        self._kennel = kennel

    def _execute(self):
        # type: () -> None
        self._kennel.run()
