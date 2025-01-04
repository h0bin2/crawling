from chzzk import Chat
from chzzk_top20 import Top

from itertools import chain
from collections import defaultdict

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
    socket.nickname = name
    sockets.append(socket)
    tasks.append(asyncio.ensure_future(socket.connect()))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.wait(tasks))
    except KeyboardInterrupt:
        print("종료")
    finally:
        print("저장 중")
        df = pd.DataFrame()
        for socket in sockets:
            new = pd.DataFrame.from_dict(socket.chatting, orient='columns')
            df = pd.concat([df, new])
            

        print(df['host'].unique())
        df.to_csv(f'crawling/chzzk/data/{datetime.now(timezone("Asia/Seoul")).strftime("%Y-%m-%d_%H:%M:%S")}_chzzk.csv', index=False)

    