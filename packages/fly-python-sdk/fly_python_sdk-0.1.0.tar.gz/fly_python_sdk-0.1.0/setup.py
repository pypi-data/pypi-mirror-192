# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fly_python_sdk',
 'fly_python_sdk.models',
 'fly_python_sdk.models.apps',
 'fly_python_sdk.models.machines']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.3,<0.24.0', 'pydantic>=1.10.4,<2.0.0', 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'fly-python-sdk',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Python SDK for Fly.io\n\nFlyPy is active development. Please come back later for more documentation.\n',
    'author': 'Brian Li',
    'author_email': 'brian@brianli.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
