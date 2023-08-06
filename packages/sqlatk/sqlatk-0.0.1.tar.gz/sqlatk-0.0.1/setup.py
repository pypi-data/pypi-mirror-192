# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlatk']

package_data = \
{'': ['*']}

install_requires = \
['asyncpg==0.27.0',
 'databases==0.7.0',
 'fastapi==0.92.0',
 'loguru==0.6.0',
 'pydantic==1.10.5',
 'sqlalchemy>=1.4.42,<2.0.0']

setup_kwargs = {
    'name': 'sqlatk',
    'version': '0.0.1',
    'description': 'async database toolkit for fastapi',
    'long_description': '',
    'author': 'wayfaring-stranger',
    'author_email': 'zw6p226m@duck.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
