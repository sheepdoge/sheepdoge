"""Configuration for the `sheepdoge` pip package."""

from setuptools import setup, find_packages

GITHUB_URL = 'https://github.com/sheepdoge/sheepdoge'

# @TODO(mattjmcnaughton) determine this value dynamically.
VERSION = '0.1.5'

setup(
    name='sheepdoge',
    version=VERSION,
    description='Manage your personal Unix machine(s) with Ansible.',
    url=GITHUB_URL,
    author='Matt McNaughton',
    author_email='mattjmcnaughton@gmail.com',
    license='Apache',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    keywords=['provisioning', 'automation'],
    packages=find_packages(where='.', exclude=['tests*']),
    install_requires=[
        'ansible>=2.0,<3.0',
        'configparser>=3.0',
        'click>=6.0,<7.0',
        'PyYaml>=3.0,<4.0',
        'six>=1.0,<2.0',
        'futures>=3.0,<4.0; python_version == "2.7"'
    ],
    entry_points={
        'console_scripts': ['sheepdoge = sheepdoge.cli:main']
    }
)
