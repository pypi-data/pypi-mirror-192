# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ayaka_utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ayaka-utils',
    'version': '0.0.3',
    'description': '',
    'long_description': '嗯嗯嗯嗯',
    'author': 'Su',
    'author_email': 'wxlxy316@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bridgeL/ayaka_utils',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
