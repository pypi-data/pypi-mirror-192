# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gdatalog']

package_data = \
{'': ['*']}

install_requires = \
['distlib>=0.3.6,<0.4.0',
 'dumbo-asp>=0.0.21,<0.0.22',
 'pytest>=7.2.0,<8.0.0',
 'rich>=13.0.1,<14.0.0',
 'typeguard>=2.13.3,<3.0.0',
 'typer>=0.7.0,<0.8.0',
 'valid8>=5.1.2,<6.0.0']

setup_kwargs = {
    'name': 'gdatalog',
    'version': '0.0.2',
    'description': 'Genereative Datalog with stable negation',
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
