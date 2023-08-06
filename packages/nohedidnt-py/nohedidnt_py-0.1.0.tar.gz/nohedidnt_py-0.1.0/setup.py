# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nohedidnt_py']

package_data = \
{'': ['*']}

install_requires = \
['codetiming>=1.4.0,<2.0.0',
 'devtools[pygments]>=0.10.0,<0.11.0',
 'pydantic[email]>=1.10.4,<2.0.0',
 'python-box[all]>=7.0.0,<8.0.0',
 'python-dotenv>=0.21.1,<0.22.0',
 'pytz>=2022.7.1,<2023.0.0',
 'urllib3>=1.26.14,<2.0.0']

setup_kwargs = {
    'name': 'nohedidnt-py',
    'version': '0.1.0',
    'description': '',
    'long_description': '# nohedidnt_py\n\n[![codecov](https://codecov.io/gh/NoHeDidnt/nohedidnt_py/branch/main/graph/badge.svg?token=U0OQI580BA)](https://codecov.io/gh/NoHeDidnt/nohedidnt_py)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)\n\n## [License](./LICENSE)\n',
    'author': 'NoHeDidnt',
    'author_email': 'dj@nohedidnt.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
