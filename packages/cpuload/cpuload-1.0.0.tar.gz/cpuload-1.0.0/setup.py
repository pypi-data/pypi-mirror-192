# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cpuload']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'psutil>=5.9.4,<6.0.0']

entry_points = \
{'console_scripts': ['cpuload = cpuload.cpuload:main']}

setup_kwargs = {
    'name': 'cpuload',
    'version': '1.0.0',
    'description': 'Python tool to generate CPU load',
    'long_description': '',
    'author': 'Alexey Vyskubov',
    'author_email': 'alexey@ocaml.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
