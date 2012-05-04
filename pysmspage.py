#!/usr/bin/env python
#pysmspage.py
#
#Copyright 2012 - Patrick F. Wilbur <proj pdub net>
#
#



# Python 2.6+ compatibility:
from __future__ import print_function
try:
    input = raw_input
except:
    pass
# End of Python 2.6+ compatibility code

import os
import platform
import sys
sys.path.append('lib')

from SMSOverSMTP import *
from PersonDatabase import *

class SMSPager:
    def __init__(self):
        self.db = PersonDB()        
        self.SMSGateway = None
    def page(self,recipient,carrier,recipientName,text):
        self.SMSGateway.sendSMS(recipient,carrier,recipientName,text)
    def searchPeople(self,query):
        return self.db.search(query)

class SMSOverSMTPPager(SMSPager):
    def __init__(self):
        self.db = PersonDB()
        self.SMSGateway = SMSOverSMTPSender()

def clearScreen():
    os.system( "cls" if platform.system() == "Windows"
               else "clear")


if __name__ == '__main__':
    p = SMSOverSMTPPager()
    p.db.PersonDatabase = {'doe1':('Jane Doe','5555551212','AT&T (Cingular)'),
                           'deer1':('John Deer','5555551313','Verizon')}
    try:
        while True:
            clearScreen()
            print('Welcome to PySMSPage!')
            print('')
            print('At any time, press Ctrl+C to quit.')
            print('')
            print('')
            while True:
                try:
                    print('')
                    query = input('Query (Ctrl+D to go back): ')
                except EOFError:
                    pass
                    break
                if query != '':
                    print('')
                    results = p.searchPeople(query)
                    if len(results) != 1:
                        print("Results for '" + query.lower() + "':")
                    for result in results:
                        if len(results) == 1:
                            print('Paging', results[result][0],
                                  '(' + result + ')',
                                  '@',
                                  results[result][1],
                                  '...')
                            try:
                                text = input('Enter a page message (Ctrl+D to cancel): ')
                            except EOFError:
                                pass
                                continue
                            p.page(results[result][1],
                                   results[result][2],
                                   results[result][0],
                                   text)
                        else:
                            print(results[result][1], ' ', results[result][0], '  (' + result + ')')
    except KeyboardInterrupt:
        pass
        print('')
        print('')
        print('')
        print('')
        exit(0)
