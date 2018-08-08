import os, datetime
import sys
from flask import Flask, jsonify, abort, request, make_response
import json
import urllib.request
import simplejson
from werkzeug.security import check_password_hash
import pickle

import logging

from app.api import api
from ..models import Customer, db 

from ..model.execute_command import command_ready
from ..model.settings import Pickle_table


logging.basicConfig(level=logging.DEBUG, 
                    format='levelname:%(levelname)s filename: %(filename)s '
                           'outputNumber: [%(lineno)d]  thread: %(threadName)s output msg:  %(message)s'
                           ' - %(asctime)s', datefmt='[%d/%b/%Y %H:%M:%S]',
                    filename='./logAPI.log')
 

def operation(data,sys_id,asys_id,asys_key):
    auth = Customer.query.filter(Customer.access_system_id==asys_id).first()
    try:
        pass_hash = auth.access_system_key
    except:
        return make_response(jsonify({"code": 0, "data": "Error, may be key not in DB, please contact the administrator"}), 400)    
    if check_password_hash(pass_hash,asys_key) is True:
        if data != '':
            raw_alarm = data
            source_type = "api"
            receive_type = "2"
            connectdb = command_ready()
            if len(raw_alarm) == 4:
                raw_alarm = raw_alarm["data"]
            customer_system_code, active_flg = connectdb.select_cust_systemCode(raw_alarm["客户code"],raw_alarm["监控系统code"],raw_alarm["监控系统版本"])
            if int(active_flg) == 1:
                connectdb = command_ready()
                connectdb.insert_raw_alarm(customer_system_code, raw_alarm, source_type, receive_type)
            else:
                return make_response(jsonify({"code": 0,"data": "The sent user system code is not activated"}), 400)
            return jsonify({"code": 1,"data": "success"})
        else:
            return make_response(jsonify({"code": 0,"data": "Request no data"}), 400)
    else:
        return make_response(jsonify({"code": 0, "data": "Authentication failure"}), 400)


@api.route("/api/alarm", methods=['GET', 'POST'])
def alarm():
    if request.method == 'POST':
        data = request.data
        
        IP = request.remote_addr
        data = json.loads(data.decode('utf8'))
        try:
            if 'data' and 'system_id' and 'access_system_id' and 'access_system_key' in list(data.keys()):
                rep_retu = operation(data['data'],data['system_id'],data['access_system_id'],data['access_system_key'])
                return rep_retu
            else:
                return make_response(jsonify({"code": 0, "data": "The key 'data,system_id,access_system_id,access_system_key' may be incorrect, please check your 'data,system_id,access_system_id,access_system_key' field"}), 400)
        except:
            return make_response(jsonify({"code": 0, "data": "The key 'data,system_id,access_system_id,access_system_key' may be incorrect, please check your 'data,system_id,access_system_id,access_system_key' field"}), 400)


    if request.method == 'GET':
        if len(list(request.args.items())) == 4 and request.args.get('data') != None and request.args.get('system_id') != None and request.args.get('access_system_id') != None and request.args.get('access_system_key') != None:
            data = request.args.get('data')
            system_id = request.args.get('system_id')
            access_system_id = request.args.get('access_system_id')
            access_system_key = request.args.get('access_system_key')
            rep_retu = operation(data,system_id,access_system_id,access_system_key)
            return rep_retu
        else:
            return jsonify({"code": 0,"data": "error"})

