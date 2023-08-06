# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jasmin_fuzzer']

package_data = \
{'': ['*']}

install_requires = \
['paramiko>=3.0.0,<4.0.0', 'rich>=13.3.1,<14.0.0']

entry_points = \
{'console_scripts': ['jasmin = jasmin_fuzzer.jasmin:main']}

setup_kwargs = {
    'name': 'jasmin-fuzzer',
    'version': '0.1.3',
    'description': 'Jasmin is a utility that displays a list of Linux commands available on a given machine.',
    'long_description': '![Logo](https://i.imgur.com/qXfSr0u.png)\n\nJasmin is a utility that displays a list of Linux commands available on a given machine. \n\nConnecting via SSH, Jasmin tests potentially useful commands to exit a restricted shell and perform actions that were normally restricted.\n\n## Demonstration\n\n[![asciicast](https://asciinema.org/a/0K7bmescf283rWU2pxr5KMWy4.svg)](https://asciinema.org/a/0K7bmescf283rWU2pxr5KMWy4)\n\n## Requirements\n\n```\npython -m pip install paramiko rich\n```\n\n## Installing\n\n```\npython -m pip install jasmin-fuzzer\n```\n\n## Help page\n\n```\n$ jasmin --help\nusage: jasmin [-h] --user username --host hostname [--privatekey] [-p PORT] [-v]\n\noptional arguments:\n  -h, --help            show this help message and exit\n\nrequired arguments:\n  --user username       username\n  --host hostname       ip address or domain name\n\noptional arguments:\n  --privatekey          connection established with your private key\n  -p PORT, --port PORT  ssh to use port (default=22)\n  -v, --verb            give each command tested (default=False)\n```',
    'author': 'Fayred',
    'author_email': 'fayred@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
