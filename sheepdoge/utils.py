import os
import subprocess

from sheepdoge.exception import SheepdogeShellRunnerException


class ShellRunner(object):
    """A wrapper around the `subprocess.check_call` command, to DRY the
    transformations necessary to run a shell command.

    :param cmd_as_list: The command for the `ShellRunner` to execute.
    :type cmd_as_list: list
    :raises: SheepdogeShellRunnerException
    """
    def __init__(self, cmd_as_list):
        self._cmd_as_str = ' '.join(cmd_as_list)

    def run(self, env_additions=None):
        """Execute the command wrapped by `ShellRunner`.

        :param env_additions: Optional method for specifying additional
        environment variables for the shell in the subprocess in which the
        command will execute.
        :type env_additions: dict
        """
        env_additions = env_additions or {}

        shell_env = os.environ.copy()
        shell_env.update(env_additions)

        try:
            subprocess.check_call(
                self._cmd_as_str,
                shell=True,
                env=shell_env
            )
        except subprocess.CalledProcessError as err:
            raise SheepdogeShellRunnerException(
                '{} failed: {}'.format(self._cmd_as_str, err.message)
            )
