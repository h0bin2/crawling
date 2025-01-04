import requests
import json
import asyncio
import websockets
import pandas as pd

from datetime import datetime
from pytz import timezone
    

class Chzzk():
    def __init__(self, bjid):

        self.bjid = bjid
        
        self.session = requests.session()
        self.channelId = ""
        self.nickname = ""
        
        self.accessToken = ""
        self.extraToken = ""

        self.nowTime = datetime.now(timezone('Asia/Seoul'))

    def getChannelInfo(self):
        try:
            url = f'https://api.chzzk.naver.com/polling/v3/channels/{self.bjid}/live-status'
            self.channelId = self.session.get(url=url).json()['content']['chatChannelId']
            if self.channelId is None:
                raise Exception
            print(f'channelId : {self.channelId}')
        except:
            print(f"{self.bjid} : channelId not found(getChannelInfo)")

    def getToken(self):
        try:
            url = f'https://comm-api.game.naver.com/nng_main/v1/chats/access-token?channelId={self.channelId}&chatType=STREAMING'
            token = self.session.get(url=url).json()['content']

            self.accessToken = token['accessToken']
            self.extraToken = token['extraToken']

        except:
            print(f'{self.bjid} : Token not found(getToken)')


class Chat(Chzzk):
    def __init__(self, bjid):
        self.socketUrl = 'wss://kr-ss1.chat.naver.com/chat'
        self.chatting = {'host':[], 'channelId':[], 'nickname':[], 'msg':[], 'time':[]}

        super().__init__(bjid)
        super().getChannelInfo()
        super().getToken()

        self.reqData = {
            'bdy':{
                'accTkn':self.accessToken,
                'auth':'READ',
            },
            'cid':self.channelId,
            'cmd':100,
            'svcid':'game',
            'tid':1,
            'ver':'3'
        }

    async def connect(self):
        async with websockets.connect(self.socketUrl, ping_interval=60) as websocket:
            await websocket.send(json.dumps(self.reqData))
            #(datetime.now(timezone('Asia/Seoul')) - self.nowTime).seconds < 3600:
            if self.channelId is None:
                return

            while (datetime.now(timezone('Asia/Seoul')) - self.nowTime).seconds < 60:
                now = datetime.now(timezone('Asia/Seoul'))

                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=60.0)
                except asyncio.TimeoutError:
                    print(f"{self.bjid} timeout")
                    break

                response = json.loads(response)

                if response['cmd'] == 0:
                    await websocket.send(json.dumps({'ver':"3", 'cmd':10000}))
                    print(f"{self.channelId}", end=' / ')
                    continue

                if response['cmd'] == 93101:
                    for res in response['bdy']:
                        msg = res['msg']
                        nickname = json.loads(res['profile'])['nickname']
                        strNow = now.strftime('%Y-%m-%d_%H:%M:%S')
                        self.chatting['host'].append(self.nickname)
                        self.chatting['channelId'].append(self.channelId)
                        self.chatting['nickname'].append(nickname)
                        self.chatting['msg'].append(msg)
                        self.chatting['time'].append(strNow)
                        # self.chatting.append([self.nickname, self.channelId, nickname, msg, strNow])
                        print(f'{self.nickname}[{self.channelId}]에서 {nickname}님께서 {msg}라고 말했다. {strNow}')
                        # print(self.channelId + ' : ' + nickname + ' : ' + msg + ' - ' + now.strftime('%Y-%m-%d_%H:%M:%S'))
                
                if response is None:
                    print(f"{self.channelId} 방송 종료됨.")
                    break

# liveId = [
#     '75cbf189b3bb8f9f687d2aca0d0a382b',
#     '45e71a76e949e16a34764deb962f9d9f',
#     '2eee29ce69664154d8bc478825941259',
#     '17aa057a8248b53affe30512a91481f5'
# ]

# now = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d_%H:%M:%S')

# objects = []
# tasks = []
# # for live in liveId:
# #     go = Chat(live)
# #     objects.append(go)
# #     tasks.append(asyncio.ensure_future(go.connect()))

# # loop = asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))
# # print(objects[0].chatting)