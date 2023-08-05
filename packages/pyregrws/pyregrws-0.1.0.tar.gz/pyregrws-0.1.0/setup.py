# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['regrws', 'regrws.api', 'regrws.models']

package_data = \
{'': ['*']}

install_requires = \
['pydantic-xml[lxml]>=0.5.0,<0.6.0',
 'pydantic[dotenv]>=1.10.4,<2.0.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'pyregrws',
    'version': '0.1.0',
    'description': "Python library to retrieve and modify records within ARIN's database through their Reg-RWS service",
    'long_description': 'None',
    'author': 'Jonathan Senecal',
    'author_email': 'contact@jonathansenecal.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
