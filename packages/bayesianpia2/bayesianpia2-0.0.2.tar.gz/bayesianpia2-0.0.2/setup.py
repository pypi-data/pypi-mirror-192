# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bayesianpia2']

package_data = \
{'': ['*']}

install_requires = \
['python-semantic-release>=7.33.1,<8.0.0', 'semver>=2.13.0,<3.0.0']

setup_kwargs = {
    'name': 'bayesianpia2',
    'version': '0.0.2',
    'description': '',
    'long_description': '# Lab 2 IA',
    'author': 'IPablo271',
    'author_email': '69815580+IPablo271@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
