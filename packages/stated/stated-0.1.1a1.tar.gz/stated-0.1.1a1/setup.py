# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stated']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'stated',
    'version': '0.1.1a1',
    'description': 'Distributed State in memory',
    'long_description': '# stated\n\nStated aims to provide distributed state in memory(and persistant) purely in python, example usecases can be for example syncronising state among pods in a set of kubernets pods.\n',
    'author': 'Abbas Jafari',
    'author_email': 'abbas.jafari@powercoders.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
