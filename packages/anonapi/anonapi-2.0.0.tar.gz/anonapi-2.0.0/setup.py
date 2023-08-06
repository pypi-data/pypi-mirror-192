# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['anonapi', 'anonapi.cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'fileselection>=0.3.2,<0.4.0',
 'openpyxl>=3.1.0,<4.0.0',
 'pydicom>=2.3.1,<3.0.0',
 'requests>=2.28.2,<3.0.0',
 'tabulate>=0.9.0,<0.10.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'anonapi',
    'version': '2.0.0',
    'description': 'Client and tools for working with the anoymization web API',
    'long_description': '# AnonAPI\n\n\n[![CI](https://github.com/sjoerdk/anonapi/actions/workflows/build.yml/badge.svg?branch=master)](https://github.com/sjoerdk/anonapi/actions/workflows/build.yml?query=branch%3Amaster)\n[![PyPI](https://img.shields.io/pypi/v/anonapi)](https://pypi.org/project/anonapi/)\n[![Code Climate](https://codeclimate.com/github/sjoerdk/anonapi/badges/gpa.svg)](https://codeclimate.com/github/sjoerdk/anonapi)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/anonapi)](https://pypi.org/project/anonapi/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n\n\nClient and tools for working with the IDIS web API\n\n\n* Free software: MIT license\n* Documentation: https://anonapi.readthedocs.io.\n\n\nFeatures\n--------\n\n* Interact with IDIS anonymization server web API via https\n* Create, modify, cancel anonymization jobs\n* CLI (Command Line Interface) for quick overview of jobs and cancel/restart job.\n* Python code with examples for fully automated interaction\n\nCredits\n-------\n\nThis package was originally created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)',
    'author': 'sjoerdk',
    'author_email': 'sjoerd.kerkstra@radboudumc.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
