import urllib.request as urlreq
import threading
import json

from .api import api as API
from .handler import Handler
from .config import config
from .events import event_types

class Worker(threading.Thread):
    def __init__(self, func, args = None):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
    def run(self):
        try:
            self.func(self.args)
        except Exception as er:
            return 0

class Longpoll:
    def __init__(self, token = None, v = "5.95", api = API):
        self.token = token
        self.api_v = v
        if self.token is None:
            raise RuntimeError("You must past token into settings")

        config['access_token'] = self.token
        config['api_version'] = self.api_v

        self.api = api

        self.group = self.api("groups.getById")[0]
        self.lp_server_data = None
        self.lp_server = "{}?act=a_check&key={}&ts={}&wait=25"

        self.is_polling = None

        # other
        self.handler = Handler()
        self.command = self.handler.command
        self.event = self.handler.event


    def get_longpoll_data(self):
        longpoll = self.api("groups.getLongPollServer", group_id = self.group['id'])

        self.lp_server_data = {
            **longpoll
        }

    def receiver(self):
        if not self.lp_server_data:
            self.get_longpoll_data()

        try:
            with urlreq.urlopen(
                self.lp_server.format(
                    self.lp_server_data['server'],
                    self.lp_server_data['key'],
                    self.lp_server_data['ts']
                )
            ) as res:
                response = json.loads(res.read())
        except Exception:
            return ()

        if 'error' in response:
            self.get_longpoll_data()

        if 'ts' in response:
            self.lp_server_data['ts'] = response['ts']

        return response['updates']

    def main(self, none):
        try:
            while True:
                if not self.is_polling:
                    break
                for update in self.receiver():
                    if update['type'] in event_types:
                        worker = Worker(self.handler._update_handler(update), self.handler._msg_parser(update['object']))
                        worker.start()
        except KeyboardInterrupt:
            self.is_polling = False

    def startPolling(self):
        self.is_polling = True
        worker = Worker(self.main)
        worker.start()

    def stopPolling(self):
        self.is_polling = False

