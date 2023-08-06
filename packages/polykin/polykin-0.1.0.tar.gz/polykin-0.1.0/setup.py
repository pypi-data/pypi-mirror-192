# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['polykin', 'polykin.copolymerization', 'polykin.distributions']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.2,<4.0.0',
 'mpmath>=1.2.1,<2.0.0',
 'numba>=0.56.4,<0.57.0',
 'numpy>=1.23',
 'pydantic>=1.10.4,<2.0.0',
 'scipy>=1.9.3,<2.0.0']

setup_kwargs = {
    'name': 'polykin',
    'version': '0.1.0',
    'description': 'A polymerization kinetics library.',
    'long_description': '# PolyKin\n\n[![CI](https://github.com/HugoMVale/polykin/actions/workflows/CI.yml/badge.svg)](https://github.com/HugoMVale/polykin/actions)\n[![codecov](https://codecov.io/gh/HugoMVale/polykin/branch/main/graph/badge.svg?token=QfqQLX2rHx)](https://codecov.io/gh/HugoMVale/polykin)\n[![Latest Commit](https://img.shields.io/github/last-commit/HugoMVale/polykin)](https://img.shields.io/github/last-commit/HugoMVale/polykin)\n\nPolyKin is an open-source polymerization kinetics library for Python. It is still at an early\ndevelopment stage, but the following modules can already be used:\n\n- [x] distributions\n- [ ] copolymerization\n- [ ] kinetics\n- [ ] database\n- [ ] models\n\n## Documentation\n\nPlease refer to the package [homepage](https://hugomvale.github.io/polykin/).\n\n## Tutorials\n\nThe main features of PolyKin are explained and illustrated through a series of [tutorials](https://hugomvale.github.io/polykin/tutorials/distributions/) based on Jupyter [notebooks](https://github.com/HugoMVale/polykin/tree/main/docs/tutorials),\nwhich can be launched online via Binder.\n\n<p align="center">\n  <a href="https://github.com/HugoMVale/polykin">\n  <img src="https://raw.githubusercontent.com/HugoMVale/polykin/8e54e0b492b4dd782c2fe92b52f617dda71a29b3/docs/deconvolution.svg" width=600 alt="MWD of a polymer blend">\n  </a>\n</p>\n\n## Installation\n\nPolyKin currently runs on Python 3.9+. You can install it from PyPI via `pip` (or `poetry`):\n\n```console\npip install polykin\n# poetry add polykin\n```\n\nAlternatively, you may install it directly from the source code repository:\n\n```console\ngit clone https://github.com/HugoMVale/polykin.git\ncd polykin\npip install . \n# poetry install\n```\n',
    'author': 'HugoMVale',
    'author_email': '57530119+HugoMVale@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://hugomvale.github.io/polykin/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4',
}


setup(**setup_kwargs)
