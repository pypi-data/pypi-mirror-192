# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pavpy']

package_data = \
{'': ['*']}

install_requires = \
['astropy==5.1.1',
 'astroquery==0.4.7.dev8076',
 'dustmaps==1.0.10',
 'numpy==1.23.3',
 'pandas==1.5.0',
 'scipy==1.9.1']

setup_kwargs = {
    'name': 'pavpy',
    'version': '0.1.0',
    'description': 'A package for analysing PAVO observations in Python',
    'long_description': '# pavpy\n[![Licence](http://img.shields.io/badge/license-GPLv3-blue.svg?style=flat)](http://www.gnu.org/licenses/gpl-3.0.html)\n\nA package for analysing PAVO observations in Python',
    'author': 'Tim White',
    'author_email': 'tim.white@sydney.edu.au',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
