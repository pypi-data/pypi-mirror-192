# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dems']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=3.10,<5.0', 'xarray-dataclasses>=1.4,<2.0']

setup_kwargs = {
    'name': 'dems',
    'version': '0.1.0',
    'description': 'DESHIMA measurement set',
    'long_description': '# dems\nDESHIMA measurement set\n',
    'author': 'Akio Taniguchi',
    'author_email': 'taniguchi@a.phys.nagoya-u.ac.jp',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
