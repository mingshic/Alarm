#!/usr/bin/python
#-*- coding: utf-8 -*-

import email
from email.header import decode_header
import poplib
from settings import POP3
import time


class POP3MailServer:
    def __init__(self, server, user, password):
        self.pop3 = poplib.POP3(server)
        self.pop3.user(user)
        self.pop3.pass_(password)
    

    def uid(self, which):
        uid = self.pop3.uidl(which).split()[2]
        return uid

    def decode_str(self, s):
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        return value


    @property
    def uids(self):
        idl = self.pop3.uidl()
     #   uidl = [id.split()[2] for id in idl]
        uidl = [j.split()[1] for j in [i.decode("utf-8") for i in idl[1]]]
        return uidl
    
    def _header(self, which):
        h = "\n".join([i.decode("utf-8") for i in self.pop3.top(which, 0)[1]]) 
        head = email.message_from_string(h)
        return head

    def headerParser(self, msg):
        subject= msg.get("subject")
        h = email.header.Header(subject)
        dh = email.header.decode_header(h)
        head = {}
        head['subject'] = self.decode_str(dh[0][0].decode("utf-8"))
        head['rcv_time'] = self._rcvtime(msg)
        head['user'], head['address']= email.utils.parseaddr(msg.get("from"))[1].split('@')
        head['send_time'] = time.mktime(email.utils.parsedate(msg.get('date')))
        return head

    def header(self, which):
        h = self._header(which)
        return self.headerParser(h)

    def _rcvtime(self, h):
        words = h[h.keys()[0]].split()
        strftime = ' '.join(words[-6:])
        rcv_time = time.mktime(email.utils.parsedate(strftime))
        return rcv_time
    
    def rcvtime(self, which):
        h = self._header(which)
        return self._rcvtime(h)
    
    def quit(self):
        self.pop3.quit()

    def total(self):
        return self.pop3.stat()[0]

    def pegging_count(self, uid):
        uids = self.uids
        num = uids.index(uid)
        return num+1


    def mail(self, which, stop = None):
        resp, lines, octets = self.pop3.retr(which)
        msg_content = '\n'.join([i.decode("utf-8") for i in lines])
        msg = email.message_from_string(msg_content)
        m = self.headerParser(msg)
#        print msg
        body_html = None
        body_plain = None
        type_html = None
        type_plain = None

        def contentType(part):
            content_type = part.get('Content-Type', '').lower().split("=")[1]

            return content_type

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/html':
                    type_html = contentType(part)
                    body_html = part.get_payload(decode=True)
#                    print (1111111111111111111)
#                    break
                if part.get_content_type() == 'text/plain':
                    type_plain = contentType(part)
                    body_plain = part.get_payload(decode=True)
#                    print (222222222222222222222)
                    break
        elif msg.get_content_type() == 'text/html':
            type_html = contentType(msg)
            body_html = msg.get_payload(decode=True)
#            print (3333333333333333)
        elif msg.get_content_type() == 'text/plain':
            type_plain = contentType(msg)
            body_plain = msg.get_payload(decode=True)
#            print (444444444444444)
 
        if body_html != None and body_plain != None: 
            content = body_plain.decode(type_plain)
        elif body_html == None and body_plain != None:
            content = body_plain.decode(type_plain)
        elif body_html != None and body_plain == None:
            content = body_html.decode("utf-8")
        
        m.update({"content": content})        

        return m

#conn = POP3MailServer()
#conn.connect(POP3['server'],POP3['user'],POP3['password'])
