# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pokemon_showdown_replays']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pokemon-showdown-replays',
    'version': '0.1.0',
    'description': 'A package for generating pokemon showdown replays from pokemon showdown logs',
    'long_description': '',
    'author': 'eyalmen',
    'author_email': 'dave.eyal@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
