#!/usr/bin/env python
#-*- coding: utf-8 -*-

from .settings import Analysis_field, Analysis_field_mail
from .settings import to_top_data_field
import hashlib
import time

def _type_dict(data):
    content = []
    data_content = ""
    content_id = data.pop('id')
    content.append(content_id)
#    for value in data.values():
#        data_content += str(value) + " "
    content.append(data)
    return content


def data_type(data):
    if type(data) is dict:
        data_ = _type_dict(data)
    return data_


def remove_unused_fields(data):
    data = eval(data)
    unparsed = []
    for i,j in data.items():
        if j == "":
            data[i] = "NULL"
#    k = []
#    j = []
#    unparsed = []
#    data = data.replace("{","").replace("}","").split(",")
#    for i in data:
#        if len(i.split(":")) == 2:
#            k.append(i.split(":")[0].replace(" ",""))
#            j.append(i.split(":")[1].replace(" ",""))
#        elif len(i.split(":")) > 2:
#            k.append(i.split(":")[0].replace(" ",""))
##            j.append(':'.join(i.split(":")[1:]).replace(" ",""))
#            if i.split(":")[1][0] == " ":
#                b = i.split(":")[1].split(" ")
#                b.remove("")
#                b = " ".join(b)
#                j.append(b+':'+':'.join(i.split(":")[2:]))
#            else:
#                j.append(i.split(":")[1]+':'+':'.join(i.split(":")[2:]))
#        elif len(i.split(":")) < 2:
#            unparsed.append(i.split(":")[0].replace(" ",""))
##    print (dict(zip(k,j)), unparsed)
    return data, unparsed  
#    return dict(zip(k,j)), unparsed

def remove_unused_fields_mail(data):
    k = []
    j = []
    unparsed = []
    data = data.split("split_point")
    for i in data:
        if len(i.split(":")) == 2:
         #   k.append(i.split(":")[0].replace(" ",""))
         #   j.append(i.split(":")[1].replace(" ",""))
            k.append(i.split(":")[0].strip())
            if i.split(":")[1] == "":
                j.append("NULL")
            else:
                j.append(i.split(":")[1].strip())
            
        elif len(i.split(":")) > 2:
         #   k.append(i.split(":")[0].replace(" ",""))
            k.append(i.split(":")[0].strip())
#            j.append(':'.join(i.split(":")[1:]).replace(" ",""))
            if i.split(":")[1][0] == " ":
                b = i.split(":")[1].split(" ")
                b.remove("")
                b = " ".join(b)
                j.append(b+':'+':'.join(i.split(":")[2:]))
            else:
                j.append(i.split(":")[1]+':'+':'.join(i.split(":")[2:]))
        elif len(i.split(":")) < 2:
         #   unparsed.append(i.split(":")[0].replace(" ",""))
            unparsed.append(i.split(":")[0].strip())
#    print (dict(zip(k,j)), unparsed)

    return dict(zip(k,j)), unparsed

                                                               
def analysis_format_data(needed_pending_data):
    datas = []
    receive_info_ids = []
    if needed_pending_data is not None:
        for num in range(len(needed_pending_data)):
            if needed_pending_data[num][0] == 'api':
                has_been_analysis_data, unparsed = remove_unused_fields(needed_pending_data[num][1])
            elif needed_pending_data[num][0] == 'mail':
                has_been_analysis_data, unparsed = remove_unused_fields_mail(needed_pending_data[num][1])
            datas.append((has_been_analysis_data, unparsed))
            receive_info_ids.append(needed_pending_data[num][2])
    return datas, receive_info_ids


def datas_key_compare_if_exists(pre_data):        
#    print (pre_data)
    keyss = []
    filter_in = []
    filter_not = []
    for i in range(len(pre_data)):
        if len(pre_data[i]) == 2:
            keys = []
            filter_data_in_field = {}
            filter_data_not_in_field = {}
            for key,value in pre_data[i][0].items():
                if key in Analysis_field:
                    keys.append(Analysis_field[key])
                    filter_data_in_field.update({Analysis_field[key]: value})
#                    print (str(Analysis_field[key])+str(keys)+str(filter_data_in_field)+"\n")
                else:
                    try:
                        filter_data_not_in_field.update({Analysis_field[key]: value})
                    except:
                        pass

            filter_data_in_field = datas_if_not_to_None(keys, filter_data_in_field)
            keyss.append(keys) 
            filter_in.append(filter_data_in_field)
            filter_not.append(filter_data_not_in_field)
    return keyss, filter_in, filter_not


def datas_key_compare_if_exists_mail(pre_data):
    keyss = []
    filter_in = []
    filter_not = []
    filter_data_in_field = {}
    filter_data_not_in_field = {}
    for i in range(len(pre_data)):
        if len(pre_data[i]) == 2:
            keys = []
            for key,value in pre_data[i][0].items():
                if key in Analysis_field:
                    keys.append(Analysis_field[key])
                    filter_data_in_field.update({Analysis_field[key]: value})
                else:
                    try:
                        filter_data_not_in_field.update({Analysis_field[key]: value})
                    except:
                        pass

            filter_data_in_field = datas_if_not_to_None(keys, filter_data_in_field)
            keyss.append(keys)
            filter_in.append(filter_data_in_field)
            filter_not.append(filter_data_not_in_field)
    return keyss, filter_in, filter_not


def datas_if_not_to_None(keys, filter_data_in_field):
#    num = 0
    for key in Analysis_field.keys():
        if Analysis_field[key] not in keys:
