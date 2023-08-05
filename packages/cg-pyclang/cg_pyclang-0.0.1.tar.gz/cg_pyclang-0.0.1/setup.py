# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cg', 'cg.pyclang']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cg-pyclang',
    'version': '0.0.1',
    'description': 'For Doing Clang Things in Python...',
    'long_description': '# PyClang - For Doing Clang Things in Python...\n\n<!-- ToDo -->\n',
    'author': 'ChunkyGrumbler',
    'author_email': 'ChunkyGrumbler@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ChunkyGrumbler/PyClang',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
