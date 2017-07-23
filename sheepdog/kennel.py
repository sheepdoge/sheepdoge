from configparser import SafeConfigParser
import os
import shutil
import subprocess


class KennelRunException(Exception):
    pass


class Kennel(object):
    KENNEL_CFG_SECTION = 'kennel'

    @staticmethod
    def refresh_roles(kennel_roles_path):
        """Ensure a clean directory exists at `kennel_roles_path`."""
        if os.path.isdir(kennel_roles_path) and os.listdir(kennel_roles_path):
            shutil.rmtree(kennel_roles_path)
            os.mkdir(kennel_roles_path)

    @classmethod
    def parse_kennel_from_config_files(cls, kennel_playbook_path,
                                       kennel_roles_path,
                                       kennel_cfg_path):
        with open(kennel_cfg_path, 'r') as kennel_cfg:
            parsed_kennel_config = cls._parse_kennel_cfg_contents_into_config(
                kennel_cfg.read())

        return cls(kennel_playbook_path, kennel_roles_path,
                   parsed_kennel_config)

    @classmethod
    def _parse_kennel_cfg_contents_into_config(cls, config_file_contents):
        config_parser = SafeConfigParser()
        config_parser.read_string(config_file_contents.decode('utf-8'))

        return {
            'vault_password_file': config_parser.get(cls.KENNEL_CFG_SECTION,
                                                     'vault_password_file')
        }

    def __init__(self, kennel_playbook_path, kennel_roles_path, kennel_config):
        self._kennel_playbook_path = kennel_playbook_path
        self._kennel_roles_path = kennel_roles_path
        self._kennel_config = kennel_config

    def run(self):
        ansible_playbook_cmd = ' '.join([
            'ansible-playbook',
            self._kennel_playbook_path,
            '--vault-password-file={}'.format(
                self._kennel_config['vault_password_file'])
        ])

        env_vars = os.environ.copy()
        env_vars['ANSIBLE_ROLES_PATH'] = self._kennel_roles_path

        try:
            subprocess.check_call(ansible_playbook_cmd, env=env_vars,
                                  shell=True)
        except subprocess.CalledProcessError as err:
            raise KennelRunException('{} failed: {}'.format(
                ansible_playbook_cmd, err.message))
