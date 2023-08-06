#!/usr/bin/python3

from http import HTTPStatus
import html
from typing import Optional, TextIO
import urllib.request as request
import argparse
import json
import glob
import os
import sys
import datetime
from typing import TypedDict, List, Dict, Tuple


class Player(TypedDict):
    uuid: str
    username: str
    last_looked_up: float
    last_modified_date: float


def get_last_modified_date(p: Player):
    return datetime.datetime.fromtimestamp(p["last_modified_date"]).strftime(
        "%a %b %d %Y, %I:%M %p"
    )


def is_bedrock_player(uuid: str) -> bool:
    return uuid.startswith("00000000-0000-0000-000")


def lookup_username(uuid: str) -> str:
    """Hit the mojang API to get the username for the given UUID"""
    if is_bedrock_player(uuid):
        return "(Bedrock/Geyser Player)"

    # perform request
    uuid_mangled = uuid.replace("-", "")
    r = request.Request(f"https://api.mojang.com/user/profile/{uuid_mangled}")

    try:
        resp = request.urlopen(r)
    except request.HTTPError as e:
        if e.status in [HTTPStatus.NOT_FOUND, HTTPStatus.NO_CONTENT]:
            print(f"Player `{uuid}` not found!")
            return uuid
        elif e.status == 429:
            print(f"we got rate limited :(")
            return uuid
        print(f"failed to look up uuid {uuid}")
        raise e

    body = json.load(resp)
    return body["name"]


def player_can_update(p: Player) -> bool:
    """Check if we can hit the mojang API for the given player.

    You can only look up a player once every minute."""
    last_looked_up_time = datetime.datetime.fromtimestamp(p["last_looked_up"])

    return (datetime.datetime.now() - last_looked_up_time).total_seconds() > 120


def get_max_player_name_length(players: List[Player]):
    return max(len(p["username"]) for p in players)


def get_player_uuids(worldpath: str) -> List[Tuple[str, float]]:
    """
    Returns a list of players, sorted from most recent to last
    """
    datfiles = glob.glob(f"{worldpath}/playerdata/*.dat")

    players: List[Tuple[str, float]] = []

    for datfile in datfiles:
        uuid = os.path.basename(datfile).replace(".dat", "")
        mtime = os.path.getmtime(datfile)
        players.append((uuid, mtime))

    players.sort(key=lambda x: x[1], reverse=True)
    return players


def write_text_output(out: TextIO, players: List[Player], servername: str):
    """
    Writes a textual representation of the output
    """
    header = f"Players last seen on {servername}"
    print(header, file=out)

    longest = get_max_player_name_length(players)

    max_row_len = 4 + longest + 4 + len("Mon Oct 05 2020, 02:33 PM")
    print("=" * max(len(header), max_row_len), file=out)

    count = 1
    for p in players:
        print(
            f"{{:<3}} {{:>{longest}}}    {{}}".format(
                count, p["username"], get_last_modified_date(p)
            ),
            file=out,
        )
        count += 1


def write_html_output(out: TextIO, players: List[Player], servername: str):
    """
    Writes a basic HTML representation of the output to stdout
    """
    header = f"<html><head><!-- generated with github.com/jaydenmilne/minecraft-server-player-list -->"
    header += f"<title>{servername} players</title><meta name='viewport' content='width=device-width, initial-scale=1.0'></head><body><h1>Players on {servername}</h1>"
    print(header, file=out)
    print("<table><tr><th>Place</th><th>Player</th><th>Last Seen</th></tr>", file=out)

    count = 1
    for p in players:
        print(
            f"<tr><td>{count}<td>{html.escape(p['username'])}</td><td>{get_last_modified_date(p)}</td></tr>",
            file=out,
        )
        count += 1

    print("</table></body></html>", file=out)


def read_cache(cache_path: str) -> Dict[str, Player]:
    if not os.path.isfile(cache_path):
        return {}

    with open(cache_path, "r") as c:
        try:
            cache: Dict[str, Player] = json.load(c)
        except json.JSONDecodeError as e:
            print(
                f"ERROR: failed to parse the cache at {cache_path}. You may need to delete that file and start over."
            )
            raise e

    assert isinstance(cache, dict)
    return cache


def write_cache(cache_path: str, cache: Dict[str, Player]):
    with open(cache_path, "w") as f:
        json.dump(cache, f)


def main(
    worldpath: str,
    out: Optional[str],
    cache_path: Optional[str],
    html: bool,
    n: int,
    servername: str,
):
    player_uuids = get_player_uuids(worldpath)

    if n != -1:
        player_uuids = player_uuids[: int(n)]

    players: List[Player] = []
    if cache_path is not None:
        cache = read_cache(cache_path)

        for uuid, mtime in player_uuids:
            if uuid not in cache or player_can_update(cache[uuid]):
                # look them up again and update the cache
                cache[uuid] = {
                    "uuid": uuid,
                    "username": lookup_username(uuid),
                    "last_looked_up": datetime.datetime.now().timestamp(),
                    "last_modified_date": mtime,
                }
            players.append(cache[uuid])

        # write out updated cache
        write_cache(cache_path, cache)
    else:
        # lookup all the players
        for uuid, mtime in player_uuids:
            players.append(
                {
                    "uuid": uuid,
                    "username": lookup_username(uuid),
                    "last_looked_up": datetime.datetime.now().timestamp(),
                    "last_modified_date": mtime,
                }
            )

    if out is None:
        f = sys.stdout
    else:
        f = open(out, "w")

    if html:
        write_html_output(f, players, servername)
    else:
        write_text_output(f, players, servername)


def entry():
    parser = argparse.ArgumentParser(
        description="Generate a list of recent players on a minecraft server."
    )

    parser.add_argument(
        "worldpath",
        type=str,
        help="Path to the world folder to scan (eg <server_root>/world)",
    )
    parser.add_argument(
        "--out",
        type=str,
        help="Path to output file, defaults to stdout",
        required=False,
        default=None,
    )
    parser.add_argument(
        "--cache-file",
        type=str,
        help="Path to cache file (created if not exists) to prevent rate limiting",
        required=False,
        default=None,
    )
    parser.add_argument(
        "--html",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "-n",
        required=False,
        help="Only return the last n usernames, default all",
        default=-1,
    )
    parser.add_argument(
        "--servername",
        required=False,
        help="Server name for use in output",
        default="server",
    )

    args = parser.parse_args()
    main(args.worldpath, args.out, args.cache_file, args.html, args.n, args.servername)


if __name__ == "__main__":
    entry()
