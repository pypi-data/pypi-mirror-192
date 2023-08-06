# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gitno']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'requests>=2.28.2,<3.0.0', 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'gitno',
    'version': '0.1.1',
    'description': '',
    'long_description': '# gitno\n\n[![PyPI version](https://img.shields.io/pypi/v/gitno.svg)](https://pypi.org/project/gitno/)\n[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/andwati>/gitno/blob/main/LICENSE)\n[![Python versions](https://img.shields.io/pypi/pyversions/gitno.svg)](https://pypi.org/project/gitno/)\n\nGitno is a command-line tool that generates `.gitignore` files based on the templates available in the [github/gitignore](https://github.com/github/gitignore) repository.\n\n## Installation\n\nYou can install `gitno` using pip:\n\n```sh\npip install gitno\n```\n## Usage\n\nCreate a `GITHUB_ACCESS_TOKEN` in your settings then add it to your environment variables\n\nInitialize a local copy of the .gitignore files by running:\n\n```sh\ngitno update\n```\n\nTo generate a .gitignore file on the current working directory, run the generate command followed by the template number or name:\n\n```sh\ngitno generate\n```\n\nTo see a list of available templates, run the list command:\n\n```sh\ngitno list\n```\n## Contributing\nContributions are welcome! Please see CONTRIBUTING.md for details.\n\n## License\nThis project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.',
    'author': 'Ian Andwati',
    'author_email': 'andwatiian@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
