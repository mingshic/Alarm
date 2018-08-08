#!/usr/bin/env python3
#-*- coding: utf8 -*-

import datetime
from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from .model.settings import Tables

class Customer(UserMixin,db.Model):
    __tablename__ = 'customer_access_use'
    id = db.Column(db.Integer(), primary_key=True)
    system_id = db.Column(db.String(20))
    access_system_id = db.Column(db.String(80))
    access_system_key = db.Column(db.String(100))

    __table_args__ = {
        "mysql_charset": "utf8"
    }

    def __repr__(self):
        return '%r,%r,%r' % (self.system_id,self.access_system_id,self.access_system_key)


#class CustomerSystemTable(db.Model):
    
#class AlarmRawData(db.Model):
#    __tablename__ = Tables['receive_table']
#    receive_info_id = db.Column(db.Integer(), primary_key=True)
#    uuid = db.Column(db.String(1000)) 
#    source_type = db.Column(db.String(50))
#    cust_system_code = db.Column(db.String(100))
#    receive_type = db.Column(db.String(30))
#    receive_time = 

class RawAnalysisData(db.Model):
    __tablename__ = Tables['format_table']
    info_id = db.Column(db.Integer(), primary_key=True)
    receive_info_id = db.Column(db.String(100))
    customer_code = db.Column(db.String(1000))
    monitor_code = db.Column(db.String(100))
    monitor_version = db.Column(db.String(100))
    identity_code = db.Column(db.String(100))
    kpi_assortment = db.Column(db.String(100))
    kpi_name = db.Column(db.String(100))
    kpi_value = db.Column(db.String(100))
    alert_content = db.Column(db.Text)
    ip = db.Column(db.String(100))
    alert_time = db.Column(db.String(100))
    service_object = db.Column(db.String(100))
    service_name = db.Column(db.String(100))
    factory_name = db.Column(db.String(100))
    model_name = db.Column(db.String(100))
    sn = db.Column(db.String(100))
    city = db.Column(db.String(100))
    business_system = db.Column(db.String(100))
    ma_dept = db.Column(db.String(100))
    ma_user = db.Column(db.String(100))
    ma_mobile = db.Column(db.String(100))
    ma_email = db.Column(db.String(100))
    analysised_time = db.Column(db.String(100))
    auto_create_flg = db.Column(db.String(100))
    in_service_flg = db.Column(db.String(100))
    deal_status = db.Column(db.String(100))
    create_on = db.Column(db.DateTime, default=datetime.datetime.now())
    modified_on = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())

    __table_args__ = {
        "mysql_charset": "utf8"
    }

    def __repr__(self):

        return '%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r' % (self.receive_info_id,self.customer_code,self.monitor_code,self.monitor_version,self.identity_code,self.kpi_assortment,self.kpi_name,self.kpi_value,self.alert_content,self.ip,self.alert_time,self.service_object,self.service_name,self.factory_name,self.model_name,self.sn,self.city,self.business_system,self.ma_dept,self.ma_user,self.ma_mobile,self.ma_email,self.analysised_time,self.auto_create_flg,self.in_service_flg,self.deal_status,self.create_on,self.modified_on)

class UserCorrespondingRule(db.Model):
    __tablename__ = 'customer_alert_rule'
    rule_id = db.Column(db.Integer(), primary_key=True)
    cust_system_code = db.Column(db.String(100))
    rule_name = db.Column(db.String(100))
    kpi_criterionalert = db.Column(db.Text)
    active_flg = db.Column(db.Integer())
    created_by = db.Column(db.String(100))
    created_on = db.Column(db.DateTime, default=datetime.datetime.now())
    modified_by = db.Column(db.String(100))
    modified_on = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())

    __table_args__ = {
        "mysql_charset": "utf8"
    }

    def __repr__(self):
        return '%r,%r,%r,%r' % (self.cust_system_code,self.rule_name,self.kpi_criterionalert,self.active_flg)



class MatchedRule(db.Model):
    __tablename__ = 'case_matched_rule'
    id = db.Column(db.Integer(), primary_key=True)    
    info_id = db.Column(db.Integer())
    rule_name = db.Column(db.String(100))
    rule_matched = db.Column(db.Text)
    created_on = db.Column(db.DateTime, default=datetime.datetime.now())

    __table_args__ = {
        "mysql_charset": "utf8"
    }
    
    def __repr__(self):
        return '%r,%r,%r' % (self.info_id,self.rule_name,self.rule_matched)
