# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['paperbush']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'paperbush',
    'version': '0.2.0',
    'description': 'Super concise argument parsing tool',
    'long_description': 'None',
    'author': 'trag1c',
    'author_email': 'trag1cdev@yahoo.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
