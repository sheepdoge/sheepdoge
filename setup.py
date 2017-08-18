"""Configuration for the `sheepdog` pip package."""

from setuptools import setup

GITHUB_URL = 'https://github.com/mattjmcnaughton/sheepdog'

# @TODO(mattjmcnaughton) determine this value dynamically.
VERSION = '0.1.0'

setup(
    name='sheepdog',
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
        'License :: OSI Approved :: Apache License',
        'Programming Language :: Python :: 2.7'
    ],
    keywords=['provisioning', 'automation'],
    packages=['sheepdog'],
    install_requires=[
        'ansible>=2.0,<3.0',
        'click>=6.0,<7.0',
        'PyYaml>=3.0,<4.0'
    ],
    python_requires='>=2.7, <3',
    entry_points={
        'console_scripts': ['sheepdog = sheepdog.cli:main']
    }
)
