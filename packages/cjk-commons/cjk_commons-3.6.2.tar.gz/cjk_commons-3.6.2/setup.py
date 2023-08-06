# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cjk_commons']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'loguru>=0.6.0,<0.7.0',
 'pyyaml>=6.0,<7.0',
 'yodl>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'cjk-commons',
    'version': '3.6.2',
    'description': 'Commons',
    'long_description': 'Commons\n===\n',
    'author': 'Cujoko',
    'author_email': 'cujoko@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Cujoko/commons',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
