#!/usr/bin/python

import sys
import time
import hashlib
import requests

sys.path.append('..')

from url import reply_url
from app.model.execute_command import command_ready
from app.model.data_processing import reply_data_ready_top


class TopReplyStatus:

    def _query_status_to_top(self, reply_url, json):
        r = requests.post(reply_url, json=json)
        return r.text


    def _process(self):
        self.connectdb = command_ready()
        req_pending_data = self.connectdb.select_union_raw_custsystem("6")

        datas = req_pending_data

        return datas

    def query_ready(self):
        
        response = None
        datas = self._process()
 
        json = reply_data_ready_top(datas)

        response = eval(self._query_status_to_top(reply_url, json)) if len(json["data"]) != 0 else response

        return response

    def statusFilter(self, statu):
        if statu["dealStatus"] == "1" or "2":
            #return statu
            pass
        else:
            return statu

    
