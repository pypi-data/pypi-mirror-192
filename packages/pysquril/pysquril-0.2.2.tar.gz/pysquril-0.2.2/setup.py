# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysquril']

package_data = \
{'': ['*']}

install_requires = \
['psycopg2-binary>=2.9.3,<3.0.0']

setup_kwargs = {
    'name': 'pysquril',
    'version': '0.2.2',
    'description': 'Python implementation of structured URI query language',
    'long_description': 'None',
    'author': 'Leon du Toit',
    'author_email': 'l.c.d.toit@usit.uio.no',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/unioslo/pysquril',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
