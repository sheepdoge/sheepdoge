"""Configuration for the `sheepdog` pip package."""

from setuptools import setup

GITHUB_URL = 'https://github.com/mattjmcnaughton/sheepdog'

# @TODO(mattjmcnaughton) determine this value dynamically.
VERSION = '0.1.0'

setup(
    name='sheepdog',
    version=VERSION,
    description='Manage your personal Unix machine(s) with Ansible.',
    author='Matt McNaughton',
    license='Apache',
    author_email='mattjmcnaughton@gmail.com',
    url=GITHUB_URL,
    download_url='{}/tarball/{}'.format(GITHUB_URL, VERSION),
    keywords=['provisioning', 'automation'],
    install_requires=[],
    packages=['sheepdog'],
    entry_points={
        'console_scripts': ['sheepdog = sheepdog.cli:main']
    }
)
