# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['riboswitchinator']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['swin = riboswitchinator.executable:switchinator_main']}

setup_kwargs = {
    'name': 'riboswitchinator',
    'version': '0.0.1',
    'description': 'Tool to generate riboswitches for specific sequences',
    'long_description': '# Switchinator\n\nTranslates riboswitch logic gates to different sequences.\n\nIt provides the `swin` commandline command.\n\n',
    'author': 'Reto Stamm',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/retospect/riboswitchinator',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
