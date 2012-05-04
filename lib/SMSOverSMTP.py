#!/usr/bin/env python
#SMSOverSMTP.py
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


# Import WirelessCarriers SMS-over-email-gateway database (stored in a dict)
import WirelessCarriers


# Thanks to http://www.daniweb.com/software-development/python/code/380881/python-3-and-python-2-send-email-through-gmail
# thanks to http://segfault.in/2010/12/sending-gmail-from-python/
import sys
# Import smtplib for the actual sending function
import smtplib
from email.mime.text import MIMEText


# Class that implements functionality to send an SMS (text message) over SMTP, given a carriers database
class SMSOverSMTPSender:
    def __init__(self, path_to_config_file=None, manualPageFunction=None):
        self.config = configparser.SafeConfigParser({'debug': '0',
                                                     'smtp_server': 'localhost',
                                                     'smtp_port': '587',
                                                     'tls_encryption': '1',
                                                     'smtp_user': 'user@example.com',
                                                     'smtp_password': '',
                                                     'page_subject': 'PAGE'})
        if path_to_config_file != None and path_to_config_file != '':
            self.config.read(path_to_config_file)
        else:
            self.config.read('pysmspage.cfg')
            self.config.write(open('pysmspageexample.cfg','w'))
        self.CarrierGateways = WirelessCarriers.WirelessCarrierEmailGateways().getCarrierGateways()
        self.manualPageFunction = manualPageFunction

    def sendEmailOverSMTP(self, to, subject, text):
        msg = MIMEText(text)
        msg['Subject'] = subject
        msg['From'] = self.config.get('DEFAULT','smtp_user')
        msg['To'] = to
        s = smtplib.SMTP(self.config.get('DEFAULT','smtp_server'),
                         self.config.get('DEFAULT','smtp_port'))
        s.ehlo()
        if self.config.get('DEFAULT','tls_encryption') == '1':
            s.starttls()
        try:
            p = self.config.get('DEFAULT','smtp_password')
        except:
            p = None
            pass
        if p != None and p != '':
            s.login(msg['From'], p)
        try:
            # Python 3.2.1
            s.send_message(msg)
        except AttributeError:
            # Python 2.7.2
            s.sendmail(msg['From'], [msg['To']], msg.as_string())
        s.quit()
        
    def sendSMS(self, recipient, carrier, recipientName, text):
        try:
            emailSuffix = self.CarrierGateways[carrier]
        except:
            emailSuffix = None
            print('Error: Unable to locate carrier in wireless carrier gateways table. Check to make sure that carrier exists in the Wireless Carriers database.')
            self.manualPage(recipient,recipientName,text)
            raise
        if emailSuffix == None:
            print('Error: Recipient carrier is set to None! Unable to send SMS message.')
            raise TypeError('Recipient carrier is set to None, so unable to send SMS message.')
        else:
            try:
                self.sendEmailOverSMTP(recipient + emailSuffix,
                                       self.config.get('DEFAULT','page_subject'),
                                       text)
                print('SMS sent to', recipient, '@', carrier)
            except:
                print('Error: Unable to send SMS as e-mail message.')
                raise
    def getCarrierGateways(self):
        return self.CarrierGateways


if __name__ == '__main__':
    s = SMSOverSMTPSender()
    gw = WirelessCarrierEmailGateways().getCarrierGateways()
    for k in gw:
        print(k,'   ',gw[k])

