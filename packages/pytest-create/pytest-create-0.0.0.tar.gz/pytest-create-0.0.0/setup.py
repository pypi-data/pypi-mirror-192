# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytest_create']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1']

entry_points = \
{'console_scripts': ['pytest-create = pytest_create.__main__:main']}

setup_kwargs = {
    'name': 'pytest-create',
    'version': '0.0.0',
    'description': 'pytest-create',
    'long_description': "# pytest-create\n\n[![PyPI](https://img.shields.io/pypi/v/pytest-create.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/pytest-create.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/pytest-create)][python version]\n[![License](https://img.shields.io/pypi/l/pytest-create)][license]\n\n[![Read the documentation at https://pytest-create.readthedocs.io/](https://img.shields.io/readthedocs/pytest-create/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/56kyle/pytest-create/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/56kyle/pytest-create/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/pytest-create/\n[status]: https://pypi.org/project/pytest-create/\n[python version]: https://pypi.org/project/pytest-create\n[read the docs]: https://pytest-create.readthedocs.io/\n[tests]: https://github.com/56kyle/pytest-create/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/56kyle/pytest-create\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\n- TODO\n\n## Requirements\n\n- TODO\n\n## Installation\n\nYou can install _pytest-create_ via [pip] from [PyPI]:\n\n```console\n$ pip install pytest-create\n```\n\n## Usage\n\nPlease see the [Command-line Reference] for details.\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_pytest-create_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/56kyle/pytest-create/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/56kyle/pytest-create/blob/main/LICENSE\n[contributor guide]: https://github.com/56kyle/pytest-create/blob/main/CONTRIBUTING.md\n[command-line reference]: https://pytest-create.readthedocs.io/en/latest/usage.html\n",
    'author': 'Kyle Oliver',
    'author_email': '56kyleoliver@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/56kyle/pytest-create',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
