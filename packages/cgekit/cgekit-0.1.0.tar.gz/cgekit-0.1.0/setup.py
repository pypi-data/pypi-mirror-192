# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cgekit']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cgekit',
    'version': '0.1.0',
    'description': 'Additional tools for the cgePy library',
    'long_description': '',
    'author': 'catbox305',
    'author_email': 'lion712yt@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
