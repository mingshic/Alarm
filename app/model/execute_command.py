#-*- coding: utf-8 -*-
#!/usr/bin/env python
import sys
import hashlib
import time
import datetime

from .settings import Tables, Pickle_table
from .model import MysqlDB
from .sql import create_raw_table_sql, create_analysis_table_sql, create_customer_system_table_sql, create_rule_table_sql,  create_case_matched_table_sql

import pickle

#sys.path.append("../..")
#from app.models import RawAnalysisData, db
#from app import create_app
#
#app=create_app()
#app.app_content().push()

def data_format_deal(data):
    try:
        if "'" in data:
            data = data.replace("'",'"')
    except:
        pass
    return data

def data_format_deal_mail(data):
    try:
        if "\r\n" in data:
            data = data.replace("\r\n","split_point")
        elif '\n' in data:
            data = data.replace('\n',"split_point")
        if " " in data:
            data = data.replace(" ","")
    except:
        pass
    return data


class command_ready(MysqlDB):
    def __init__(self):
        super(command_ready,self).__init__()
        self.conn = self.connection
    

    def operation_close(self):
        self.conn.connection.commit()
        self.conn.connection.close()

    def create_raw_table(self):
        self.conn.execute(create_raw_table_sql)


    def create_rule_table(self):
        self.conn.execute(create_rule_table_sql)
        self.conn.execute(create_case_matched_table_sql)

    def create_analysis_table(self):
        self.conn.execute(create_analysis_table_sql)

    def create_customer_system_table(self): 
        self.conn.execute(create_customer_system_table_sql)


    def insert_customer_system(self, cust_system_code, customer_code, customer_name, monitor_code, monitor_name, monitor_version, active_flg):
        sql = '''insert into %s (cust_system_code,customer_code,customer_name,monitor_code,monitor_name,monitor_version,active_flg) value ('%s','%s','%s','%s','%s','%s','%s')''' % (Tables["customer_system_table"],cust_system_code,customer_code,customer_name,monitor_code,monitor_name,monitor_version,active_flg)
        conn = self.conn
        conn.execute(sql)
        conn.connection.commit()
        conn.connection.close()

    def update_customer_system(self, cust_system_code, customer_code, monitor_code, monitor_version, active_flg):
        sql = '''update %s set active_flg='%s' where cust_system_code='%s' and customer_code='%s' and monitor_code='%s' and monitor_version='%s' ''' % (Tables["customer_system_table"],active_flg,cust_system_code,customer_code,monitor_code,monitor_version) 
        conn = self.conn
        conn.execute(sql)
        conn.connection.commit()
        conn.connection.close()

    def insert_rule(self, data, policySet):
        policy_matched = str(policySet['rule_matched'])
        data_content = str(data[1]['alarm_title'])+str(data[1]['alarm_level'])+str(data[1]['processer'])+str(data[1]['instance'])+str(data[1]['service_name'])+str(data[1]['alarm_content'])
        data_format_deal(policy_matched)
        data_format_deal(data_content)
        
        sql = '''insert into rule_recotb (rule_id,rule_matched,suggest_operate_case,alarm_content,SN,top_response) values ('%s','%s','%s','%s','%s','%s')''' % (data[1]['rule_id'],policy_matched,policySet['建议'],data_content,data[1]['SN'],data[2]['top_response'])     

