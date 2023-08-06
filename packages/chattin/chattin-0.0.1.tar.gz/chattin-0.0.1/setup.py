# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chattin']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.2.0,<3.0.0',
 'numpy>=1.22.2,<2.0.0',
 'openai>=0.26.5,<0.27.0',
 'replit>=3.2.4,<4.0.0',
 'urllib3>=1.26.12,<2.0.0']

setup_kwargs = {
    'name': 'chattin',
    'version': '0.0.1',
    'description': 'Python-based package that answers simplistic questions and can be taught by Human input & AI input.',
    'long_description': None,
    'author': 'ledges',
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
