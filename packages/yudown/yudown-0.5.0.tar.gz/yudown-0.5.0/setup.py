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
    'version': '0.5.0',
    'description': 'This is a python script to download Youtube Media file',
    'long_description': '# YuDown (project under improvement)\n\nYuDown is a python script to download YouTube video developped using [Typer](https://typer.tiangolo.com) and [Pytube](https://github.com/pytube/pytube)\n\n## Installation\n\nTo install and run the script:\n\n```bash\n  python3 -m venv venv\n  pip install yudown\n\n  yudown --help\n```\n\n## Run Locally\n\nTo launch the project, you need [Poetry](https://python-poetry.org) to be installed\n\nClone the project\n\n```bash\n  git clone https://github.com/TianaNanta/yudown.git\n```\n\nGo to the project directory\n\n```bash\n  cd yudown\n```\n\nInstall dependencies\n\n```bash\n  poetry install\n```\n\nLaunch the project\n\n```bash\n  poetry run python -m yudown --help\n```\n\n## Usage/Examples\n\nTo download audio file from the given Youtube link\n\n```bash\n  yudown -A https://youtube.com/.....\n```\n\n## Authors\n\n- [@TianaNanta](https://www.github.com/TianaNanta)\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n',
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
