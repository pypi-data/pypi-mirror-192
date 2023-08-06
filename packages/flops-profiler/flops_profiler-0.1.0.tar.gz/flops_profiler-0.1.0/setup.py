# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flops_profiler']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata>=6.0.0,<7.0.0']

setup_kwargs = {
    'name': 'flops-profiler',
    'version': '0.1.0',
    'description': '',
    'long_description': 'None',
    'author': 'Cheng Li',
    'author_email': 'pistasable@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
