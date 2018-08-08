#!/usr/bin/env /usr/local/python35/bin/python3

# -*- coding: utf8 -*-
import time
import sys
from mailprocessor import MailProcessor

sys.path.append('..')

from app.model.execute_command import command_ready
from app.model.data_processing import mail_data_deal_forCustSystemCode


class Mail_raw:
    def _process(self, mail):
         
        try:
            customer_name, monitor_name = mail_data_deal_forCustSystemCode(mail)
           # print (customer_name, monitor_name)
            self.connectdb = command_ready()
            customer_system_code, customer_code, monitor_code, active_flg = self.connectdb.select_cust_systemCode_by_name(customer_name, monitor_name) 
#            print ("1111111111111111111111" * 10, customer_system_code, customer_code, monitor_code, active_flg, "\n")
        
        except:
            customer_system_code, customer_code, monitor_code, active_flg = None, None, None, 0
#            print (customer_system_code, customer_code, monitor_code, active_flg)
        

        return customer_system_code, customer_code, monitor_code, active_flg

    def start(self, period = 30):
        while True:
            mail_data = MailProcessor()      
            for mail in mail_data[::-1]:  
                customer_system_code, customer_code, monitor_code, active_flg = self._process(mail)
##                print (customer_system_code, mail) 
##                print (customer_system_code, active_flg)
#   
                if int(active_flg) == 1:
#                
                    self.connectdb = command_ready()
                    self.connectdb.insert_raw_mail_data(customer_system_code, mail, 'mail', 1) 
#                else:
#                    
#                    
#       
            time.sleep(period)
#

def main():
    
    if True:  
        mail_raw = Mail_raw()
    else: 
        exit(1)

    mail_raw.start(30)

if __name__ == '__main__':
    
    main()


