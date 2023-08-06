# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypitmpl']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['pypitmpl = pypitmpl.cli:run']}

setup_kwargs = {
    'name': 'pypi-pkg-template',
    'version': '0.0.1rc7',
    'description': 'A Template for Python Package',
    'long_description': '# PyPI Template\n\n![][version-image]\n[![Release date][release-date-image]][release-url]\n[![License][license-image]][license-url]\n[![semantic-release][semantic-image]][semantic-url]\n[![Jupyter Book][jupyter-book-image]][jupyter-book-url]\n\nA Template for Python Packages\n\n## Usage\n\n### Create a new repository\n\n1. Click the `Use this template` button\n2. Enter a name for your repository\n3. Click `Create repository from template`\n\n## License\n\nThis project is released under the [MIT License][license-url].\n\n<!-- Links: -->\n\n[version-image]: https://img.shields.io/github/v/release/entelecheia/pypi-template?sort=semver\n[release-date-image]: https://img.shields.io/github/release-date/entelecheia/pypi-template\n[release-url]: https://github.com/entelecheia/pypi-template/releases\n[semantic-image]: https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg\n[semantic-url]: https://github.com/semantic-release/semantic-release\n[license-image]: https://img.shields.io/github/license/entelecheia/pypi-template\n[license-url]: https://github.com/entelecheia/pypi-template/blob/main/LICENSE\n[changelog-url]: https://github.com/entelecheia/pypi-template/blob/main/docs/CHANGELOG.md\n[jupyter-book-image]: https://jupyterbook.org/en/stable/_images/badge.svg\n[jupyter-book-url]: https://jupyterbook.org\n',
    'author': 'Young Joon Lee',
    'author_email': 'entelecheia@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
