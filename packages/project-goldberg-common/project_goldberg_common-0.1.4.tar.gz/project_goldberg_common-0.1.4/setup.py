# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['project_goldberg_common', 'project_goldberg_common.math_module']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.2.1,<8.0.0']

setup_kwargs = {
    'name': 'project-goldberg-common',
    'version': '0.1.4',
    'description': '',
    'long_description': '# project-goldberg-common\n\nThis is the develop branch of the project-goldberg-common repository. This branch is used for development and testing of the project-goldberg-common library. The master branch is used for releases.\n\n## How to use this package inside other projects in development environment\n\nFirst you need to clone the project-goldberg-common repository:\n\nThen you need to install the project-goldberg-common package in editable mode:\n\n```bash\npoetry add --editable <path-to-project-goldberg-common-repository>\n```\n',
    'author': 'Simone Sangeniti',
    'author_email': 'snakenextgen@gmai.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': '',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
