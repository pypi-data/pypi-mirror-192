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
    'version': '0.1.1',
    'description': "Python library to retrieve and modify records within ARIN's database through their Reg-RWS service",
    'long_description': '# pyregrws\n\n[![CI](https://github.com/jsenecal/pyregrws/actions/workflows/ci.yml/badge.svg?branch=main&event=push)](https://github.com/jsenecal/pyregrws/actions/workflows/ci.yml)  \n[![codecov](https://codecov.io/github/jsenecal/pyregrws/branch/main/graph/badge.svg?token=G5CK0SWY41)](https://codecov.io/github/jsenecal/pyregrws)\n\n## Currently Supported Payloads\n\n- [POC](https://www.arin.net/resources/manage/regrws/payloads/#poc-payload)\n- [Customer](https://www.arin.net/resources/manage/regrws/payloads/#customer-payload)\n- [ORG](https://www.arin.net/resources/manage/regrws/payloads/#org-payload)\n- [NET Block](https://www.arin.net/resources/manage/regrws/payloads/#net-block-payload)\n- [NET](https://www.arin.net/resources/manage/regrws/payloads/#net-payload)\n- [POC Link](https://www.arin.net/resources/manage/regrws/payloads/#poc-link-payload)\n\n- [Ticketed Request Payload](https://www.arin.net/resources/manage/regrws/payloads/#ticketed-request-payload)\n- [Ticket Payload](https://www.arin.net/resources/manage/regrws/payloads/#ticket-payload)\n\n- [Error](https://www.arin.net/resources/manage/regrws/payloads/#error-payload)\n',
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
