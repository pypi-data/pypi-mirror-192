# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['climap']

package_data = \
{'': ['*']}

install_requires = \
['rich==13.3.1']

entry_points = \
{'console_scripts': ['climap = climap.main:main']}

setup_kwargs = {
    'name': 'climap',
    'version': '0.1.1',
    'description': 'A rich command line utility for accessing emails',
    'long_description': '\n[![version](https://img.shields.io/pypi/v/climap?color=green)](https://pypi.org/project/climap/)\n[![supports](https://img.shields.io/pypi/pyversions/climap?color=blue&label=supports)](https://pypi.org/project/climap/)\n[![test coverage](https://codecov.io/gh/symonk/climap/branch/main/graph/badge.svg)](https://codecov.io/gh/symonk/climap)\n[![docs](https://img.shields.io/badge/documentation-online-brightgreen.svg)](https://symonk.github.io/climap/)\n\n\n# climap (**ALPHA**)\n\n-----\n\nA rich-based command line utility for IMAP. Written solely in python.\n',
    'author': 'symonk',
    'author_email': 'jackofspaces@gmail.com',
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
