# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['devtools',
 'devtools.exceptions',
 'devtools.models',
 'devtools.providers',
 'devtools.providers.database',
 'devtools.providers.database.types',
 'devtools.types',
 'devtools.utils']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.4,<2.0.0', 'pytest>=7.2.1,<8.0.0']

setup_kwargs = {
    'name': 'eric-devtools',
    'version': '0.1.1',
    'description': '',
    'long_description': '',
    'author': 'Eric Batista',
    'author_email': 'klose.eric31@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
