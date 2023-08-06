# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_pytree']

package_data = \
{'': ['*']}

install_requires = \
['jax', 'jaxlib']

setup_kwargs = {
    'name': 'simple-pytree',
    'version': '0.1.1',
    'description': '',
    'long_description': '# simple-pytree',
    'author': 'Cristian Garcia',
    'author_email': 'cgarcia.e88@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
