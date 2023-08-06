# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oc_idmanager']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'lxml>=4.9.1,<5.0.0',
 'oc-meta==1.2.3',
 'requests>=2.28.1,<3.0.0',
 'validators>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'oc-idmanager',
    'version': '0.2.5',
    'description': 'This library allows validating identifiers with DOI, ISBN, ISSN, ORCID, PMCID, and PMID schemes',
    'long_description': 'None',
    'author': 'Silvio Peroni',
    'author_email': 'essepuntato@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.4,<4.0.0',
}


setup(**setup_kwargs)
