# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hidemysrc']

package_data = \
{'': ['*'], 'hidemysrc': ['compiled/*']}

install_requires = \
['pycryptodome>=3.17,<4.0']

setup_kwargs = {
    'name': 'hidemysrc',
    'version': '0.0.3',
    'description': 'Python-based package for encrypting your python source code!',
    'long_description': None,
    'author': 'Beliefs',
    'author_email': 'bio@fbi.ac',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10.0,<3.11',
}


setup(**setup_kwargs)
