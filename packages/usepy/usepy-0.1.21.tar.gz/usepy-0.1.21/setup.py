# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['usepy', 'usepy.data', 'usepy.decorator', 'usepy.utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'usepy',
    'version': '0.1.21',
    'description': 'usepy',
    'long_description': 'None',
    'author': 'miclon',
    'author_email': 'jcnd@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
