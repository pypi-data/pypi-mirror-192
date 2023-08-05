# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['modelos',
 'modelos.env',
 'modelos.env.image',
 'modelos.object',
 'modelos.pkg',
 'modelos.pkg.repo',
 'modelos.pkg.scheme',
 'modelos.run',
 'modelos.run.kube',
 'modelos.util',
 'modelos.virtual.container']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.30,<4.0.0',
 'black>=23.1.0,<24.0.0',
 'cloudpickle>=2.2.1,<3.0.0',
 'dataclasses-jsonschema>=2.16.0,<3.0.0',
 'deepdiff>=6.2.3,<7.0.0',
 'docker-image-py>=0.1.12,<0.2.0',
 'docker>=6.0.1,<7.0.0',
 'isort>=5.12.0,<6.0.0',
 'kubernetes>=25.3.0,<26.0.0',
 'lib-programname>=2.0.5,<3.0.0',
 'ocifacts>=0.0.9,<0.0.10',
 'opencontainers>=0.0.14,<0.0.15',
 'removestar>=1.3.1,<2.0.0',
 'rich>=13.3.1,<14.0.0',
 'semver>=2.13.0,<3.0.0',
 'starlette>=0.24.0,<0.25.0',
 'unimport>=0.14.1,<0.15.0',
 'uvicorn[standard]>=0.20.0,<0.21.0',
 'xdg>=5.1.1,<6.0.0']

setup_kwargs = {
    'name': 'modelos',
    'version': '0.1.3',
    'description': 'An operating system for machine learning',
    'long_description': None,
    'author': 'Patrick Barker',
    'author_email': 'patrickbarkerco@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
