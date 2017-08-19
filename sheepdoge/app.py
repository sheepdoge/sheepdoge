"""Orchestrates the different `sheepdoge` operations."""

from sheepdoge.config import Config


class Sheepdoge(object):
    """A class we instantiate with instances of the `Action`, which indicate
    which cli command we'll perform.

    :param action: The Sheepdoge action we're running.
    :type action: sheepdoge.action.Action
    """
    def __init__(self, action, config=None):
        self._action = action
        self._config = config or Config.get_config_singleton()

    def run(self):
        """Execute an command given to `sheepdoge`."""
        self._action.run()
