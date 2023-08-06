# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yudown']

package_data = \
{'': ['*']}

install_requires = \
['pytube>=12.1.2,<13.0.0', 'tinydb>=4.7.1,<5.0.0', 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['yudown = yudown.cli:app']}

setup_kwargs = {
    'name': 'yudown',
    'version': '0.6.0',
    'description': 'This is a python script to download Youtube Media file',
    'long_description': "# `YuDown`\n\nDownload Youtube Media from this script and have a wonderful output😋\n\n## Installation\n\nTo install and run the script:\n\n```console\n  python3 -m venv venv\n  pip install yudown\n\n  yudown --help\n```\n\n## Run Locally\n\nTo launch the project, you need [Poetry](https://python-poetry.org) to be installed\n\nClone the project\n\n```console\n  git clone https://github.com/TianaNanta/yudown.git\n```\n\nGo to the project directory\n\n```console\n  cd yudown\n```\n\nInstall dependencies\n\n```console\n  poetry install\n```\n\nLaunch the project\n\n```console\n  poetry run python -m yudown --help\n```\n\n## Usage\n\n**Usage**:\n\n```console\nyudown [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `-v, --version`: Show the application's version and exit.\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `download`: Download file from [red]Youtube[/red] 📥\n* `history`: Show the download [blue]history[/blue] ⌚️\n* `playlist`: Download Youtube [yellow]Playlist[/yellow]...\n* `search`: [blue]Search[/blue] for video on Youtube 🔍\n\n## `yudown download`\n\nDownload file from [red]Youtube[/red] 📥\n\n**Usage**:\n\n```console\nyudown download [OPTIONS] [LINKS]...\n```\n\n**Arguments**:\n\n* `[LINKS]...`\n\n**Options**:\n\n* `-t, --type TEXT`: The type of media to download  [default: video]\n* `-l, --location PATH`: Location of the downloaded file  [default: ~/YuDown/notSpecified]\n* `--help`: Show this message and exit.\n\n## `yudown history`\n\nShow the download [blue]history[/blue] ⌚️\n\n**Usage**:\n\n```console\nyudown history [OPTIONS]\n```\n\n**Options**:\n\n* `-D, --delete`\n* `--help`: Show this message and exit.\n\n## `yudown playlist`\n\nDownload Youtube [yellow]Playlist[/yellow] video 📼\n\n**Usage**:\n\n```console\nyudown playlist [OPTIONS] [LINK]\n```\n\n**Arguments**:\n\n* `[LINK]`\n\n**Options**:\n\n* `-l, --location PATH`: Location of the files to download  [default: /home/nanta/YuDown/Playlist]\n* `--help`: Show this message and exit.\n\n## `yudown search`\n\n[blue]Search[/blue] for video on Youtube 🔍\n\n**Usage**:\n\n```console\nyudown search [OPTIONS] [SEARCH_QUERY]\n```\n\n**Arguments**:\n\n* `[SEARCH_QUERY]`: The word you are searching for\n\n**Options**:\n\n* `-s, --suggestion`: Show search suggestion\n* `--help`: Show this message and exit.\n\n## Authors\n\n* [@TianaNanta](https://www.github.com/TianaNanta)\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n",
    'author': 'TianaNanta',
    'author_email': 'andrianjakananta@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
