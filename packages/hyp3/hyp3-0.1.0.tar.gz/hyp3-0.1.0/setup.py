# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hyperplane', 'hyperplane.cli', 'hyperplane.configuration', 'hyperplane.tests']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'numpy>=1.24.2,<2.0.0']

entry_points = \
{'console_scripts': ['hyp = cli.hyp:hyp']}

setup_kwargs = {
    'name': 'hyp3',
    'version': '0.1.0',
    'description': 'An intelligent metric plane for the modern data stack',
    'long_description': '<br/>\n<div align="center">\n    <img src="assets/logo.svg" height="150px" />\n</div>\n\n# Hyperplane\nAn intelligent metric plane for the modern data stack.\n\n# Documentation\nComing soon.\n\n# Installation\nThe package can be installed from PyPi with the following command:\n```\npip install hyp3\n```\n\n# Contributions\nWe always welcome contributions! Please read our [guide](https://github.com/hyperplane-data/hyperplane/CONTRIBUTING.md) to get started.\n\n# License\nHyperplane always will be open source. The project adheres to the Apache 2.0 license. ',
    'author': 'Hyperplane',
    'author_email': 'hyperplane.dev@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/hyperplane-data',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
