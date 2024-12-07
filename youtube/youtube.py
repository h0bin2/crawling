import pytchat
import datetime
import pandas as pd

class Youtube():
    def __init__(self, url):
        self.url = url
        self.id = self.__getID__()

    def __getID__(self):
        id = self.url.split("?")[-1].split("=")[-1]
        return id

class Chat(Youtube):
    def __init__(self, url):
        super().__init__(url)
        self.chat = pytchat.create(video_id=self.id)

    def connect(self):
        while self.chat.is_alive():
            for c in self.chat.get().sync_items():
                print(f"{c.datetime} [{c.author.name}]- {c.message}")

live = "https://www.youtube.com/watch?v=5bD0y6bVVas"
yt = Chat(live)
yt.connect()