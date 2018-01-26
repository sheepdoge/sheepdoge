"""Orchestrates the different `sheepdoge` operations."""

from sheepdoge.config import Config
from sheepdoge.action import Action # pylint: disable=unused-import


class Sheepdoge(object):
    """A class we instantiate with instances of the `Action`, which indicate
    which cli command we'll perform.

    :param action: The Sheepdoge action we're running.
    """
    def __init__(self, action, config=None):
        # type: (Action, Config) -> None
        self._action = action
        self._config = config or Config.get_config_singleton()

    def run(self):
        # type: () -> None
        """Execute an command given to `sheepdoge`."""
        self._action.run()
