# SCP-079-PM - Everyone can have their own Telegram private chat bot
# Copyright (C) 2019 SCP-079 <https://scp-079.org>
#
# This file is part of SCP-079-PM.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import pickle
from os import mkdir
from os.path import exists
from shutil import rmtree
from typing import List, Dict, Set, Tuple, Union
from configparser import RawConfigParser

# Enable logging
logger = logging.getLogger(__name__)

# Init
all_commands: List[str] = [
    "block",
    "ping",
    "recall",
    "start",
    "unblock",
    "version"
]
version = "0.2.1"

# Load data from pickle

# Init dir
try:
    rmtree("tmp")
except Exception as e:
    logger.info(f"Remove tmp error: {e}")

for path in ["data", "tmp"]:
    if not exists(path):
        mkdir(path)

# Init ids variables
blacklist_ids: Set[int] = set()
flood_ids: Dict[str, Union[Dict[int, int], set]] = {
    "users": set(),
    "counts": {}
}
message_ids: Dict[int, Dict[str, Set[int]]] = {}
reply_ids: Dict[str, Dict[int, Tuple[int, int]]] = {
    "g2h": {},
    "h2g": {}
}

# Load ids data
file_list: List[str] = ["blacklist_ids", "message_ids", "reply_ids"]
for file in file_list:
    try:
        try:
            if exists(f"data/{file}") or exists(f"data/.{file}"):
                with open(f"data/{file}", 'rb') as f:
                    locals()[f"{file}"] = pickle.load(f)
            else:
                with open(f"data/{file}", 'wb') as f:
                    pickle.dump(eval(f"{file}"), f)
        except Exception as e:
            logger.error(f"Load data {file} error: {e}")
            with open(f"data/.{file}", 'rb') as f:
                locals()[f"{file}"] = pickle.load(f)
    except Exception as e:
        logger.critical(f"Load data {file}_words backup error: {e}")
        raise SystemExit("[DATA CORRUPTION]")

# Read data from config.ini

# [basic]
bot_token: str = ""
prefix: List[str] = []
prefix_str: str = "/!！"

# [channels]
test_group_id: int = 0

# [custom]
host_id: int = 0

try:
    config = RawConfigParser()
    config.read("config.ini")
    # [basic]
    bot_token = config["basic"].get("bot_token", bot_token)
    prefix = list(config["basic"].get("prefix", prefix_str))
    # [channels]
    test_group_id = int(config["channels"].get("test_group_id", test_group_id))
    # [custom]
    host_id = int(config["custom"].get("host_id"), host_id)
except Exception as e:
    logger.warning(f"Read data from config.ini error: {e}")

# Check
if (bot_token in {"", "[DATA EXPUNGED"}
        or prefix == []
        or test_group_id == 0
        or host_id == 0):
    logger.critical("No proper settings")
    raise SystemExit('No proper settings')

# Start program
copyright_text = (f"SCP-079-PM v{version}, Copyright (C) 2019 SCP-079 <https://scp-079.org>\n"
                  "Licensed under the terms of the GNU General Public License v3 or later (GPLv3+)\n")
print(copyright_text)
