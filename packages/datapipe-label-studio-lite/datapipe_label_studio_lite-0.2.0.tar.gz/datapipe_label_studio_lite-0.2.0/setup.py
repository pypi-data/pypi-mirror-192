# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datapipe_label_studio_lite']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.25,<2.0.0',
 'datapipe-core[sqlite]>=0.11.12-dev.1,<0.12',
 'iteration-utilities>=0.11.0,<0.12.0',
 'label-studio-sdk>=0.0.16,<0.0.17',
 'numpy>=1.21.0,<2.0.0',
 'pandas>=1.2.0,<2.0.0',
 'requests>=2.24.0,<3.0.0',
 'tqdm>=4.60.0,<5.0.0']

setup_kwargs = {
    'name': 'datapipe-label-studio-lite',
    'version': '0.2.0',
    'description': '',
    'long_description': 'None',
    'author': 'Alexander Kozlov',
    'author_email': 'bobokvsky@epoch8.co',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
