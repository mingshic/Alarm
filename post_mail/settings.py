# -*- coding: utf8 -*-


import hashlib
from datetime import datetime

appid = "dcitsMonitor"
appkey="52023eec8ad5516bab1c6bd2992be660"


class json_initialization:
    def __init__(self, appid, appkey):
        self.appid = appid       
        self.appkey = appkey

    @property
    def json(self):
        self.accesstime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.key = self.appkey+self.accesstime

        hash = hashlib.md5()
        hash.update(bytes(self.key ,encoding='utf-8'))

        self.appsecret = hash.hexdigest().upper()


        MAIL_REQUESTS = {
            'appid': self.appid,
            'accesstime': self.accesstime,
            'appsecret': self.appsecret,
            'id': ""
        }

        return MAIL_REQUESTS
