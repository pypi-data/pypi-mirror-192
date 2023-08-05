# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['integral_thermal']

package_data = \
{'': ['*']}

install_requires = \
['pyroll-core>=2.0.0rc,<3.0.0']

setup_kwargs = {
    'name': 'pyroll-integral-thermal',
    'version': '2.0.0rc0',
    'description': 'Plugin for PyRoll providing an integral approach for thermal modelling.',
    'long_description': '# PyRoll Integral Thermal Model\n\nPlugin for PyRoll providing an integral approach for thermal modelling.\n\n## Documentation\n\nSee the [documentation](https://pyroll-project.github.io/modules/pyroll-integral-thermal/docs/docs) to learn about basic\nconcepts and usage.\n\n## License\n\nThe project is licensed under the [BSD 3-Clause license](LICENSE).\n\n## Installation\n\nThe package is available via [PyPi](https://pypi.org/project/pyroll-integral-thermal/) and can be installed with\n    \n    pip install pyroll-integral-thermal',
    'author': 'Max Weiner',
    'author_email': 'max.weiner@imf.tu-freiberg.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pyroll-project.github.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
