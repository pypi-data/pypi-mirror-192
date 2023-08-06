# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['backup_github']

package_data = \
{'': ['*']}

install_requires = \
['prometheus_client>=0.16.0,<0.17.0', 'requests>=2.28.2,<3.0.0']

entry_points = \
{'console_scripts': ['backup-github = backup_github.main:main']}

setup_kwargs = {
    'name': 'backup-github',
    'version': '0.1.0',
    'description': '',
    'long_description': '# GitHub-Backup\n\n## Project description\n\nApplication for backing up information about a GitHub organization\n\n## Installation\n\nYou can clone this repository and set up the environment directly from the command line using the following command:\n\n```bash\ngit clone git@github.com:cloud-labs-infra/github-backup.git\ncd github-backup\nmake env\nexport PYTHONPATH=$PYTHONPATH:$PWD/github_backup\n```\n\n## Testing\n\nYou can run the tests using the following command:\n\n```bash\nmake test\n```\n\nThis command runs all unit tests and calculates coverage\n\n## Usage\n\nCLI Usage is as follows:\n\n    ./venv/bin/python github_backup/main.py [-h] [-t TOKEN] [-o OUTPUT_DIR]\n               [-r REPOSITORY [REPOSITORY ...]]\n               ORGANIZATION_NAME\n\n    Backup a GitHub organization\n    \n    positional arguments:\n      ORGANIZATION_NAME                     github organization name\n    \n    options:\n      -h, --help                            show this help message and exit\n      -t TOKEN, --token TOKEN\n                                            personal token\n      -o OUTPUT_DIR, --output-directory OUTPUT_DIR\n                                            directory for backup\n      -r REPOSITORY [REPOSITORY ...], --repository REPOSITORY [REPOSITORY ...]\n                                            name of repositories to limit backup\n\n\n## Backup structure\n\n    .\n    └── organization\n        ├── members\n        │ └── login1\n        │     ├── member.json\n        │     └── membership.json\n        └── repos\n            └── repo1\n                ├── content\n                │ └── repo1.git\n                ├── issues\n                │ └── 1\n                │     ├── assignee.json\n                │     ├── comments\n                │     ├── issue.json\n                │     └── user.json\n                ├── pulls\n                │ └── 2\n                │     ├── assignee.json\n                │     ├── base.json\n                │     ├── comments\n                │     │ └── 1\n                │     │     ├── comment.json\n                │     │     └── user.json\n                │     ├── head.json\n                │     ├── pull.json\n                │     ├── reviews\n                │     │ ├── 1\n                │     │ │   ├── review.json\n                │     │ │   └── user.json\n                │     │ └── 2\n                │     │     ├── comments\n                │     │     │ └── 1\n                │     │     │     ├── comment.json\n                │     │     │     └── user.json\n                │     │     ├── review.json\n                │     │     └── user.json\n                │     └── user.json\n                └── repo.json\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n\n## Project status\n\nThe project is currently in a development state',
    'author': 'Karina5005',
    'author_email': 'karinaanisimova23062001@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
