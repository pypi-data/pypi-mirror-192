# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cli', 'cli.res']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'click>=8.0.0,<9.0.0', 'pyroll-core>=2.0.0rc,<3.0.0']

entry_points = \
{'console_scripts': ['pyroll = pyroll.cli.program:run_cli']}

setup_kwargs = {
    'name': 'pyroll-cli',
    'version': '2.0.0rc0',
    'description': 'PyRoll rolling simulation framework - command line interface (CLI).',
    'long_description': '# PyRoll CLI\n\nThis is a command line interface (CLI) for the rollig simulation framework PyRolL.\nSee the [core repository](https://github.com/pyroll-project/pyroll-core) for further information.\n\n## Documentation\n\nSee the [documentation](https://pyroll.readthedocs.io/en/latest/basic/cli.html) to learn about basic concepts and\nusage.\n\n## License\n\nThe project is licensed under the [BSD 3-Clause license](LICENSE).\n',
    'author': 'Max Weiner',
    'author_email': 'max.weiner@imf.tu-freiberg.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pyroll-project.github.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
