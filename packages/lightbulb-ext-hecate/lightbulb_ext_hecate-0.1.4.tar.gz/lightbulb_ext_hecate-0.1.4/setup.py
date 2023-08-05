# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hecate']

package_data = \
{'': ['*']}

install_requires = \
['hikari-lightbulb>=2.3.1,<3.0.0']

setup_kwargs = {
    'name': 'lightbulb-ext-hecate',
    'version': '0.1.4',
    'description': 'File driven wrappers around lightbulb extensions and plugins.',
    'long_description': '# lightbulb-ext-hecate\nFile driven wrappers around lightbulb extensions and plugins.\n',
    'author': 'Radkii',
    'author_email': 'real.radkii@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/radkii/lightbulb-ext-hecate',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