#        sql = '''insert into test (a) values ('%s')''' % (data['alarm_content'])
        conn = self.conn
        conn.execute(sql)
        conn.connection.commit()
        conn.connection.close()
        

    def insert_raw_alarm(self, customer_system_code, data, source_type, receive_type):
        data = data_format_deal(str(data))
        try:
            uuid = hashlib.md5()
            uuid.update(bytes(str(time.time()),encoding='utf-8'))
            uuid = uuid.hexdigest()
        except:
            uuid = 'failed'
        sql = '''insert into %s (uuid,source_type,cust_system_code,receive_type,receive_content,analysis_flg) values ('%s','%s','%s','%s','%s','%s')''' % (Tables["receive_table"],uuid,source_type,customer_system_code,receive_type,data,"0")                
        conn = self.conn
        conn.execute(sql)
        conn.connection.commit()
        conn.connection.close()


    def update_raw_alarm(self, receive_info_id, analysis_flg):
        sql = '''update %s set analysis_flg='%s' where receive_info_id='%s' ''' % (Tables["receive_table"],analysis_flg,receive_info_id)
        conn = self.conn
        conn.execute(sql)
        conn.connection.commit()
        conn.connection.close()

    def insert_analysis_data(self, data, receive_info_id):
        deal_time = datetime.datetime.now()
        sql = '''insert into %s (receive_info_id,customer_code,monitor_code,monitor_version,identity_code,kpi_assortment,kpi_name,kpi_value,alert_content,alert_time,ip,service_object,service_name,factory_name,model_name,sn,city,business_system,ma_dept,ma_user,ma_mobile,ma_email,analysised_time,deal_status) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')''' % (Tables["format_table"],receive_info_id,data["customer_code"],data["monitor_code"],data["monitor_version"],data["identity_code"],data["kpi_assortment"],data["kpi_name"],data["kpi_value"],data["alert_content"],data["alert_time"],data["ip"],data["service_object"],data["service_name"],data["factory_name"],data["model_name"],data["sn"],data["city"],data["business_system"],data["ma_dept"],data["ma_user"],data["ma_mobile"],data["ma_email"],deal_time,"1")
        self.conn.execute(sql)


    def update_anlysis_after_deal_status(self, info_id, deal_status):
        sql = '''update %s set deal_status='%s' where info_id='%s' ''' % (Tables["format_table"],deal_status,info_id)
        conn = self.conn
        conn.execute(sql)
        conn.connection.commit()
        conn.connection.close()

    def update_anlysis_before_deal_status(self, info_id, deal_status):
        sql = '''update %s set deal_status='%s' where info_id='%s' ''' % (Tables["format_table"],deal_status,info_id)
        conn = self.conn
        conn.execute(sql)
        conn.connection.commit()
        conn.connection.close()


    def select_raw_alarm(self, pending_table, analysis_flg):
        sql = '''select source_type,receive_content,receive_info_id from %s where analysis_flg='%s' ''' % (pending_table,analysis_flg)
        nums = self.conn.execute(sql)
        penging_data = self.conn.fetchall()
        return penging_data
        

    def select_cust_systemCode(self, customer_code, monitor_code, monitor_version):
        sql = '''select %s,%s from %s where customer_code='%s' and monitor_code='%s' and monitor_version='%s' ''' % ("cust_system_code","active_flg",Tables["customer_system_table"],customer_code,monitor_code,monitor_version)
        conn = self.conn
        nums = conn.execute(sql)
        customer_system_code, active_flg = conn.fetchone()
        conn.connection.commit()
        conn.connection.close()
        return customer_system_code, active_flg      


    def select_cust_systemCode_by_name(self, customer_name, monitor_name):
        sql = '''select %s,%s,%s,%s from %s where customer_name='%s' and monitor_name='%s' ''' % ("cust_system_code","customer_code","monitor_code","active_flg",Tables["customer_system_table"],customer_name,monitor_name)
        conn = self.conn
        nums = conn.execute(sql)
        customer_system_code, customer_code, monitor_code, active_flg = conn.fetchone()
        conn.connection.commit()
        conn.connection.close()
        return (customer_system_code,customer_code,monitor_code,active_flg)



    def select_union_raw_custsystem(self, deal_status):
        sql = '''select * from %s, %s where %s.%s=%s.%s and %s.%s=%s.%s and %s.%s=%s.%s and %s.%s='%s' ''' % (Tables["format_table"],Tables["customer_system_table"],Tables["format_table"],"customer_code",Tables["customer_system_table"],"customer_code",Tables["format_table"],"monitor_code",Tables["customer_system_table"],"monitor_code",Tables["format_table"],"monitor_version",Tables["customer_system_table"],"monitor_version",Tables["format_table"],"deal_status",deal_status)
        conn = self.conn
        conn.execute(sql)
        penging_data = conn.fetchall()
        conn.connection.commit()
        conn.connection.close()
        return penging_data


#    def storeFile(self,datadb):
#        A = []
#        B = []
#        sql = '''select * from %s''' % (datadb) 
#        conn = self.conn
#        nums = conn.execute(sql)
#        conn.scroll(0,mode='absolute')
#        results = conn.fetchall()
#        for num in range(nums):
#            A.append(results[num][2])    
#            B.append(results[num][3]) 
#        A_B = dict(zip(A,B))
#        f = open("app/"+Pickle_table['export_pickle'],'wb')
#        pickle.dump(A_B,f)
#        f.close()  
#        conn.connection.commit()
#        conn.connection.close() 




