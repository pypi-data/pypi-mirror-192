# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['statuspageio']

package_data = \
{'': ['*']}

install_requires = \
['munch>=2.5.0,<3.0.0', 'requests>=2.28.0,<3.0.0']

setup_kwargs = {
    'name': 'crunch-statuspageio',
    'version': '0.6',
    'description': 'Python client library for statuspage.io',
    'long_description': 'None',
    'author': 'Adrien Pensart',
    'author_email': 'adrien.pensart@corp.ovh.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
