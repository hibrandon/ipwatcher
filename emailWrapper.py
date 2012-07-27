#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os
import getpass



class EmailWrapper:
    def __init__(self, to, subject, text, fromAddress, pwd, 
                  server="smtp.gmail.com", port=587, attach=None):
        self.to = to
        self.subject = subject
        self.text = text
        self.attach = attach
        self.fromAddress = fromAddress
        self.passwd = pwd
        self.attach = attach
        self.server = server
        self.port = port
        self.hasErrors = False
        self.errString = ""
         
    def mail(self):
        """
        Use the add header message and then the get_all message to add multiple recipients
        """
        msg = MIMEMultipart()
        msg.add_header('From', self.fromAddress)
        msg.add_header('Subject', self.subject)
        
        #Loop over csv string to add recipients
        for emailAddress in self.to.split(','):
            msg.add_header('To', emailAddress)
        
    
        msg.attach(MIMEText(self.text))
    
        if self.attach != None:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(self.attach, 'rb').read())
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                   'attachment; filename="%s"' % os.path.basename(self.attach))
            msg.attach(part)
    
        try:
            mailServer = smtplib.SMTP(self.server, self.port)
            mailServer.ehlo()
            mailServer.starttls()
            mailServer.ehlo()
            
            mailServer.login(self.fromAddress, self.passwd)
            mailServer.sendmail(self.fromAddress, msg.get_all(('To')), msg.as_string())
            # Should be mailServer.quit(), but that crashes...
            
        except smtplib.SMTPAuthenticationError as inst:
            output = "ERROR GENERATED:\n"
            output += "Exception Type: " + str(type(inst)) + "\n"
            output += "Exception: " + str(inst) + "\n"
            self.errString += output + '\n' 
            self.hasErrors = True
            
        except Exception as inst:
            output = "ERROR GENERATED:\n"
            output += "Exception Type: " + str(type(inst)) + "\n"
            output += "Exception: " + str(inst) + "\n"
            self.errString += output + '\n' 
            self.hasErrors = True
        
        finally:
            mailServer.close()

if __name__ == "__main__":
    
    print "Testing Mail function..."
    user = raw_input("Enter your email address: ")
    user = user.strip()
    to = raw_input("Enter the recipients, use comma separation: ")
    to = to.strip()
    
    subject = raw_input("Enter the subject: ")
    text = raw_input("Enter the test message: ")
    text += " END MESSAGE"
    
    print "Warning Eclipse & IDLE echo the password to the screen!"
    pwd = getpass.getpass()
    
    email = EmailWrapper(to,subject,text, user, pwd)
    
    print "Emailing Now...."
    email.mail()
    
    

    print "Done"
