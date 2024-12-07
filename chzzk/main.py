from chzzk import Chat
from chzzk_top20 import Top

import requests
import json
import asyncio
import websockets
import pandas as pd

from datetime import datetime
from pytz import timezone

top_list = Top().bjid_list
sockets = []
tasks = []

for name, bjid in top_list.items():
    socket = Chat(bjid)
    sockets.append(socket)
    tasks.append(asyncio.ensure_future(socket.connect()))

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
loop.close()

print(sockets[0].chatting)

    