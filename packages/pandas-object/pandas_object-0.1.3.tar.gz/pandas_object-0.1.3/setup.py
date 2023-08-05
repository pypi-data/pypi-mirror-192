# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pandas_object']

package_data = \
{'': ['*']}

install_requires = \
['pandas', 'rich']

setup_kwargs = {
    'name': 'pandas-object',
    'version': '0.1.3',
    'description': '',
    'long_description': '',
    'author': 'dwpeng',
    'author_email': '1732889554@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3,<4',
}


setup(**setup_kwargs)
