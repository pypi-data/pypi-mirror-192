# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyassorted', 'pyassorted.asyncio']

package_data = \
{'': ['*']}

install_requires = \
['pytz', 'rich']

setup_kwargs = {
    'name': 'pyassorted',
    'version': '0.0.1',
    'description': 'A library has light-weight assorted utils in Prue-Python.',
    'long_description': '# pyassorted\nA library has assorted utils in Prue-Python.\n',
    'author': 'Allen Chou',
    'author_email': 'f1470891079@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
