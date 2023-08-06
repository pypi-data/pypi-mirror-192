# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dumbo_asp']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.3.0,<10.0.0',
 'cairocffi>=1.4.0,<2.0.0',
 'clingo>=5.6.2,<6.0.0',
 'dateutils>=0.6.12,<0.7.0',
 'dumbo-utils>=0.1.8,<0.2.0',
 'igraph>=0.10.2,<0.11.0',
 'rich>=13.3.1,<14.0.0',
 'typeguard>=2.13.3,<3.0.0',
 'update>=0.0.1,<0.0.2',
 'valid8>=5.1.2,<6.0.0']

setup_kwargs = {
    'name': 'dumbo-asp',
    'version': '0.0.20',
    'description': 'Utilities for Answer Set Programming',
    'long_description': 'None',
    'author': 'Mario Alviano',
    'author_email': 'mario.alviano@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
