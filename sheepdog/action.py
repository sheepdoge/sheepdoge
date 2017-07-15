"""Define sheepdog user actions (i.e. install, run...)"""

class Action(object):
    """A base class for all actions.

    :param config: The configuration object for performing this action.
    :type config: sheepdog.config.Config
    """
    def __init__(self, config):
        self._config = config

    def run(self):
        """Execute this action."""
        raise NotImplementedError

class InstallAction(Action):
    """`sheepdog install`"""
    def run(self):
        """Install this kennel's pups and their associated dependencies."""
        print 'install'

class RunAction(Action):
    """`sheepdog run`"""
    def run(self):
        """Bring the machine on which we are running this command into the state
        described in `kennel.yml`
        """
        print 'run'
