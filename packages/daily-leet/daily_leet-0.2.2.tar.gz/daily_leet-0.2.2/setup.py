# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['daily_leet', 'daily_leet.language_support']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0', 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['leetcode = daily_leet.main:app']}

setup_kwargs = {
    'name': 'daily-leet',
    'version': '0.2.2',
    'description': '',
    'long_description': '',
    'author': 'madmaxieee',
    'author_email': '76544194+madmaxieee@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
