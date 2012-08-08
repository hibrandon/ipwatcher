"""
   Copyright 2012 Brandon Sutherlin, Mike Deats, and Ryan Neal

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
""" 

import tkMessageBox
from Tkinter import *
from ConfigParser import SafeConfigParser
import os
import base64

from emailWrapper import EmailWrapper
from utilities import *


class EmailConfigGui():
    def __init__(self, master,display=True,errorLog="", isMain=False, title="Email Configuration", properties=".email.properties"):
        self.title = title
        self.master = master
        self.password = StringVar()
        self.fromAddress = StringVar()
        self.port = StringVar()
        self.server = StringVar()
        self.recipients = StringVar()
        
        self.tmpPassword = ''
        self.tmpFromAddress = ''
        self.tmpPort = ''
        self.tmpServer = ''
        self.tmpRecipient = ''
        self.tmpSavePassword = ''
        self.sections = ['from','port','server','to', 'password']
        self.sectionsDict = {'email':self.sections}
        self.errorLog = errorLog
        
        
        
        
         #setup properties file
        self.properties = setupPropertiesFilePath(properties)

        self.isMain = isMain
        self.isDisplayed = False
        self.parser = SafeConfigParser()
        self.parser.read(self.properties)
        self.newWindow = True
        
        # Create the properties file if it doesn't exist
        propertiesFileIntact, errString = isPropertiesFileIntact(self.properties, self.parser, self.sectionsDict)
        
        if propertiesFileIntact == False:
            writeLog(self.errorLog, errString)
            deleted, errString = deleteFile(self.properties)
            
            if not deleted:
                writeLog(self.errorLog, errString)
                
            success, errString = createPropertiesFile(self.properties, self.parser, self.sectionsDict)
            
            if success == False:
                writeLog(self.errorLog, errString)
            
                
        else:    
            self.fromAddress.set(self.readProp(self.parser, self.properties, 'from'))
            self.port.set(self.readProp(self.parser, self.properties,'port'))
            self.server.set(self.readProp(self.parser, self.properties, 'server'))
            self.recipients.set(self.readProp(self.parser, self.properties, 'to'))
            self.password.set(self.readProp(self.parser, self.properties,'password'))
     

                
            
        if display:
            self.display()
           
    def readProp(self, parser, properties, key, section='email'):
        val = ""
        try:
            val = self.parser.get(section, key)
        except Exception as inst:
            output = "ERROR GENERATED: EmailConfigGUI.readProp\n"
            output += "Exception Type: " + str(type(inst)) + "\n"
            output += "Exception: " + str(inst) + "\n"
            writeLog(self.errorLog,output)
            
            writeLog(self.errorLog, 'Properties File appears to be corrupted attempting to recreate it')
            
            
        return val
        
    def apply(self):  
        #grab temp params and obfuscate password
        self.getCurrentParameters()
              
        updateProperties(self.parser, self.properties, 'from', self.tmpFromAddress, 'email')        
        updateProperties(self.parser, self.properties, 'to',self.tmpRecipient, 'email')
        updateProperties(self.parser, self.properties, 'port',self.tmpPort, 'email')
        updateProperties(self.parser, self.properties, 'server',self.tmpServer, 'email')
        
        if self.savePassword.get() == True:
            msg = "The password though obfuscated will be saved in an insecure manner."
            msg += "This is not recommended.  Are you sure you wish to do this?"
            if tkMessageBox.askyesno('Dangerous Action', msg ):
                
                updateProperties(self.parser,self.properties, 'password', self.tmpPassword, 'email')

        tkMessageBox.showinfo('Changes Applied', 'Your changes have been applied.')
        self.applied = True
        self.cancel()
        
    
    def cancel(self): 
        if self.isMain == True:
            #tkMessageBox.showinfo("Cheers", "Have a good one :) " )
            os.sys.exit(0)
        else:
            self.running = False
            if self.applied == False:
                self.preExecution = False
                
            if self.parentWindow != None:
                self.mainFrame.withdraw()
                self.parentWindow.display(self.preExecution) 
        
         
    def checkMissingConfig(self):
        """
        Initially display is not called so the property variables must also be checked
        """
        self.hasMissingConfig = False
            
        if self.fromAddress.get() == "":
            self.hasMissingConfig = True
            
        if self.port.get() == "":
            self.hasMissingConfig = True
            
        if self.server.get() == "":
            self.hasMissingConfig = True
        
        if self.recipients.get() == "":
            self.hasMissingConfig = True
            
        return self.hasMissingConfig
    

            
    def display(self, parentWindow=None, preExecution=False):
        self.preExecution = preExecution
        self.applied = False
        
        if self.newWindow == False:
            self.mainFrame.update()
            self.mainFrame.deiconify()
        
        else:
            self.parentWindow = parentWindow
            
            self.mainFrame = Toplevel(self.master)
            self.mainFrame.title(self.title)
            self.mainFrame.resizable(width=FALSE, height=FALSE)
            self.mainFrame.protocol("WM_DELETE_WINDOW",self.cancel)
            self.isDisplayed  = True
            self.savePassword = BooleanVar()
    
            eWidth = 30
            lWidth = 20
            curRow = 0
     
            Label(self.mainFrame, text="Email Configuration",
                               bd=2,relief=SOLID,width=45, bg='gray').grid(columnspan=2,row=curRow, pady=8)
            
            curRow += 1               
            Label(self.mainFrame, text="Sender Email Address",
                               bd=2,relief=SOLID,width=lWidth).grid(row=curRow)
            self.eFrom = Entry(self.mainFrame,width=eWidth, textvariable=self.fromAddress)
            self.eFrom.grid(row=curRow,column=1, pady=3, padx=5)
           
            
            curRow += 1 
            
            Label(self.mainFrame, text="Server",
                               bd=2,relief=SOLID,width=lWidth).grid(row=curRow)
            self.eServer = Entry(self.mainFrame,width=eWidth, textvariable=self.server)
            self.eServer.grid(row=curRow,column=1, pady=3, padx=5)
            
            
            curRow += 1 
            Label(self.mainFrame, text="Port",
                               bd=2,relief=SOLID,width=lWidth).grid(row=curRow)
            self.ePort = Entry(self.mainFrame,width=eWidth, textvariable=self.port)
            self.ePort.grid(row=curRow,column=1, pady=3, padx=5)
            
            
            curRow += 1 
            Label(self.mainFrame, text="Recipients",
                               bd=2,relief=SOLID,width=lWidth).grid(row=curRow)
            self.eRecipients = Entry(self.mainFrame,width=eWidth, textvariable=self.recipients)
            self.eRecipients.grid(row=curRow,column=1, pady=3, padx=5)
            
            curRow += 1 
            Label(self.mainFrame, text="Password",
                               bd=2,relief=SOLID,width=lWidth).grid(row=curRow)        
            self.ePassword = Entry(self.mainFrame,width=eWidth, textvariable=self.password, show='*')
            self.ePassword.grid(row=curRow,column=1, pady=3, padx=5)
            
            curRow += 1 
            Button(self.mainFrame, text='Test',bg='blue', fg='white', command=self.testConfiguration).grid(row=curRow,column=0, pady=5)
            cbPassword = Checkbutton(self.mainFrame, text='Save Password\n(Not Recommended)',var=self.savePassword)
            cbPassword.grid(row=curRow,column=1, pady=5)
            
            
            curRow += 1 
            Button(self.mainFrame, text='Cancel',bg='blue', fg='white', command=self.cancel).grid(row=curRow,column=0, pady=5)
            Button(self.mainFrame, text='Apply',bg='blue', fg='white', command=self.apply).grid(row=curRow,column=1, pady=5)
            self.newWindow = False
            
    def getCurrentParameters(self):
        
        self.obsPassword = self.password.get().strip()
        self.obsPassword = obfuscateString(self.obsPassword)
        
        self.tmpPassword = self.obsPassword
        self.tmpFromAddress = self.fromAddress.get().strip()
        self.tmpPort = self.port.get().strip()
        self.tmpServer = self.server.get().strip()
        self.tmpRecipient = self.recipients.get().strip()
        self.tmpSavePassword = self.savePassword.get()
        
        
    def checkCurrentParameters(self):
        self.missingTempParam = False
        self.getCurrentParameters()
        
        if self.tmpPassword == "":
            self.missingTempParam = True
            
        if self.tmpFromAddress == "":
            self.missingTempParam = True
            
        if self.tmpPort == "":
            self.missingTempParam = True
            
        if self.tmpServer == "":
            self.missingTempParam = True
            
        if self.tmpRecipient == "":
            self.missingTempParam = True
            
        return self.missingTempParam
    
    def getPassword(self):
        obsPassword = self.password.get().strip()
        obsPassword = obfuscateString(obsPassword)
        return obsPassword
        
        
    def testConfiguration(self):
        self.checkCurrentParameters()
        
        if self.missingTempParam == True:
            tkMessageBox.showerror('Missing Configuration Information', 'Please complete all configuration information')
            
        else:
            text = 'This is a test email'
            subject = 'Email Configuration Test'
            
            email = EmailWrapper(self.tmpRecipient,subject,text, self.tmpFromAddress, self.tmpPassword)
            
            email.mail()
            
            if email.hasErrors:
                tkMessageBox.showerror('Error Generated', email.errString) 
                
            else:
                tkMessageBox.showinfo('Test Completed Successfully', 'You should receive an email with the subject --> ' + subject)
                  
                
#    def updateProperties(self, parser, propertiesFile, key, val, section='email'):
#        success = True
#        output = ""
#
#        try:
#            parser.set(section, key, val)
#            
#            with open(propertiesFile, 'w') as fOut:
#                parser.write(fOut)
#
#                
#        except Exception as inst:
#            success = False
#            output = "ERROR GENERATED in Utilities.UpdateProperties:\n"
#            output += "Exception Type: " + str(type(inst)) + "\n"
#            output += "Exception: " + str(inst) + "\n"
#            
#            print output
#
#        return success, output
            
    
if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    emailConf = EmailConfigGui(root, True, "", True)
    root.mainloop()
