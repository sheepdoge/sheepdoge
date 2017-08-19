"""Top-level module for sheepdoge actions"""

from sheepdoge.config import Config


class Action(object):
    """A base class for all actions.

    :param config: The configuration object for performing this action.
    :type config: sheepdoge.config.Config
    """
    def __init__(self, config=None):
        self._config = config or Config.get_config_singleton()

    def run(self):
        """Execute this action."""
        self._setup()
        self._execute()
        self._teardown()

    def _setup(self):
        pass

    def _execute(self):
        pass

    def _teardown(self):
        pass
