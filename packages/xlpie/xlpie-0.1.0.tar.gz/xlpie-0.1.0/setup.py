# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xlpie']

package_data = \
{'': ['*']}

install_requires = \
['pywin32>=305,<306', 'rich>=13.3.1,<14.0.0']

setup_kwargs = {
    'name': 'xlpie',
    'version': '0.1.0',
    'description': 'Python classes for simple MS Excel interactions',
    'long_description': '# xlpie',
    'author': 'PeluxGit',
    'author_email': '63825662+PeluxGit@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
