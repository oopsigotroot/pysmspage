import smtpd
import asyncore
from email.parser import Parser
import email

class CustomSMTPServer(smtpd.SMTPServer):
    
    def process_message(self, peer, mailfrom, rcpttos, data):
        print('Receiving message from:',peer)
        print('Message addressed from:',mailfrom)
        print('Message addressed to  :' ,rcpttos)
        print('Message length        :',len(data))
        print('Data:')
        print(data)
        header = Parser().parsestr(data)
        print('Subject:', header['subject'])
        print('Body:')
        msg = email.message_from_string(data)
        for part in msg.walk():
            # multipart/* are just containers
            if part.get_content_maintype() == 'multipart':
                continue
            # Applications should really sanitize the given filename so that an
            # email message can't be used to overwrite important files
            if part.get_content_maintype() == 'text':
                print('',part.get_payload(decode=True))
            else:
                print('[Message of type:', part.get_content_maintype(), ']')
        return

server = CustomSMTPServer(('127.0.0.1', 1025), None)

asyncore.loop()
