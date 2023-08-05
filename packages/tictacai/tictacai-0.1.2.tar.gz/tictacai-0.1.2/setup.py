# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tictacai', 'tictacai.game', 'tictacai.logic']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tictacai',
    'version': '0.1.2',
    'description': 'Tic-Tac-Toe Game created using Minimax AI players',
    'long_description': '# TicTacToe Game Engine library\n\nA pure Python library for creating tic tac toe game frontends\n\n## Installation\n\nInstall the library into an active virtual environment:\n\n```sh\n(venv) python -m pip install .\n```\n\n## Packaging\n\nBuild and package a standalone tic tac toe library for distribution with:\n\n``` sh\npython -m pip wheel .\n```\n',
    'author': 'BrianLusina',
    'author_email': '12752833+BrianLusina@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
