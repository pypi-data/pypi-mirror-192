# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kvd']

package_data = \
{'': ['*']}

install_requires = \
['modelos==0.1.3']

setup_kwargs = {
    'name': 'kvd',
    'version': '0.1.0',
    'description': 'A KV store built on ModelOS',
    'long_description': None,
    'author': 'Patrick Barker',
    'author_email': 'patrickbarkerco@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
