# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drf_microservice_auth', 'drf_microservice_auth.migrations']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=39.0.1,<40.0.0',
 'django>=4.1.6,<5.0.0',
 'djangorestframework>=3.14.0,<4.0.0',
 'pyjwt>=2.6.0,<3.0.0']

setup_kwargs = {
    'name': 'drf-microservice-auth',
    'version': '0.1.1a0',
    'description': 'Unstable as this is in heavy development.',
    'long_description': 'None',
    'author': 'christian',
    'author_email': 'imchristianlowe@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
