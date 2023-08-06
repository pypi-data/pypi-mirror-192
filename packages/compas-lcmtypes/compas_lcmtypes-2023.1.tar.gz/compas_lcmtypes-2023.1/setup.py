# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['compas_lcmtypes',
 'compas_lcmtypes.bot_core',
 'compas_lcmtypes.navlcm',
 'compas_lcmtypes.oi',
 'compas_lcmtypes.senlcm']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'compas-lcmtypes',
    'version': '2023.1',
    'description': 'CoMPAS LCM types',
    'long_description': 'None',
    'author': 'Kevin Barnard',
    'author_email': 'kbarnard@mbari.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
