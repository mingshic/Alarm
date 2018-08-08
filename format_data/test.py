#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import time
sys.path.append("..")

from model.execute_command import command_ready
from model.settings import Tables
from model.data_processing import analysis_format_data, datas_key_compare_if_exists 

import logging

import multiprocessing as mp
import threading
import time
import queue

queue_ = queue.Queue()

logging.basicConfig(level=logging.DEBUG,
                    format='levelname:%(levelname)s filename: %(filename)s '
                           'outputNumber: [%(lineno)d]  thread: %(threadName)s output msg:  %(message)s'
                           ' - %(asctime)s', datefmt='[%d/%b/%Y %H:%M:%S]',
                    filename='./format_raw_data.log')

def operation_store_queue():
    global queue_
    connectdb = command_ready()
    position_num, req_pending_data = connectdb.select_raw_alarm(Tables['receive_table'], 0)
    connectdb.operation_close()

    processed_data, receive_info_ids = analysis_format_data(req_pending_data)

    deal_data = []
    receive_info_idss = []

    for num in range(len(processed_data)):
        if len(processed_data[num]) == 2 and len(processed_data[num][1]) != 0:
            analysis_if_success_todb(receive_info_ids[num], 2)  #2表示解析失>败
            logging.warn(processed_data[num][0])
        else:
            deal_data.append(processed_data[num])
            receive_info_idss.append(receive_info_ids[num])

    keys, filter_data_in_field, filter_data_not_in_field = datas_key_compare_if_exists(deal_data)

    for i in range(len(filter_data_in_field)):
        queue_.put((filter_data_in_field[i], receive_info_idss[i]))


def analysis_if_success_todb(receive_info_id, analysis_flg):
    connectdb = command_ready()
    connectdb.update_raw_alarm(receive_info_id, analysis_flg)
    

def create_format_table():
    connectdb = command_ready()
    connectdb.create_analysis_table()
    connectdb.operation_close()


class Analysis_data(threading.Thread):
#class Analysis_data(mp.Process):
    def run(self):
        global queue_
        while queue_.qsize() > 0:
            data = queue_.get()
            self.connectdb = command_ready()
            self.connectdb.insert_analysis_data(data[0],data[1])
            self.connectdb.operation_close()
            analysis_if_success_todb(data[1], 1)
            logging.info(data[0])
            time.sleep(4)

def main():
    operation_store_queue()
    for i in range(100):
        c = Analysis_data()
        c.start()


if __name__ == '__main__':
    create_format_table()
    main()
 
