#!/usr/bin/python

import threading
import time
from multiprocessing import Queue
import multiprocessing as mp
import requests
#from test_data import data
import random

customer_info = [["C3383","神州","its","ITS","1.1"],["customer_code_测试","customer_name_测试","monitor_code_测试","monitor_name_测试","monitor_version_测试"]]
# ["test_2", "test_name_2", "test_monitor_2", "test_monitor_name_2", "test_monitor_name_version_2"], ["test_3", "test_name_3", "test_monitor_3", "test_monitor_name_3", "test_monitor_name_version_3"]]


def choise(info):
    json = { "data1": {
            "客户code": info[0][0],
            "客户名称": info[0][1],
            "监控系统code": info[0][2],
            "监控系统名称": info[0][3],
            "监控系统版本": info[0][4],
            "KPI分类": "例如: firewall_cisco， IBM存储……",
            "KPI名称": "例如：CPU使用率， 系统宕机，SGA引导区大小……",
            "KPI值": "例如：99%， Tomcat is down，",
            "告警内容描述": "eth5网卡出流量为297484，超过40000，请关注.",
            "告警发生时间": "2018-05-11 11:11:13",
            "IP": "172.19.100.83",
            "服务对象": "crm2csb1",
            "服务名": "44348e04dcaf410890af4efb0b76e10a",
            "厂商": "SUN",
            "型号": "V440",
            "序列号": "0720BD2159",
            "所在城市": "浙江省/杭州市",
            "业务系统": "ESB、CSB多平台业务系统",
            "维护部门": "运维部",
            "维护人员": "张三",
            "维护人员手机": "12938457001",
            "维护人员邮箱": "zhangsan@customer.com",
            },
            "data2": {
            "客户code": info[0][0],
            "客户名称": info[0][1],
            "监控系统code": info[0][2],
            "监控系统名称": info[0][3],
            "监控系统版本": info[0][4],
            "KPI分类": "例如: firewall_cisco， IBM存储……",
            "KPI名称": "例如：CPU使用率， 系统宕机，SGA引导区大小……",
            "KPI值": "例如：99%， Tomcat is down，",
            "告警内容描述": "eth5网卡出流量为297484,超过40000,请关注.",
            "告警发生时间": "2018-05-11 11:11:13",
            "IP": "172.19.100.83",
            "服务对象": "crm2csb1",
            "服务名": "44348e04dcaf410890af4efb0b76e10a",
            "厂商": "SUN",
            "型号": "V440",
            "序列号": "0720BD2159",
            "所在城市": "浙江省/杭州市",
            "业务系统": "ESB、CSB多平台业务系统",
            "维护部门": "运维部",
            "维护人员": "张三",
            "维护人员手机": "12938457001",
            "维护人员邮箱": "zhangsan@customer.com",
            }
    }
    return json    


def write_que_info(data):
#    for i in range(1000000):
    with open("10","a") as wp:
        wp.write(str(data)+"\n")


def readFile():
    file_object = open('10')
    global queue
    for line in file_object:
        queue.put(line)


class Consumer(mp.Process):
#class Consumer(threading.Thread):
    def run(self):
        global queue
        while queue.qsize() > 0:
            q = queue.get()
            r = requests.post("http://172.16.1.14:5000/api/alarm", json={"data": eval(q), "system_id": "alarm_to_top_system", "access_system_id": "its_smart", "access_system_key": "shpQJR2ACLg7uYBS"})
            print (self.name + '消费了 '+ eval(q)["客户code"] + str(r.text))
            time.sleep(4)


queue = Queue()
def main():
    readFile()
    for i in range(100):
#        info = random.sample(customer_info,1)
#        choise_json = choise(info) 
#        info1 = random.sample(choise_json.keys(),1)
#        data = choise_json[info1[0]]
#        write_que_info(data) 
        c = Consumer()        
        c.start()


if __name__ == "__main__":
    main()
