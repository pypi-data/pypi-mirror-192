# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uiuc_490_sp23',
 'uiuc_490_sp23.Exceptions',
 'uiuc_490_sp23.LineSearch',
 'uiuc_490_sp23.Optimizers',
 'uiuc_490_sp23.Problem',
 'uiuc_490_sp23.assignment1']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.2,<2.0.0']

entry_points = \
{'console_scripts': ['assignment1 = assignment1']}

setup_kwargs = {
    'name': 'uiuc-490-sp23',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Eric Silk',
    'author_email': 'eric.silk@ericsilk.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
