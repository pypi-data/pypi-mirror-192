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
    'version': '0.1.0',
    'description': 'Jasmin is a utility that displays a list of Linux commands available on a given machine.',
    'long_description': '',
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
