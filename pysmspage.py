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

try:
    import configparser
except:
    pass
    import ConfigParser as configparser
# End of Python 2.6+ compatibility code

import os
import platform
import sys
sys.path.append('lib')

from SMSOverSMTP import *
from PersonDatabase import *

class SMSPager:
    def __init__(self):
        self.db = PersonDB(path_to_person_flatfile='personpagingdatabase.fdb')        
        self.SMSGateway = None
    def page(self,recipient,carrier,recipientName,text):
        self.SMSGateway.sendSMS(recipient,carrier,recipientName,text)
    def searchPeople(self,query):
        return self.db.search(query)

class SMSOverSMTPPager(SMSPager):
    def __init__(self):
        self.db = PersonDB(path_to_person_flatfile='personpagingdatabase.fdb')        
        self.SMSGateway = SMSOverSMTPSender()

class PySMSPage:
    def __init__(self,smsPagerClass):
        self.smsPager = smsPagerClass
    def clearScreen(self):
        os.system( "cls" if platform.system() == "Windows"
                   else "clear")
    def mainMenu(self, clearScreen=True):
        menuItems = {'a': ('add person to database',self.addPersonMenu),
                     'd': ('delete/remove person from database', self.removePersonMenu),
                     'p': ('page person',self.pageMenu)}
        if clearScreen == True:
            self.clearScreen()
        while True:
            try:
                print('')
                print('Welcome to PySMSPage!')
                print('')
                print('At any time, press Ctrl+C to quit.')
                print('')
                print('[MAIN MENU]')
                for key in menuItems.keys():
                    print(key, menuItems[key][0])
                choice = input('Enter selection: ')
                if choice in menuItems.keys():
                    menuItems[choice][1]()
                    self.clearScreen()
                else:
                    self.clearScreen()
                    print('Invalid choice.  Please try again!')
            except EOFError:
                pass
                self.clearScreen()
                print('You are already at the Main Menu.  Pressing Ctrl+C will quit.')
                print('')
                print('')
            except KeyboardInterrupt:
                pass
                print('')
                print('')
                print('')
                print('')
                exit(0)
    def addPersonMenu(self):
        print('')
        print('')
        print('Adding a new person to database (Press Ctrl+D to cancel and go back):')
        print('')
        try:
            name = input('Enter full name: ')
            telephone = input('Enter telephone number: ')
            carrier = input('Enter telephone carrier: ')
            key = input('Enter paging ID (shorthand): ')
            self.smsPager.db.addPerson(key,name,telephone,carrier)
            self.smsPager.db.savePersonFlatfile()
        except EOFError:
            pass
    def removePersonMenu(self):
        print('')    
        while True:
            try:
                print('')
                query = input('Query for person deletion (Ctrl+D to go back): ')
            except EOFError:
                pass
                break
            if query != '':
                print('')
                results = self.smsPager.searchPeople(query)
                if len(results) != 1:
                    print("Results for '" + query.lower() + "':")
                for result in results:
                    if len(results) == 1:
                        print('')
                        print('You are about to delete the following person from the database:')
                        print(result,results[result][0],results[result][1])
                        confirm = input('Are you sure? (Y/n): ')
                        if confirm == 'Y' or confirm == 'y':
                            self.smsPager.db.deletePerson(result)
                            self.smsPager.db.savePersonFlatfile()
                        break
                    else:
                        print(results[result][1],
                              ' ',
                              results[result][0],
                              '  (' + result + ')')
    def pageMenu(self):
        while True:
            try:
                print('')
                query = input('Query (Ctrl+D to go back): ')
            except EOFError:
                pass
                break
            if query != '':
                print('')
                results = self.smsPager.searchPeople(query)
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
                        self.smsPager.page(results[result][1],
                                           results[result][2],
                                           results[result][0],
                                           text)
                    else:
                        print(results[result][1],
                              ' ',
                              results[result][0],
                              '  (' + result + ')')


if __name__ == '__main__':
    smsPager = SMSOverSMTPPager()
#    smsPager.db.PersonDatabase = {'doe1':('Jane Doe','5555551212','AT&T (Cingular)'),'deer1':('John Deer','5555551313','Verizon')}
#    smsPager.db.savePersonFlatfile()
    p = PySMSPage(smsPager)
    p.mainMenu(clearScreen=False)
