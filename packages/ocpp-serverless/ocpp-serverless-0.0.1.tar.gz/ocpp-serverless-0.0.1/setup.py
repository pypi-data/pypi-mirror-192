# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ocpp_serverless']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ocpp-serverless',
    'version': '0.0.1',
    'description': 'ocpp-serverless provides a framework for implementing highly scalable serverless event-driven server-side support for OCPP protocol with Python.',
    'long_description': None,
    'author': 'Ville Kärkkäin',
    'author_email': 'ville.karkkainen@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
