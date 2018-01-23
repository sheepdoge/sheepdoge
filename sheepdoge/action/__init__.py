"""Top-level module for sheepdoge actions"""

from sheepdoge.config import Config


class Action(object):
    """A base class for all actions.

    :param config: The configuration object for performing this action.
    """
    def __init__(self, config=None):
        # type: (Config) -> None
        self._config = config or Config.get_config_singleton()

    def run(self):
        # type: () -> None
        """Execute this action."""
        self._setup()
        self._execute()
        self._teardown()

    def _setup(self):
        # type: () -> None
        pass

    def _execute(self):
        # type: () -> None
        pass

    def _teardown(self):
        # type: () -> None
        pass