###################################
#mail sql
    def select_raw_mail_uid(self, source_type):
        sql = '''select uuid from %s where source_type='%s' order by receive_info_id desc limit 1 ''' % (Tables['receive_table'],source_type)
        conn = self.conn
        conn.execute(sql)
        uuid_data = conn.fetchall()
        conn.connection.commit()
        conn.connection.close()
        return uuid_data

    def insert_raw_mail_data(self, customer_system_code, mail_data, source_type, receive_type):
        if 'content' in mail_data:
            mail_content = data_format_deal_mail(str(mail_data['content']))
            mail_content = data_format_deal(mail_content)
            sql = '''insert into %s (uuid,source_type,cust_system_code,receive_type,receive_content,analysis_flg) values ('%s','%s','%s','%s','%s','%s')''' % (Tables["receive_table"],mail_data['id_'].decode("utf-8"),source_type,customer_system_code,receive_type,mail_content,"0")    
            conn = self.conn
            conn.execute(sql)
            conn.connection.commit()
            conn.connection.close()

        if 'body' in mail_data:
            mail_content = data_format_deal_mail(str(mail_data['body']))
            mail_content = data_format_deal(mail_content)
            sql = '''insert into %s (uuid,source_type,cust_system_code,receive_type,receive_content,analysis_flg) values ('%s','%s','%s','%s','%s','%s')''' % (Tables["receive_table"],mail_data['universalID'],source_type,customer_system_code,receive_type,mail_content,"0")
            conn = self.conn
            conn.execute(sql)
            conn.connection.commit()
            conn.connection.close()


#def insert_analysis_data(data, receive_info_id):
#    deal_time = datetime.datetime.now()
#    raw_analysis = RawAnalysisData(receive_info_id=receive_info_id,customer_code=data["customer_code"],monitor_code=data["monitor_code"],monitor_version=data["monitor_version"],identity_code=data["identity_code"],kpi_assortment=data["kpi_assortment"],kpi_name=data["kpi_name"],kpi_value=data["kpi_value"],alert_content=data["alert_content"],alert_time=data["alert_time"],ip=data["ip"],service_object=data["service_object"],service_name=data["service_name"],factory_name=data["factory_name"],model_name=data["model_name"],sn=data["sn"],city=data["city"],business_system=data["business_system"],ma_dept=data["ma_dept"],ma_user=data["ma_user"],ma_mobile=data["ma_mobile"],ma_email=data["ma_email"],analysised_time=deal_time,deal_status="1")
#    db.session.add(raw_analysis)
#    db.session.close()



#################################
#rule relate table operation
    def select_cust_corresponding_rule(self, cust_system_code):
        sql = '''select rule_name,kpi_criterionalert,active_flg from %s where cust_system_code='%s' ''' % (Tables["customer_alert_rule"],cust_system_code)
        self.conn.execute(sql)
        rule_data = self.conn.fetchall()        
        return rule_data        
   
    def select_default_corresponding_rule(self, cust_system_code):
        sql = '''select rule_name,kpi_criterionalert,active_flg from %s where cust_system_code='%s' ''' % (Tables["customer_alert_rule"],cust_system_code)
        self.conn.execute(sql)
        rule_data = self.conn.fetchall()
        return rule_data

    def insert_cust_corresponding_rule(self, data, cust_system_code):
        sql = '''insert into %s (cust_system_code,rule_name,kpi_criterionalert,active_flg,create_by,modified_by) value ('%s','%s','%s','%s','%s','%s')''' % (Tables["customer_alert_rule"],cust_system_code,cust_system_code+"_rule",data,"1","system","system")
        conn = self.conn
        conn.execute(sql)
        conn.connection.commit()
        conn.connection.close()

    def update_cust_corresponding_rule(self, data, cust_system_code):
        sql = '''update %s set kpi_criterionalert='%s' where cust_system_code='%s' ''' % (Tables["customer_alert_rule"],data,cust_system_code) 
        conn = self.conn
        conn.execute(sql)
        conn.connection.commit()
        conn.connection.close()

    def select_rule_matched(self, rule_name):
        sql = '''select info_id,rule_matched from %s where rule_name='%s' ''' % (Tables["case_matched_rule"],rule_name)
        self.conn.execute(sql)
        matched_data = self.conn.fetchall()
        return matched_data

    def insert_matched_corresponding_rule(self, data):
        sql = '''insert into %s (info_id,rule_name,rule_matched,kpis_and_content,deal_status,same_rule) value ('%s','%s','%s','%s','%s',"%s")''' % (Tables["case_matched_rule"],data["info_id"],data["rule_name"],data["rule_matched"],data["kpis_and_content"],data["deal_status"],data["same_rule"])
        conn = self.conn
        conn.execute(sql)
        conn.connection.commit()
        conn.connection.close()

    def update_matched_corresponding_rule(self, info_id, deal_status):
        sql = '''update %s set deal_status='%s' where info_id='%s' ''' % (Tables["case_matched_rule"],deal_status,info_id)
        conn = self.conn
        conn.execute(sql)
        conn.connection.commit()
        conn.connection.close()
    
#    def update_cust_corresponding_rule(self, rule_name):
#        sql = '''update %s set ='%s' where cust_system_code='%s' ''' % (Tables["customer_alert_rule"],cust_system_code)
#        conn = self.conn
#        conn.execute(sql)
#        conn.connection.commit()
#        conn.connection.close()
