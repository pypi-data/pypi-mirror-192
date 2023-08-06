# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tapioca_arbache']

package_data = \
{'': ['*']}

install_requires = \
['pre-commit>=2.15.0,<3.0.0',
 'python-status>=1.0.1,<2.0.0',
 'requests-oauthlib>=1.3.0,<2.0.0',
 'responses>=0.13.3,<0.14.0',
 'tapioca-wrapper>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'tapioca-arbache',
    'version': '2.2.2',
    'description': "Clients for Arbache's APIs",
    'long_description': 'None',
    'author': 'Leonardo Jose N Silva',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10.4,<4.0.0',
}


setup(**setup_kwargs)
