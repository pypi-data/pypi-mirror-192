# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xe_temp']

package_data = \
{'': ['*']}

install_requires = \
['currencyconverter>=0.17.5,<0.18.0']

setup_kwargs = {
    'name': 'xe-temp',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Alexander Molero',
    'author_email': 'alemoler@ucm.es',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
