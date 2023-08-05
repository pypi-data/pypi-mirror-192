# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lendl_equivalent_method']

package_data = \
{'': ['*']}

install_requires = \
['pyroll-core>=2.0.0b,<3.0.0']

setup_kwargs = {
    'name': 'pyroll-lendl-equivalent-method',
    'version': '2.0.0b0',
    'description': "Plugin for PyRoll providing Lendl's equivalent rectangle method",
    'long_description': '# PyRoll Lendl Equivalent Method\n\nPlugin for PyRoll providing the equivalent method from A.E. Lendl.\n\nFor the docs, see [here](docs/docs.pdf).\n\nThis project is licensed under the [BSD-3-Clause license](LICENSE).\n\nThe package is available via [PyPi](https://pypi.org/project/pyroll-lendl-euquivalent-method/) and can be installed with\n    \n    pip install pyroll-lendl-equivalent-method',
    'author': 'Christoph Renzing',
    'author_email': 'christoph.renzing@imf.tu-freiberg.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pyroll-project.github.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
