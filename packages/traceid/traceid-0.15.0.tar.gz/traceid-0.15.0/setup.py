# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['traceid']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'traceid',
    'version': '0.15.0',
    'description': '',
    'long_description': '# TraceId\n\na \n\n## title\naskldjl\n',
    'author': 'Yibu Ma',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
