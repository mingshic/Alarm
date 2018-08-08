#!/usr/bin/python
import time

import sys
from settings import json_initialization, appid, appkey
from url import url
import requests

sys.path.append('..')
from app.model.execute_command import command_ready


def MailProcessor():
    req_data = json_initialization(appid, appkey)
    json = req_data.json

    connectdb = command_ready()
    try:
        last_uids = connectdb.select_raw_mail_uid('mail')
    except:
        last_uids = []

    if len(last_uids) != 0:
        mail_data_filter = []
        universalID = last_uids[0][-1]
        json['id'] = universalID
        req = eval(requests.post(url, json=json).text)
#        print (req)
        if int(req['code']) == 200:
            mail_data = req['data'] 
            return mail_data
    
    else:
        req = eval(requests.post(url, json=json).text)
        if int(req['code']) == 200:
            mail_data = req['data']
          #  for i in range(len(mail_data)):
          #      if "customer_name_测试" in str(mail_data[i]['body'].split(':')):
          #          print ("\n", mail_data[i])

            return mail_data       

            
