"""Orchestrates the different `sheepdog` operations."""

from sheepdog.config import Config


class Sheepdog(object):
    """A class we instantiate with instances of the `Action`, which indicate
    which cli command we'll perform.

    :param action: The Sheepdog action we're running.
    :type action: sheepdog.action.Action
    """
    def __init__(self, action, config=None):
        self._action = action
        self._config = config or Config.get_config_singleton()

    def run(self):
        """Execute an command given to `sheepdog`."""
        self._action.run()
