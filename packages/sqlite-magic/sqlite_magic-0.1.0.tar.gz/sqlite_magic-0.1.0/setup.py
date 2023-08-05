# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlite_magic']

package_data = \
{'': ['*']}

install_requires = \
['ipython>=6.0.0', 'pandas>=1.0.0']

setup_kwargs = {
    'name': 'sqlite-magic',
    'version': '0.1.0',
    'description': '',
    'long_description': '## `sqlite_magic`\n\nThis library implements basic `Ipython` magic commands for interfacing with a `sqlite3` database, using `pandas.read_sql_query` to execute and display query results.\n\n',
    'author': 'Todd Iverson',
    'author_email': 'Tiverson@winona.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
