# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gitflux', 'gitflux.commands']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'pygithub>=1.57,<2.0']

entry_points = \
{'console_scripts': ['gitflux = gitflux.__main__:cli']}

setup_kwargs = {
    'name': 'gitflux',
    'version': '0.3.0',
    'description': 'A command-line utility to help you manage repositories hosted on GitHub.',
    'long_description': '# gitflux\n\nA command-line utility to help you manage repositories hosted on [GitHub][1].\n\n## Installation\n\nThere are two options to install `gitflux` command.\n\n1. Download compiled executable binary file from [Releases][2].\n\n2. Install package `gitflux` via `pip` command:\n\n    ```shell\n    pip install gitflux\n    ```\n\n## Usage\n\n```\nUsage: gitflux [OPTIONS] COMMAND [ARGS]...\n\n  A command-line utility to help you manage repositories hosted on GitHub.\n\nOptions:\n  --version  Show version information.\n  --init     Initialize configurations.\n  --help     Show this message and exit.\n\nCommands:\n  create-repos  Create remote repositories.\n  delete-repos  Delete an existing repository.\n  list-repos    List all remote repositories.\n  sync-repos    Synchronize repositories with remote.\n```\n\n## License\n\nCopyright (C) 2022 HE Yaowen <he.yaowen@hotmail.com>\n\nThe GNU General Public License (GPL) version 3, see [LICENSE](./LICENSE).\n\n[1]: https://github.com\n\n[2]: https://github.com/he-yaowen/gitflux/releases\n',
    'author': 'HE Yaowen',
    'author_email': 'he.yaowen@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