#            print (str(Analysis_field[key])+str(keys)) 
            filter_data_in_field.update({Analysis_field[key]: None})
#        num += 1
#        print (str(num)+"\n")
    return filter_data_in_field



def mail_data_deal_forCustSystemCode(mail):
    customer_name, monitor_name, monitor_version = None, None, None
    mail_content = None
    if 'content' in mail:
        mail_content = mail['content']
    elif 'body' in mail:
        mail_content = mail['body']
    if '\r\n' in mail_content:
        mail_content = mail_content.split('\r\n')
        for i in range(len(mail_content)):

            if len(mail_content[i]) > 0:

                mail_content_ = mail_content[i].split(":")

                if mail_content_[0] == '客户名称':
                    customer_name =  mail_content_[1]
                elif mail_content_[0] == '监控系统名称':
                    monitor_name = mail_content_[1]
#                elif mail_content_[0] == '监控系统版本':
#                    monitor_version = mail_content_[1]

#        mail_content = mail_content.split('\r\n')
#        for i in range(len(mail_content)):
#
#            if len(mail_content[i]) > 0:
#
#                mail_content_ = mail_content[i].split("：")
#
#                if mail_content_[0] == '设备类型':
#                    customer_name =  mail_content_[1]
#                elif mail_content_[0] == '监控方式':
#                    monitor_name = mail_content_[1]
    elif '\n\n' in mail_content:
        mail_content = mail_content.split('\n\n')
        for i in range(len(mail_content)):

            if len(mail_content[i]) > 0:

                mail_content_ = mail_content[i].split(":")

                if mail_content_[0] == '客户名称':
                    customer_name =  mail_content_[1]
                elif mail_content_[0] == '监控系统名称':
                    monitor_name = mail_content_[1]
    else:
        mail_content = mail_content.split('\n')
        for i in range(len(mail_content)):

            if len(mail_content[i]) > 0:

                mail_content_ = mail_content[i].split(":")

                if mail_content_[0] == '客户名称':
                    customer_name =  mail_content_[1]
                elif mail_content_[0] == '监控系统名称':
                    monitor_name = mail_content_[1]
#                elif mail_content_[0] == '监控系统版本':
#                    monitor_version = mail_content_[1]
#    else:
#
#        mail_content = mail_content.split('\n')
#        for i in range(len(mail_content)):
#
#            if len(mail_content[i]) > 0:
#
#                mail_content_ = mail_content[i].split("：")
#
#                if mail_content_[0] == '设备类型':
#                    customer_name =  mail_content_[1]
#                elif mail_content_[0] == '监控方式':
#                    monitor_name = mail_content_[1]
#             
#    print ("111111111111111111 %s,%s" % (customer_name, monitor_name))
#    return customer_name, monitor_name, monitor_version
    return customer_name, monitor_name
    
    
def send_top_data_dict(data):
    data_dict = {}
    data_dict.update({"infoId": data[0]})
    data_dict.update({"customerCode": data[2]})
    data_dict.update({"customerName": data[32]})
    data_dict.update({"monitorCode": data[3]})
    data_dict.update({"monitorName": data[34]})
    data_dict.update({"monitorVersion": data[4]})
    data_dict.update({"identityCode": data[5]})
    data_dict.update({"kpiAssortment": data[6]})
    data_dict.update({"kpiName": data[7]})
    data_dict.update({"kpiValue": data[8]})
    data_dict.update({"alertContent": data[9]})
    data_dict.update({"ip": data[10]})
    data_dict.update({"alertTime": data[11]})
    data_dict.update({"serviceObject": data[12]})
    data_dict.update({"serviceName": data[13]})
    data_dict.update({"factoryName": data[14]})
    data_dict.update({"modelName": data[15]})
    data_dict.update({"sn": "0720BD2159"})   #data[16] 
    data_dict.update({"city": data[17]})
    data_dict.update({"businessSystem": data[18]})
    data_dict.update({"maDept": data[19]})
    data_dict.update({"maUser": data[20]})
    data_dict.update({"maMobile": data[21]})
    data_dict.update({"maEmail": data[22]})
    data_dict.update({"autoCreateFlg": 0})   #data[23] 
    data_dict.update({"inServiceFlg": data[25]})
    data_dict.update({"dealStatus": data[26]})
    return data_dict



def deal_data_ready_top(data_dict):
#    data_dict = {}
    data_dict_ = {}
#    key_ = data[2]+"itsMonitorMd5key"
    clientSubmitTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) 
    key_ = "clientSubmitTime="+clientSubmitTime+"itsMonitorMd5key"
#    print (key_)
    secret = hashlib.md5()
    secret.update(key_.encode(encoding="utf-8"))
    data_dict_.update({"data": data_dict})
    data_dict_.update({"key": secret.hexdigest()})
    data_dict_.update({"clientSubmitTime": clientSubmitTime})
#    print (secret.hexdigest())
    return data_dict_


def reply_data_ready_top(datas):
    json = {}
    data = []
    clientSubmitTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    key_ = "clientSubmitTime="+clientSubmitTime+"itsMonitorMd5key"
#    print (key_)
    secret = hashlib.md5()
    secret.update(key_.encode(encoding="utf-8"))
    for d in datas:
        data.append({"infoId": d[0]})
    json.update({"data": data})
    json.update({"key": secret.hexdigest()}) 
    json.update({"clientSubmitTime": clientSubmitTime})
    return json
