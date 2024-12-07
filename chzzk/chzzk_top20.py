import requests
import json
import asyncio
import websockets
import pandas as pd

from fake_useragent import UserAgent
import ssl

from datetime import datetime
from pytz import timezone

class Top():
    def __init__(self):
        ssl._create_default_https_context = ssl._create_unverified_context

        user_agent = UserAgent()
        self.headers = {'User-Agent': user_agent.random} #requests 로 get 요청 때 user-Agent 오류 떠서 해결하기 위함. 

        self.bjid_list = {} #csv로 만들기 위한 보관함 딕셔너리
        self.getAPIURL = "https://api.chzzk.naver.com/service/v1/lives" #현재 방송중인 방송국 중 가장 인기 있는 방송국 20개 출력 api
        self.params = {
            'size':20,
            'sortType':'POPULAR'
        }
        self.session = requests.session()
        self.getTop()
        
    def getTop(self):
        tops = self.session.get(url=self.getAPIURL, headers=self.headers, params=self.params).json()['content']['data']
        for top in tops:
            channel = top['channel']
            self.bjid_list[channel['channelName']] = channel['channelId']