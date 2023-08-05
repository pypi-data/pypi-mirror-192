# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kimfame']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'kimfame',
    'version': '0.0.12',
    'description': 'PyPI test project',
    'long_description': '# Kimfame\n\nPyPI Test Project',
    'author': 'kimfame',
    'author_email': 'renownkim@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kimfame/kimfame',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
