# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['morty_portal_gun']

package_data = \
{'': ['*']}

install_requires = \
['tinydb>=4.7.1,<5.0.0', 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['morty-portal-gun = morty_portal_gun.main:app']}

setup_kwargs = {
    'name': 'morty-portal-gun',
    'version': '1.0.1',
    'description': '',
    'long_description': '# Morty Portal Gun\n\n[![Python Test](https://github.com/test-python-wheel/morty-portal-gun/actions/workflows/tests.yml/badge.svg)](https://github.com/test-python-wheel/morty-portal-gun/actions/workflows/tests.yml)\n\na test project\n',
    'author': 'test-python-wheel',
    'author_email': 'test-python-wheel-project@outlook.com',
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
