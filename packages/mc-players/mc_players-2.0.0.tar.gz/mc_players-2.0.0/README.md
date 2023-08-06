# Minecraft Server Player List

Quick script that generates a list of recent players on your server, sorted
in order of who last logged in. Works by looking at the last modified time of
their `player.dat` files in `<server root>/world/playerdata`, and resolving
those UUIDs to a playername using Mojang's API.

## Usage

```
$ python3 playerlist.py -h
usage: playerlist.py [-h] [--out OUT] [--html] [-n N]
                     [--servername SERVERNAME]
                     worldpath

Generate a list of recent players on a minecraft server.

positional arguments:
  worldpath             Path to the world folder to scan (eg
                        <server_root>/world)

optional arguments:
  -h, --help            show this help message and exit
  --out OUT             Path to output file, defaults to stdout
  --html
  -n N                  Only return the last n usernames, default all
  --servername SERVERNAME
                        Server name for use in output
```

## Example Output

### Plain Text
```console
$ python3 playerlist.py  /opt/mc/world
Players last seen on server
=================================================
1                Bob    Mon Oct 05 2020, 11:01 PM
2                Dan    Mon Oct 05 2020, 10:28 PM
3             George    Mon Oct 05 2020, 03:06 PM
```

### HTML

`$ python3 playerlist.py  --html /opt/mc/world`
```html
<html>
  <head>
    <!-- generated with github.com/jaydenmilne/minecraft-server-player-list -->
    <title>Big Daddy players</title>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
  </head>
  <body>
    <h1>Players on Big Daddy</h1>
    <table>
      <tr><th>Place</th><th>Player</th><th>Last Seen</th></tr>
      <tr><td>1<td>Bob</td><td>Tue Oct 06 2020, 07:33 PM</td></tr>
      <tr><td>2<td>Dan</td><td>Tue Oct 06 2020, 07:06 PM</td></tr>
      <tr><td>3<td>George</td><td>Tue Oct 06 2020, 06:39 PM</td></tr>
    </table>
  </body>
</html>
```
