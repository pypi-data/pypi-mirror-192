# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mc_players']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['mc_players = mc_players.playerlist:entry']}

setup_kwargs = {
    'name': 'mc-players',
    'version': '2.0.0',
    'description': 'List the players that have signed to a minecraft server lately',
    'long_description': "# Minecraft Server Player List\n\nQuick script that generates a list of recent players on your server, sorted\nin order of who last logged in. Works by looking at the last modified time of\ntheir `player.dat` files in `<server root>/world/playerdata`, and resolving\nthose UUIDs to a playername using Mojang's API.\n\n## Usage\n\n```\n$ python3 playerlist.py -h\nusage: playerlist.py [-h] [--out OUT] [--html] [-n N]\n                     [--servername SERVERNAME]\n                     worldpath\n\nGenerate a list of recent players on a minecraft server.\n\npositional arguments:\n  worldpath             Path to the world folder to scan (eg\n                        <server_root>/world)\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --out OUT             Path to output file, defaults to stdout\n  --html\n  -n N                  Only return the last n usernames, default all\n  --servername SERVERNAME\n                        Server name for use in output\n```\n\n## Example Output\n\n### Plain Text\n```console\n$ python3 playerlist.py  /opt/mc/world\nPlayers last seen on server\n=================================================\n1                Bob    Mon Oct 05 2020, 11:01 PM\n2                Dan    Mon Oct 05 2020, 10:28 PM\n3             George    Mon Oct 05 2020, 03:06 PM\n```\n\n### HTML\n\n`$ python3 playerlist.py  --html /opt/mc/world`\n```html\n<html>\n  <head>\n    <!-- generated with github.com/jaydenmilne/minecraft-server-player-list -->\n    <title>Big Daddy players</title>\n    <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n  </head>\n  <body>\n    <h1>Players on Big Daddy</h1>\n    <table>\n      <tr><th>Place</th><th>Player</th><th>Last Seen</th></tr>\n      <tr><td>1<td>Bob</td><td>Tue Oct 06 2020, 07:33 PM</td></tr>\n      <tr><td>2<td>Dan</td><td>Tue Oct 06 2020, 07:06 PM</td></tr>\n      <tr><td>3<td>George</td><td>Tue Oct 06 2020, 06:39 PM</td></tr>\n    </table>\n  </body>\n</html>\n```\n",
    'author': 'Jayden Milne',
    'author_email': 'jaydenmilne@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
