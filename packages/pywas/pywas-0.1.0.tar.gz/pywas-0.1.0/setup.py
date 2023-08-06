# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pywas', 'pywas.parse', 'pywas.wrapper']

package_data = \
{'': ['*'], 'pywas': ['template/*']}

install_requires = \
['fastapi-jsonrpc>=2.2.0,<3.0.0',
 'h5py>=3.7.0,<4.0.0',
 'jinja2>=3.1.2,<4.0.0',
 'numpy>=1.23.2,<2.0.0',
 'pyyaml>=6.0,<7.0',
 'typer[all]>=0.6.0,<0.7.0',
 'uvicorn[standard]>=0.20.0,<0.21.0',
 'wget>=3.2,<4.0']

entry_points = \
{'console_scripts': ['pywas = pywas.main:cli']}

setup_kwargs = {
    'name': 'pywas',
    'version': '0.1.0',
    'description': '',
    'long_description': '# `pywas`\n\n**Usage**:\n\n```console\n$ pywas [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* For a given wrapper:\n  * `install`: install the software on the system.\n  * `prepare`: not implemented yet. Set everything up for the next simulation.\n  * `run`: run the simulation and store the output in results.\n  * `export`: export the results as a .hdf5 file.\n',
    'author': 'Patarimi',
    'author_email': 'mpqqch@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
