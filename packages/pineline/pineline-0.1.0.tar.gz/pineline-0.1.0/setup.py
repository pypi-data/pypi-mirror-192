# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pineline']

package_data = \
{'': ['*']}

install_requires = \
['eko>=0.12.0,<0.13.0', 'pineappl>=0.5.9,<0.6.0', 'pineko>=0.3.3,<0.4.0']

setup_kwargs = {
    'name': 'pineline',
    'version': '0.1.0',
    'description': 'Theory predictions for PDF fitting',
    'long_description': '# Pineline\n',
    'author': 'Alessandro Candido',
    'author_email': 'candido.ale@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
