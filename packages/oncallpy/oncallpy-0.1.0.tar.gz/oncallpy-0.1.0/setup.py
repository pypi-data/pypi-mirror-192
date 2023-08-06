# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oncallpy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'oncallpy',
    'version': '0.1.0',
    'description': '',
    'long_description': 'On-call-py',
    'author': 'yehuda.l',
    'author_email': 'yehuda.l@taboola.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
