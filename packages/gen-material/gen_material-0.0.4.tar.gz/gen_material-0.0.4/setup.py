# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gen_material', 'gen_material.data']

package_data = \
{'': ['*'],
 'gen_material': ['assets/*', 'assets/bg/*', 'assets/font/*', 'assets/frame/*']}

setup_kwargs = {
    'name': 'gen-material',
    'version': '0.0.4',
    'description': '5dfsfddsfd',
    'long_description': 'HI',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
