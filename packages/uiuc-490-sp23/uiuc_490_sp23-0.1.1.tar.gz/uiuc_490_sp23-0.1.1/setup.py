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
{'console_scripts': ['assignment1 = assignment1:__main__']}

setup_kwargs = {
    'name': 'uiuc-490-sp23',
    'version': '0.1.1',
    'description': "Programming assignments for UIUC's ECE490: Introduction to Optimization course during Spring 2023",
    'long_description': "# ECE490\nRepo to collaborate within for UIUC's ECE490, Spring 2023\n\n## Installation\n### Installation from PyPI\nThis should be as simple as:\n```bash\npython -m pip install uiuc-490-sp23\n```\n### Installation from Source\nThis project uses [Poetry](https://python-poetry.org/) Install it via\n[their instructions](https://python-poetry.org/docs/#installing-with-the-official-installer)\nand run:\n```bash\npoetry install\n```\nfrom this directory (preferably from within a `venv`).\n\n## Executing\nOnce installed, individual assignments can be ran by:\n```bash\npython -m uiuc-490-sp23.assignment<n>\n```\nwhere `<n>` is the assignment number. These will have a CLI implemented using argparse; if you're not sure,\njust run the above with `--help` to get a full list of commands.",
    'author': 'Eric Silk',
    'author_email': 'eric.silk@ericsilk.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/eric-silk/ECE490',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
