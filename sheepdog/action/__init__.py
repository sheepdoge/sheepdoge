"""Top-level module for sheepdog actions"""

class Action(object):
    """A base class for all actions.

    :param config: The configuration object for performing this action.
    :type config: sheepdog.config.Config
    """
    def __init__(self, config):
        self._config = config

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
