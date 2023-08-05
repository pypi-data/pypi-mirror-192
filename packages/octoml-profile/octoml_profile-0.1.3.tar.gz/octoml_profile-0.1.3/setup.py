# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['octoml_profile', 'octoml_profile.interceptors', 'octoml_profile.protos']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'octoml-profile',
    'version': '0.1.3',
    'description': 'Client package for OctoML Profile service',
    'long_description': None,
    'author': 'Greg Bonik',
    'author_email': 'gbonik@octoml.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
