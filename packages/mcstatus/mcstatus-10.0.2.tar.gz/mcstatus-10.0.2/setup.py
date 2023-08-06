# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'mcstatus'}

packages = \
['mcstatus', 'mcstatus.protocol', 'protocol']

package_data = \
{'': ['*']}

install_requires = \
['asyncio-dgram==2.1.2', 'dnspython==2.2.1']

entry_points = \
{'console_scripts': ['mcstatus = mcstatus.__main__:main']}

setup_kwargs = {
    'name': 'mcstatus',
    'version': '10.0.2',
    'description': 'A library to query Minecraft Servers for their status and capabilities.',
    'long_description': '# <img src="https://i.imgur.com/nPCcxts.png" height=25> MCStatus\n\n[![discord chat](https://img.shields.io/discord/936788458939224094.svg?logo=Discord)](https://discord.gg/C2wX7zduxC)\n![supported python versions](https://img.shields.io/pypi/pyversions/mcstatus.svg)\n[![current PyPI version](https://img.shields.io/pypi/v/mcstatus.svg)](https://pypi.org/project/mcstatus/)\n[![Validation](https://github.com/py-mine/mcstatus/actions/workflows/validation.yml/badge.svg)](https://github.com/py-mine/mcstatus/actions/workflows/validation.yml)\n[![Tox test](https://github.com/py-mine/mcstatus/actions/workflows/tox-test.yml/badge.svg)](https://github.com/py-mine/mcstatus/actions/workflows/tox-test.yml)\n\nMcstatus provides an API and command line script to fetch publicly available data from Minecraft servers. Specifically, mcstatus retrieves data by using these protocols: [Server List Ping](https://wiki.vg/Server_List_Ping) and [Query](https://wiki.vg/Query). Because of mcstatus, you do not need to fully understand those protocols and can instead skip straight to retrieving minecraft server data quickly in your own programs.\n\n## Installation\n\nMcstatus is available on [PyPI](https://pypi.org/project/mcstatus/), and can be installed trivially with:\n\n```bash\npython3 -m pip install mcstatus\n```\n\n## Usage\n\n### Python API\n\n#### Java Edition\n\n```python\nfrom mcstatus import JavaServer\n\n# You can pass the same address you\'d enter into the address field in minecraft into the \'lookup\' function\n# If you know the host and port, you may skip this and use JavaServer("example.org", 1234)\nserver = JavaServer.lookup("example.org:1234")\n\n# \'status\' is supported by all Minecraft servers that are version 1.7 or higher.\n# Don\'t expect the player list to always be complete, because many servers run\n# plugins that hide this information or limit the number of players returned or even\n# alter this list to contain fake players for purposes of having a custom message here.\nstatus = server.status()\nprint(f"The server has {status.players.online} player(s) online and replied in {status.latency} ms")\n\n# \'ping\' is supported by all Minecraft servers that are version 1.7 or higher.\n# It is included in a \'status\' call, but is also exposed separate if you do not require the additional info.\nlatency = server.ping()\nprint(f"The server replied in {latency} ms")\n\n# \'query\' has to be enabled in a server\'s server.properties file!\n# It may give more information than a ping, such as a full player list or mod information.\nquery = server.query()\nprint(f"The server has the following players online: {\', \'.join(query.players.names)}")\n```\n\n#### Bedrock Edition\n\n```python\nfrom mcstatus import BedrockServer\n\n# You can pass the same address you\'d enter into the address field in minecraft into the \'lookup\' function\n# If you know the host and port, you may skip this and use BedrockServer("example.org", 19132)\nserver = BedrockServer.lookup("example.org:19132")\n\n# \'status\' is the only feature that is supported by Bedrock at this time.\n# In this case status includes players_online, latency, motd, map, gamemode, and players_max. (ex: status.gamemode)\nstatus = server.status()\nprint(f"The server has {status.players_online} players online and replied in {status.latency} ms")\n```\n\n### Command Line Interface\n\nThis only works with Java servers; Bedrock is not yet supported. Use `mcstatus -h` to see helpful information on how to use this script.\n\n## License\n\nMcstatus is licensed under the Apache 2.0 license. See LICENSE for full text.\n',
    'author': 'Nathan Adams',
    'author_email': 'dinnerbone@dinnerbone.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/py-mine/mcstatus',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
