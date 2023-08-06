# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cytocluster', 'cytocluster.methods', 'cytocluster.tests']

package_data = \
{'': ['*']}

install_requires = \
['MiniSom>=2.3.0,<3.0.0',
 'PhenoGraph>=1.5.7,<2.0.0',
 'cytoplots>=0.1.0,<0.2.0',
 'cytotools>=0.1.21,<0.2.0',
 'ensembleclustering==1.0.2',
 'hdmedians>=0.14.2,<0.15.0',
 'hnswlib>=0.6.2,<0.7.0',
 'ipython>=8.4.0,<9.0.0',
 'jupyter>=1.0.0,<2.0.0',
 'llvmlite>=0.39,<0.40',
 'pandas>=1.4.3,<2.0.0']

setup_kwargs = {
    'name': 'cytocluster',
    'version': '0.1.13',
    'description': 'A package for clustering high-dimensional cytometry data in Python.',
    'long_description': '<p align="center">\n  <img src="https://i.imgur.com/cBdvN9o.png" height="25%" width="25%">\n</p>\n\n# CytoCluster\n[![PyPi](https://img.shields.io/pypi/v/cytocluster)](https://pypi.org/project/cytocluster/)\n[![Python](https://img.shields.io/pypi/pyversions/cytocluster)](https://pypi.org/project/cytocluster/)\n[![Wheel](https://img.shields.io/pypi/wheel/cytocluster)](https://pypi.org/project/cytocluster/)\n[![License]( https://img.shields.io/pypi/l/cytocluster)](https://opensource.org/licenses/MIT)\n[![LastCommit](https://img.shields.io/github/last-commit/burtonrj/cytocluster)]()\n[![CodeCov](https://img.shields.io/codecov/c/github/burtonrj/cytocluster)]()\n[![GitHubActions](https://img.shields.io/github/workflow/status/burtonrj/cytocluster/CytoCluster%20Build)]()\n\n---\n\n## Overview\n\nWelcome! This is CytoCluster, a package for clustering high-dimensional cytometry data in Python.\nCytoCluster started as a module in the first release of <a src="https://github.com/burtonrj/CytoPy">CytoPy</a>.\n\nCytoCluster is now a standalone package that provides functions and classes for:\n\n* Popular clustering algorithms such as FlowSOM, Phenograph, SPADE etc.\n* Plotting and visualising clustering results.\n* Ensemble clustering for combining the results of many clustering algorithms into consensus clusters.\n\nExamples of using the CytoCluster package are provided in the example notebooks (see notebooks folder in this repo).\n\n## Installation\n\n``\npip install cytocluster\n``\n\n---\n## Release Notes\n\nThe CytoPy ecosystem is under development, see ### for details on release information.\n',
    'author': 'burtonrj',
    'author_email': 'burtonrj@cardiff.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/burtonrj/CytoCluster',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
