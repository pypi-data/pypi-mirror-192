# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['py_mp', 'py_mp.commands', 'py_mp.models', 'py_mp.network']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-multiplayer',
    'version': '0.1.2',
    'description': 'Server Client Structure for Python',
    'long_description': '# Python Multiplayer\n\n<a href="https://pypi.org/project/python-multiplayer/"><img src="https://badge.fury.io/py/python-multiplayer.png" alt="PyPI version" height="18"></a>\n\nFramework for Client Server Structure in Python.\nIs intended to be used for multiplayer games in pygame with this Module.\n\n[pygame-multiplayer](https://github.com/BroCodeAT/python-multiplayer)\n\n----\n\n## Planned features\n- [x] Command based Network\n- [ ] Threaded Network\n- [ ] Async Network\n\n\n## Installation\n\n```bash\npip install python-multiplayer\n```\n\n## Usage (Command Server/Client)\n\nServer:\n```python\nfrom py_mp import CommandServer\nfrom py_mp import ServerSideServerCommand\nfrom py_mp.commands import NetworkFlag\n\nserver = CommandServer("localhost", 5000)\nserver.accept()\n\n# Receive a Command from the Client\ncom = server.recv(server.clients[0])\nprint(com)\n\n# Send a Test Command back to the Client\nserver.send(\n    ServerSideServerCommand(NetworkFlag.CONNECTED, server.clients[0], test="test"), \n    server.clients[0]\n)\n```\nClient:\n```python\nfrom py_mp import CommandClient\nfrom py_mp import ClientCommand\nfrom py_mp.commands import NetworkFlag\n\nclient = CommandClient("localhost", 5000)\n\n# Send a Test Command to the Server\nclient.send(ClientCommand(NetworkFlag.CONNECTED, test="test"))\n\n# Receive a Command from the Server\ncom = client.recv()\nprint(com)\n```\n',
    'author': 'dpfurners',
    'author_email': 'dpfurner@tsn.at',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/BroCodeAT/python-multiplayer',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
