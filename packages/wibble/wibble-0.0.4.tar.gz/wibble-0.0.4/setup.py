# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wibble']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['fafa = wibble.wobble:wobble']}

setup_kwargs = {
    'name': 'wibble',
    'version': '0.0.4',
    'description': 'Minimal python project that exposes a commandline feature',
    'long_description': '[![check](https://github.com/retospect/wibble/actions/workflows/check.yml/badge.svg)](https://github.com/retospect/wibble/actions/workflows/check.yml)\n# Wibble - a template for simple python packages\n\n\nA minimalist template for a python package.\n\nProvides the bl and the blarg commands.\n\n## Things to replace\n\n- ```grep -ri word .``` will find the *word* in all the files\n- ```find . | grep word``` will find the *word* in any filenames\n- *retospect* - changed to your github user name\n- *wibble* - change to the name of your project\n- *wobble* - change to the internal package name you want to use \n- *fafa* - change to whatever your commandline command should be if you are providing a script\n- update the pyproject.py file to have your name and the right description. \n',
    'author': 'Joe Schmoe',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/retospect/wibble',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
