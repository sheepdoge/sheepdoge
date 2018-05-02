"""Configuration for the `sheepdoge` pip package."""

import ast
import re

from setuptools import setup, find_packages

GITHUB_URL = 'https://github.com/sheepdoge/sheepdoge'

with open('sheepdoge/__version__.py', 'rb') as version_file:
    file_contents = version_file.read().decode('utf-8')
    version_re = re.compile(r'__version__\s+=\s+(.*)')
    version = str(ast.literal_eval(version_re.search(file_contents).group(1)))

with open('requirements.in', 'r') as requirements_file:
    install_requires = [package.strip() for package in requirements_file.readlines()]

setup(
    name='sheepdoge',
    version=version,
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
    install_requires=install_requires,
    entry_points={
        'console_scripts': ['sheepdoge = sheepdoge.cli:main']
    }
)
