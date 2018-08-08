#!/usr/bin/env python


import os


class Mysqlconfig():

    ENV = 'Mysqlconfig'
    DEBUG = True

    # session
    CSRF_ENABLED = True
    SECRET_KEY = "asgSfsf3Xd8ffy]fw8vfd0zbvssqwertsd4sdwe"

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # datebase
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://alarm:123456@localhost/alarm?charset=utf8"
#    SQLALCHEMY_ECHO = True



POP3 = {
    'server': 'pop3.sina.com',
    'user': 'm15210521936@sina.com',
    'password': 'msc920521'
}

Mysql_parameter = {
    "HOST": "localhost",
    "PORT": 3306,
    "USER": "alarm",
    "PASSWD": "123456",
    "DB": "alarm",
    "CHARSET": "utf8",
} 

Databases = {
    "Database": "alarm",
}

Tables = {
    "rule_table": "rule_recotb",
    "receive_table": "alarm_raw_data",
    "access_use": "customer_access_use",
    "customer_system_table": "customer_system",
    "format_table": "raw_analysis_data", 
    "customer_alert_rule": "customer_alert_rule",
    "case_matched_rule": "case_matched_rule",
}

Pickle_table = {
    "export_pickle": "accessUse.pkl",
}


#Analysis_field = ["kpi_name", "factory_name", "alert_content", "alert_time", "monitor_name", "service_name", "customer_code", "business_system", "sn", "model_name", "ma_user", "ma_dept", "customer_name", "ip", "city", "kpi_assortment", "ma_email", "monitor_version", "monitor_code", "service_object", "ma_mobile", "kpi_value"]
#Analysis_field = ["customer_code","monitor_code","monitor_version","identity_code","kpi_assortment","kpi_name","kpi_value","alert_content","alert_time","ip","service_object","service_name","factory_name","model_name","sn","city","business_system","ma_dept","ma_user","ma_mobile","ma_email"]
#Analysis_field = {"customer_code": "客户code","monitor_code": "监控系>统code","monitor_version": "监控系统版本","identity_code": "identity_code","kpi_assortment": "kpi分类","kpi_name": "kpi名称","kpi_value": "kpi值","alert_content": "告警内容描述","alert_time": "告警发生时间","ip": "IP","service_object": "服务对象","service_name": "服务名","factory_name": "厂商","model_name": "型号","sn": "序列号","city": "所在城市","business_system": "业务系统","ma_dept": "维护部门","ma_user": "维护人员","ma_mobile": "维护人员手机","ma_email": "维护人员邮箱"}

Analysis_field = {'服务对象': 'service_object', '维护人员': 'ma_user', '型号': 'model_name', '告警内容描述': 'alert_content', '维护人员手机': 'ma_mobile', '监控系统版本': 'monitor_version', 'KPI名称': 'kpi_name', '告警发生时间': 'alert_time', '客户code': 'customer_code', '服务名': 'service_name', 'KPI分类': 'kpi_assortment', '监控系统code': 'monitor_code', '所在城市': 'city', '业务系统': 'business_system', 'identity_code': 'identity_code', '维护部门': 'ma_dept', 'KPI值': 'kpi_value', '序列号': 'sn', '厂商': 'factory_name', 'IP': 'ip', '维护人员邮箱': 'ma_email'}


Mail_newField = {'customer_code': '客户code', 'monitor_code': '监控系统code', 'customer_name': '客户名称', 'monitor_name': '监控系统名称'}


Analysis_field_mail = ['客户名称', '监控系统名称', '监控系统版本', 'KPI名称', 'KPI值', '告警内容描述', 'IP', '机器名/设备名/数据库名', '服务名', '厂商', '型号', '序列号', '业务系统', '维护部门', '维护人员', '维护人员手机', '维护人员邮箱']


to_top_data_field = ["info_id","receive_info_id","customer_code","monitor_code","monitor_version","identity_code","kpi_assortment","kpi_name","kpi_value","alert_content","ip","alert_time","service_object","service_name","factory_name","model_name","sn","city","business_system","ma_dept","ma_user","ma_mobile","ma_email","analysised_time","auto_create_flg","in_service_flg","deal_status","create_on","modified_on","id","cust_system_code","customer_code","customer_name","monitor_code","monitor_name","monitor_version","address","parameter","remark","active_flg","create_by","create_on","modified_by","modified_on"]

#customer_code
#customer_name
#monitor_code
#monitor_name
#monitor_version
#kpi_assortment
#kpi_name
#kpi_value
#alert_content
#alert_time
#ip
#service_object
#service_name
#factory_name
#model_name
#sn
#city
#business_system
#ma_dept
#ma_user
#ma_mobile
#ma_email
#
#


#info_id										
#receive_info_id	
#
#customer_code,monitor_code,monitor_version,identity_code,kpi_assortment,kpi_name,kpi_value,alert_content,alert_time,ip,service_object,service_name,factory_name,model_name,sn,city,business_system,ma_dept,ma_user,ma_mobile,ma_email
#
#analysised_time
#auto_create_flg
#in_service_flg
#deal_status
#created_on
#modified_on										
#
