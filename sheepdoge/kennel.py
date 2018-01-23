import os
import shutil
from typing import List # pylint: disable=unused-import

from sheepdoge.config import Config
from sheepdoge.utils import ShellRunner


class Kennel(object):
    def __init__(self, additional_ansible_args='', config=None):
        # type: (str, Config) -> None
        self._additional_ansible_args = additional_ansible_args
        self._config = config or Config.get_config_singleton()

    @staticmethod
    def refresh_roles(kennel_roles_path):
        # type: (str) -> None
        """Ensure a clean directory exists at `kennel_roles_path`."""
        if os.path.isdir(kennel_roles_path) and os.listdir(kennel_roles_path):
            shutil.rmtree(kennel_roles_path)
            os.mkdir(kennel_roles_path)

    def run(self):
        # type: () -> None
        ansible_playbook_cmd = [
            'ansible-playbook',
            self._config.get('kennel_playbook_path')
        ]

        self._append_vault_password_file_flag_if_file_exists(
            ansible_playbook_cmd)

        if self._additional_ansible_args:
            ansible_playbook_cmd += self._additional_ansible_args.split(' ')

        ShellRunner(ansible_playbook_cmd).run(env_additions={
            'ANSIBLE_ROLES_PATH': self._config.get('kennel_roles_path')
        })

    def _append_vault_password_file_flag_if_file_exists(self,
                                                        ansible_playbook_cmd):
        # type: (List[str]) -> None
        password_file = self._config.get('vault_password_file')

        if password_file:
            ansible_playbook_cmd.append(
                '--vault-password-file={}'.format(password_file)
            )
