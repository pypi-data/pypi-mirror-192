# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['psychopy_pixx',
 'psychopy_pixx.calibration',
 'psychopy_pixx.calibration..ipynb_checkpoints',
 'psychopy_pixx.devices']

package_data = \
{'': ['*'], 'psychopy_pixx.devices': ['shaders/*']}

install_requires = \
['click>=8.1.3,<9.0.0']

entry_points = \
{'console_scripts': ['pixxcalibrate = '
                     'psychopy_pixx.calibration.calibration:calibration_routine_cli']}

setup_kwargs = {
    'name': 'psychopy-pixx',
    'version': '0.1.0',
    'description': 'Psychopy plugin for high-bit luminance and VPixx devices',
    'long_description': None,
    'author': 'David-Elias Kuenstle',
    'author_email': 'david-elias.kuenstle@uni-tuebingen.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
