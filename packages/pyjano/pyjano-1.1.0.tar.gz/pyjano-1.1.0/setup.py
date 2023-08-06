# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyjano',
 'pyjano.jana',
 'pyjano.plot',
 'pyjano.plugin_parser',
 'pyjano.server',
 'pyjano.server.socket']

package_data = \
{'': ['*'], 'pyjano.server': ['static/*', 'templates/*']}

setup_kwargs = {
    'name': 'pyjano',
    'version': '1.1.0',
    'description': 'Python JANA2 Orchestrator',
    'long_description': ":# pyjano\n\n![Pyjano](logo.png) \n\nPyjano stands for **Py**thon **Jan**a **O**rchestrator. Python wrapper over \n[jana2](https://github.com/JeffersonLab/JANA2) framework to make configuration\n and running convenient. \n\n**Install**\n\n```bash\npython3 -m pip install pyjano    # use --user for user level install\n```\n\nSimple configuration\n\n```python\nfrom pyjano.jana import Jana\njana = Jana()\n\n# Plugins configuration \njana.plugin('beagle_reader')\\\n    .plugin('vmeson')\\\n    .plugin('event_writer')\\\n    .plugin('jana', nevents=10000, output='beagle.root')\\\n    .source('../data/beagle_eD.txt')\n\n# Run\njana.run()\n```\n\nCustom executable\n",
    'author': 'Dmitry Romanov',
    'author_email': 'romanovda@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
