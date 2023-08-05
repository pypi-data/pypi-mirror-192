# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_plugin_bump']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.2.0,<2.0.0', 'semver>=2.13.0,<3.0.0']

entry_points = \
{'poetry.application.plugin': ['bump = poetry_plugin_bump.plugin:ExecPlugin']}

setup_kwargs = {
    'name': 'poetry-plugin-bump',
    'version': '0.0.2',
    'description': 'poetry plugin to bump version',
    'long_description': "# poetry-plugin-bump\n\nA plugin for poetry to bump version, just like you can in npm.\n\n## Installation\n\nInstallation requires poetry 1.2.0+. To install this plugin run:\n\n`poetry self add poetry-plugin-bump`\n\nIf your poetry is installed with `pipx`:\n\n```\npipx inject poetry poetry-plugin-bump\n```\n\nFor other methods of installing plugins see\nthe [poetry documentation](https://python-poetry.org/docs/master/plugins/#the-plugin-add-command).\n\n## Usage\n\nConfiguration is optional, but you can define config in `pyproject.toml`\n\ndefault config:\n\n```toml\n[tool.poetry-plugin-bump]\nmsg = 'bump: v{version}'\ntag_name = 'v{version}'\n```\n\nthis will define bump commit message and tag name.\n\n## License\n\nMIT licensed, inspired by https://github.com/keattang/poetry-exec-plugin\n",
    'author': 'trim21',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/keattang/poetry-exec-plugin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
