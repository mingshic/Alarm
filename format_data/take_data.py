#!/usr/local/python35/bin/python3
#-*- coding: utf-8 -*-

import sys
import time
import logging

sys.path.append('..')

from app.model.execute_command import command_ready
from app.model.settings import Tables, Mail_newField
from app.model.data_processing import analysis_format_data, datas_key_compare_if_exists 
#from app.model.execute_command import insert_analysis_data

logging.basicConfig(level=logging.DEBUG,
                    format='levelname:%(levelname)s filename: %(filename)s '
                           'outputNumber: [%(lineno)d]  thread: %(threadName)s output msg:  %(message)s'
                           ' - %(asctime)s', datefmt='[%d/%b/%Y %H:%M:%S]',
                    filename='./format_raw_data.log')



def analysis_if_success_todb(receive_info_id, analysis_flg):
    connectdb = command_ready()
    connectdb.update_raw_alarm(receive_info_id, analysis_flg)
    

def create_format_table():
    connectdb = command_ready()
    connectdb.create_analysis_table()
    connectdb.operation_close()

class Analysis_data:
#    def __init__(self):
#        self.connectdb = command_ready()
        
    def _process(self):
        self.connectdb = command_ready()
        req_pending_data = self.connectdb.select_raw_alarm(Tables['receive_table'], 0)

        self.connectdb.operation_close()
        
        processed_data, receive_info_ids = analysis_format_data(req_pending_data)
            

        deal_data = [] 
        receive_info_idss = []
        str_ = ""       

        for num in range(len(processed_data)):
#            print ("11111111111111", processed_data[num])

            if Mail_newField['customer_code'] and Mail_newField['monitor_code'] not in processed_data[num][0]:
                connectdb = command_ready()
                customer_system_code, customer_code, monitor_code, active_flg = connectdb.select_cust_systemCode_by_name(processed_data[num][0][Mail_newField['customer_name']],processed_data[num][0][Mail_newField['monitor_name']])        
                print (customer_system_code, customer_code, monitor_code, active_flg)
                processed_data[num][0].update({Mail_newField['customer_code']: customer_code})
                processed_data[num][0].update({Mail_newField['monitor_code']: monitor_code})

            _str = processed_data[num][1]
            for i in range(len(_str)):
                str_ += _str[i]
#len(processed_data[num][1]) != 0
            if len(processed_data[num]) == 2 and len(str_) != 0:
                analysis_if_success_todb(receive_info_ids[num], 2)  #2表示解析失败
                logging.warn(processed_data[num][0])
            else:
                deal_data.append(processed_data[num])
                receive_info_idss.append(receive_info_ids[num])

        keys, filter_data_in_field, filter_data_not_in_field = datas_key_compare_if_exists(deal_data)
        return keys, filter_data_in_field, receive_info_idss


    def _time_ex(self, time_stamp):
        strf_time = time_stamp
        try:
            #print ("wwwwwwwwwwwwwwwwww", time_stamp[-3:])
            if time_stamp[-3:] == "000":
                time_stamp = time_stamp[:-3]
                time_strf = time.localtime(int(time_stamp))
                strf_time = time.strftime("%Y-%m-%d %H:%M:%S", time_strf)
                return strf_time
            if time_stamp == "None" or time_stamp == "NULL":
                time_strf = time.localtime(int(time.time()))
                strf_time = time.strftime("%Y-%m-%d %H:%M:%S", time_strf)
                return strf_time
            else:
                time_strf = time.strptime(time_stamp, '%Y-%m-%d%H:%M')
                strf_time = time.strftime("%Y-%m-%d %H:%M:%S", time_strf)
                return strf_time
            
        except:
            pass
        return strf_time


    def start(self, period=30):
        while True:
            keys, datas, receive_info_idss = self._process()
            for i in range(len(datas)):            
                #print ("qqqqqqqqqqqqqqqqqq", datas[i])
                datas[i]["alert_time"] = self._time_ex(str(datas[i]["alert_time"]))
                #print (datas[i])
                self.connectdb = command_ready()
                self.connectdb.insert_analysis_data(datas[i],receive_info_idss[i])   
                self.connectdb.operation_close() 
                logging.info(datas[i])
                analysis_if_success_todb(receive_info_idss[i], 1)      

            time.sleep(period)

            
            

def main():
    if True:
        analysis = Analysis_data()
    else:
        exit(1)
    
    analysis.start(10)


if __name__ == '__main__':
    create_format_table()
    main()
 
