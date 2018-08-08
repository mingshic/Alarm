#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
sys.path.append('..')

from app.model.execute_command import command_ready

def select_CustCorrespondingRrule(customer_system_code):
    connectdb = command_ready()
    rule_data = connectdb.select_cust_corresponding_rule(customer_system_code)
    return rule_data

def select_DefaultCorrespondingRrule(customer_system_code):
    connectdb = command_ready()
    rule_data = connectdb.select_cust_corresponding_rule(customer_system_code)
    return rule_data

def insert_CustCorrespondingRule(matched_data, customer_system_code):
    connectdb = command_ready()
    insert_matched = connectdb.insert_cust_corresponding_rule(matched_data,customer_system_code)
    return insert_matched

def update_CustCorrespondingRule(matched_data, customer_system_code):
    connectdb = command_ready()
    update_match = connectdb.update_cust_corresponding_rule(matched_data,customer_system_code)
    return update_match

def insert_MatchedCorrespondingRule(data):
    connectdb = command_ready()
    matched_record = connectdb.insert_matched_corresponding_rule(data)
    return  matched_record


class DoubleMatchedRow:

    def _deal_rule(self, rule_data, data_dict):
        matched = []
       
        try:
            if rule_data[0][2] == "1":
                for rule_key in rule_data[0][1].split(";"):
                    if rule_key in str(data_dict["kpiAssortment"]+";"+data_dict["kpiName"]+";"+data_dict["kpiValue"]+";"+data_dict["alertContent"]):    
                        matched.append(rule_key)
                return ";".join(matched)
            elif rule_data[1] == 0:
                pass
        except:
            pass


    def _ifdataFilterRule(self, rule_data, matched):
        try:
            if rule_data[0][1] and len(rule_data[0][1]) != 0:
                filter_rule = []

                matched = matched.split(";")
                rule_data = rule_data[0][1].split(";")

                for m in range(len(matched)):
                    if matched[m].strip() in rule_data:
                        continue
                    filter_rule.append(matched[m]) 
                if len(";".join(filter_rule)) == 0:
                    return "zero"
                return ";".join(filter_rule)
            else:
                rule_data = None
                return rule_data
        except:
            pass


    def _ifMatchedFilterRule(self, matched, matched_default):
        matched = matched.split(";")
        matched_default = matched_default.split(";")
        same = list(set(matched)&set(matched_default))
        diff = list(set(matched)^set(matched_default))
        if same and diff:
            return ";".join(diff), {1: {"cust": ";".join(matched), "default": ";".join(matched_default), "same": ";".join(same)}}     # 1 说明有交集
       
        if len(same) == 0 and diff:
            return ";".join(matched), {0: {"cust": ";".join(matched), "default": ";".join(matched_default), "same": ";".join(same)}}     # 0 说明无交集
                
        if len(diff) == 0 and same:
            return ";".join(same), {2: {"cust": ";".join(matched), "default": ";".join(matched_default), "same": ";".join(same)}}     # 说明可用可信取


    def _ifmatched(self, data_dict, matched, customer_system_code, same=None):
        data = {}

        rule_data = select_CustCorrespondingRrule(customer_system_code)

        data["info_id"] = data_dict["infoId"]
        data["rule_name"] = rule_data[0][0]
        data["rule_matched"] = matched
        data["kpis_and_content"] = data_dict["kpiAssortment"] + "=&=" + data_dict["kpiName"] + "=&=" + data_dict["kpiValue"] + "=&=" + data_dict["alertContent"]
        data["deal_status"] = data_dict["dealStatus"]
        data["same_rule"] = same

        insert_MatchedCorrespondingRule(data)
        

    def _ifrule(self, data_dict):
        connectdb = command_ready()

        customer_system_code, active_flg = connectdb.select_cust_systemCode(data_dict["customerCode"],data_dict["monitorCode"],data_dict["monitorVersion"])        

        rule_data = select_CustCorrespondingRrule(customer_system_code)
        rule_data_default = select_DefaultCorrespondingRrule("default")
###############################rule_data 和 matched 的过滤中 怎么通过 rule_data 和 data_dict的规则对应提炼出新的规则   以便于规则递增加入
########
#以 $$ 标记那些地方需要递增规则添加
#########
        matched = self._deal_rule(rule_data, data_dict)
        matched_default = self._deal_rule(rule_data_default, data_dict)

        if len(rule_data) == 0:
            if (matched == None or matched == "") and matched_default != None and matched_default != "":
                insert_CustCorrespondingRule(matched_default, customer_system_code)
                self._ifmatched(data_dict, matched_default, customer_system_code)

                return matched_default

            elif matched == None or matched == "" and matched_default == "" or matched_default == None:
                insert_CustCorrespondingRule("", customer_system_code)
                self._ifmatched(data_dict, matched, customer_system_code) 
                return ""
             

        else:
            if matched != None and matched != "" and (matched_default == "" or matched_default == None):
                self._ifmatched(data_dict, matched, customer_system_code)
                return matched
 
            elif matched != None and matched != "" and matched_default != None and matched_default != "":
                filter_, same_intersection = self._ifMatchedFilterRule(matched, matched_default) 
     
                filter_matched = ";".join(list(set((rule_data[0][1]+";"+filter_).split(";"))))
                update_CustCorrespondingRule(filter_matched, customer_system_code)
                self._ifmatched(data_dict, matched, customer_system_code, str(same_intersection))
               
                
                return filter_
                                 
#############该处是 客户规则中没有被匹配上的规则,为空,在默认规则中匹配上了,这一点导致默认匹配上的规则直接向该客户的规则递增添加了.
            elif matched == "" and matched_default != None and matched_default != "":
                matched = ""
                if len(rule_data[0][1]) == 0:
                    matched_ = ";".join(list(set((matched_default).split(";"))))
                else:
                    matched_ = ";".join(list(set((rule_data[0][1]+";"+matched_default).split(";"))))
                update_CustCorrespondingRule(matched_, customer_system_code)
                self._ifmatched(data_dict, matched_default, customer_system_code) 
                return matched_default

            elif matched == "" and (matched_default == None or matched_default == ""):
                self._ifmatched(data_dict, matched_default, customer_system_code)
                return ""





