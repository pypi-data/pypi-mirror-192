# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ayaka_db']

package_data = \
{'': ['*']}

install_requires = \
['ayaka_utils>=0.0.3', 'inflection>=0.5.1', 'loguru>=0.6.0', 'sqlmodel>=0.0.8']

setup_kwargs = {
    'name': 'ayaka-db',
    'version': '0.0.3',
    'description': '',
    'long_description': '嗯嗯嗯嗯',
    'author': 'Su',
    'author_email': 'wxlxy316@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bridgeL/ayaka_db',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
