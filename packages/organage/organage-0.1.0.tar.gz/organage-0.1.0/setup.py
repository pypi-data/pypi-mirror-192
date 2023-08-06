# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['organage']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'organage',
    'version': '0.1.0',
    'description': 'A package to pestimate organ-specific biological age using SomaScan plasma proteomics data',
    'long_description': '# organage\n\nA package to pestimate organ-specific biological age using SomaScan plasma proteomics data\n\n## Installation\n\n```bash\n$ pip install OrganAge\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`organage` was created by Hamilton Oh. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`organage` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Hamilton Oh',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
