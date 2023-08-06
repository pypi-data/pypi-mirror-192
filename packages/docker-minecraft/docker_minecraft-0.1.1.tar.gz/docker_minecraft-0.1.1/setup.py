# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['docker_minecraft']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'docker>=6.0.1,<7.0.0']

entry_points = \
{'console_scripts': ['docker-minecraft = docker_minecraft:docker_minecraft']}

setup_kwargs = {
    'name': 'docker-minecraft',
    'version': '0.1.1',
    'description': 'Make a Minecraft server in Docker, with one command.',
    'long_description': '# docker-minecraft-cli\n\n## About\n\nThis is a CLI application aiming to allow you to set up and run a Minecraft server in Docker with just one command.\n\n**WARNING**: This application is currently in **beta**, not all features will work or are implemented yet.\n\n## Installation\n\nThe recommended way to install is using [`pipx`](https://pypa.github.io/pipx/):\n\n```bash\npipx install docker-minecraft\n```\n\nAlternatively, you can use `pip`:\n\n```bash\npip install docker-minecraft\n```\n\n## License\n\nThis project is licensed under the [GNU GPL v3](LICENSE.md). See [the license](LICENSE.md) for more information.\n',
    'author': 'osfanbuff63',
    'author_email': 'osfanbuff63@osfanbuff63.tech',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://codeberg.org/osfanbuff63/docker-minecraft-cli',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10',
}


setup(**setup_kwargs)
