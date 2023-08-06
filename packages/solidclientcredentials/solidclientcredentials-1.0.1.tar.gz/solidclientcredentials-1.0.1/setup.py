# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['solid_client_credentials', 'solid_client_credentials.tests']

package_data = \
{'': ['*']}

install_requires = \
['jwcrypto>=1.4.2,<2.0.0',
 'pyjwt>=2.6.0,<3.0.0',
 'types-requests>=2.28.11.13,<3.0.0.0']

setup_kwargs = {
    'name': 'solidclientcredentials',
    'version': '1.0.1',
    'description': 'Solid authentication with client credentials',
    'long_description': "# Solid Client Credentials\n\nSolid authentication with client credentials.\n\n[![Unix Build Status](https://img.shields.io/github/actions/workflow/status/Otto-AA/solid-client-credentials-py/main.yml?branch=main&label=linux)](https://github.com/Otto-AA/solid-client-credentials-py/actions)\n[![Windows Build Status](https://img.shields.io/appveyor/ci/Otto-AA/solid-client-credentials-py.svg?label=windows)](https://ci.appveyor.com/project/Otto-AA/solid-client-credentials-py)\n[![Coverage Status](https://img.shields.io/codecov/c/gh/Otto-AA/solid-client-credentials-py)](https://codecov.io/gh/Otto-AA/solid-client-credentials-py)\n[![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/g/Otto-AA/solid-client-credentials-py.svg)](https://scrutinizer-ci.com/g/Otto-AA/solid-client-credentials-py)\n[![PyPI License](https://img.shields.io/pypi/l/SolidClientCredentials.svg)](https://pypi.org/project/SolidClientCredentials)\n[![PyPI Version](https://img.shields.io/pypi/v/SolidClientCredentials.svg)](https://pypi.org/project/SolidClientCredentials)\n[![PyPI Downloads](https://img.shields.io/pypi/dm/SolidClientCredentials.svg?color=orange)](https://pypistats.org/packages/SolidClientCredentials)\n\n## Setup\n\n### Requirements\n\n* Python 3.10+ (likely works with lower versions, but not tested)\n\n### Installation\n\n```bash\n$ pip install SolidClientCredentials\n```\n\n## Use Case\n\n!!! note\n    Client credentials are not standardized, thus you can't run your application through any Solid pod. However, users from any provider can give your app access through standardized mechanisms (eg ACL).\n\n\nYou can use client credentials to create a server-side application that authenticates as a webId on ESS or CSS. After obtaining the client credentials for a webId, you can use them to make authenticated requests on behalf of this account. You will be able to access all resources this webId has access to. If you want to access data of other users, they must grant access rights to your apps webId.\n\nSee also: [https://docs.inrupt.com/developer-tools/javascript/client-libraries/tutorial/authenticate-nodejs-script/](https://docs.inrupt.com/developer-tools/javascript/client-libraries/tutorial/authenticate-nodejs-script/)\n\n## Usage\n\nTo use this package you first need valid client credentials (see [below](#obtaining-client-credentials)). Given the client credentials you can use it as follows:\n\n```python\nfrom solid_client_credentials import SolidClientCredentialsAuth, DpopTokenProvider\nimport requests\n\nclient_id = 'your-id'\nclient_secret = 'your-secret'\n\n# The server that provides your account (where you login)\nissuer_url = 'https://login.inrupt.com'\n\n# create a token provider\ntoken_provider = DpopTokenProvider(\n    token_endpoint=token_endpoint,\n    client_id=client_id,\n    client_secret=client_secret\n)\n# use the tokens with the requests library\nauth = SolidClientCredentialsAuth(token_provider)\n\nres = requests.get('https://example.org/private/stuff', auth=auth)\nprint(res.text)\n```\n\n## Obtaining client credentials\n\nThis is currently only possible with ESS and CSS.\n\n### ESS\n\nESS allows to manually obtain client credentials: [https://login.inrupt.com/registration.html](https://login.inrupt.com/registration.html)\n\n### CSS\n\nCSS allows to automatically obtain client credentials: [https://communitysolidserver.github.io/CommunitySolidServer/5.x/usage/client-credentials/](https://communitysolidserver.github.io/CommunitySolidServer/5.x/usage/client-credentials/)\n\nYou can also look at `css_utils.py` to see how this maps to python.\n\n",
    'author': 'A_A',
    'author_email': '21040751+Otto-AA@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pypi.org/project/SolidClientCredentials',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
