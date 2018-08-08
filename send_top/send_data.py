#!/usr/local/python35/bin/python3
#-*- coding: utf-8 -*-


import sys
import time

sys.path.append('..')

from url import url
from app.model.execute_command import command_ready
from app.model.settings import Tables
from app.model.data_processing import deal_data_ready_top, send_top_data_dict 
from app.models import db

from top_replystatus import TopReplyStatus 
from match_operation import DoubleMatchedRow

import requests



def update_anlysis_after_deal_status(info_id, deal_status):
    connectdb = command_ready()
    connectdb.update_anlysis_after_deal_status(info_id, deal_status)
    
def update_anlysis_before_deal_status(info_id, deal_status):
    connectdb = command_ready()
    connectdb.update_anlysis_before_deal_status(info_id, deal_status)

def update_matched_corresponding_rule(info_id, deal_status):
    connectdb = command_ready()
    connectdb.update_matched_corresponding_rule(info_id, deal_status)

def create_rule_table():
    connectdb = command_ready()
    connectdb.create_rule_table()
    connectdb.operation_close()

 
class send_data:
    def _send_data_to_top(self, url, data_dict):
        data = deal_data_ready_top(data_dict)
        r = requests.post(url, json=data)
        print (r.text)
        return r.text
        
    def _process(self):
        self.connectdb = command_ready()
        req_pending_data = self.connectdb.select_union_raw_custsystem("1")

        datas = req_pending_data
         
        return datas

    def _deal_status(self, statu):
        update_anlysis_after_deal_status(statu["infoId"], statu["dealStatus"])
        update_matched_corresponding_rule(statu["infoId"], statu["dealStatus"]) 


    def start(self, period=30):
        while True:
            req_status = TopReplyStatus()

            store_MatchedAndMatchedRow = DoubleMatchedRow()
            status = req_status.query_ready()
            if status is not None and status["message"] == "OK" and len(status["receiveData"]) != 0:
                for statu in status["receiveData"]:
                    alfilter_statu = req_status.statusFilter(statu) 
                    if alfilter_statu is not None:
                        
                        self._deal_status(alfilter_statu)
##########                    
###########告警至top
            datas = self._process()   
            for i in range(len(datas)):

                data_dict = send_top_data_dict(datas[i])

                matched = store_MatchedAndMatchedRow._ifrule(data_dict)
                if len(matched) != 0: 
                    data_dict["autoCreateFlg"] = 1

                    response = eval(self._send_data_to_top(url, data_dict))

                    if int(response["isReceiveFlg"]) == 1 and int(response["isCreateFlg"]) == 0:
                        update_anlysis_before_deal_status(datas[i][0], "6")
                        update_matched_corresponding_rule(datas[i][0], "6")
                    elif int(response["isReceiveFlg"]) == 1 and int(response["isCreateFlg"]) == 1:
                        update_anlysis_after_deal_status(datas[i][0], "2")
                        update_matched_corresponding_rule(datas[i][0], "2")
                    else:
                        continue

                else:
                    data_dict["autoCreateFlg"] = 0
                    response = eval(self._send_data_to_top(url, data_dict)) 
                    
                    if int(response["isReceiveFlg"]) == 1 and int(response["isCreateFlg"]) == 0:
                        update_anlysis_before_deal_status(datas[i][0], "6")
                        update_matched_corresponding_rule(datas[i][0], "6")
 

            time.sleep(period)
            
            

def main():
    if True:
        send_to = send_data()
    else:
        exit(1)
    
    send_to.start(15)


if __name__ == '__main__':
    create_rule_table()
    main()
 
