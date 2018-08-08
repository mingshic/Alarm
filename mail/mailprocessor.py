#!/usr/bin/python
import time

import sys
from pop3mail import POP3MailServer

sys.path.append('..')
from app.model.execute_command import command_ready
from app.model.settings import POP3





class MailProcessor:
    def __init__(self):#, num=0):
        self.mail_location = 0



    def __iter__(self):

        self.connectdb = command_ready()
        try:
            self.last_uids = self.connectdb.select_raw_mail_uid('mail')
        except:
            self.last_uids = []

#        print (type(self.last_uids), self.last_uids)

        try:
            self.pop3 = POP3MailServer(POP3['server'],POP3['user'],POP3['password']) 
            self.ready = True
        except:
            self.ready = False

        print (self.ready)
        if self.ready == True and len(self.last_uids) != 0:
            for i in range(len(self.last_uids)):
                try:
                    self.mail_location = self.pop3.pegging_count(self.last_uids[i][0])
                    print (self.mail_location)
                    break 
                except:
                    pass
        else:
            self.mail_location = 0         
        
        print ("19191991191919199191 %s, %s" % (self.mail_location, self.pop3.total()))
#        time.sleep(30)
        return self

    def __next__(self):
        if self.ready:
            if self.mail_location < self.pop3.total():
                self.mail_location += 1
                try:
                    mail = self.pop3.mail(self.mail_location)
                    uid = self.pop3.uid(self.mail_location)
                    mail['id_'] = uid
                    return mail
                except:
                    raise StopIteration() 
            else:
                raise StopIteration()
#                    pass
                #    mail = None

        

