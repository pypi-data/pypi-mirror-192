# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['keyspwgenerator']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0']

entry_points = \
{'console_scripts': ['keys = keyspwgenerator.cli:main']}

setup_kwargs = {
    'name': 'keyspwgenerator',
    'version': '0.1.0',
    'description': 'CLI tool that creates passwords',
    'long_description': "# Keys (Password Generator)\n\n![python](https://img.shields.io/badge/Python-3.8%2C%203.9%2C%203.10%2C%203.11-blue)\n[![pip install](https://img.shields.io/badge/pip%20install-click-blue)](https://palletsprojects.com/p/click/)\n[![license](https://img.shields.io/badge/License-MIT-blue)](https://opensource.org/license/mit/)\n[![Testing](https://github.com/jsattari/keys/actions/workflows/tests.yaml/badge.svg)](https://github.com/jsattari/keys/actions/workflows/tests.yaml)\n[![codecov](https://codecov.io/gh/jsattari/keys/branch/master/graph/badge.svg?token=8XQ4MXVR3M)](https://codecov.io/gh/jsattari/keys)\n\n---\n\n## Introduction to Keys\n\nKeys is a password generator that creates new passwords from uppercase letters, lowercase letters, digits, and special characters all within the Terminal.\n\n## Installation\n\n    pip3 install keys\n\n## Usage\n\n    Usage: keys [OPTIONS]\n\n        CLI app that creates a password for you!\n\n    Options:\n        -l, --length INTEGER  Length of desired password. Will default to 8\n                                if flag is not used\n        -r, --remove TEXT     Values or characters to be excluded from the created\n                                password (Enter values as a string... ex: 'j9_@Dy]'\n        -n, --no_repeats      Ensures there are no duplicate characters\n        -c, --check TEXT      Checks string and returns password strength rating\n        -s, --strong          Ignores length input and instead returns a strong\n                                password\n        --help                Show this message and exit.\n\n## Notes\n\n- Works with Python 3.8^\n",
    'author': 'John Sattari',
    'author_email': 'jsattari3@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jsattari/keys-pw-generator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
