"""Orchestrates the different `sheepdog` operations."""

class Sheepdog(object):
    """A class we instantiate with instances of the `Action`, which indicate
    which cli command we'll perform.

    :param action: The Sheepdog action we're running.
    :type action: sheepdog.action.Action
    """
    def __init__(self, action):
        self._action = action

    def run(self):
        """Execute an command given to `sheepdog`."""
        print "running sheepdog"
        self._action.run()
