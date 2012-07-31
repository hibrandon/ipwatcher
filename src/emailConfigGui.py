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


class EmailConfigGui():
    def __init__(self, master,display=True,isMain=False, title="Email Configuration"):
        self.title = title
        self.master = master
        self.password = ""
        self.fromAddress =""
        self.port = ""
        self.server = ""
        self.recipients = ""
        self.properties = '.properties'
        self.isMain = isMain
        self.isDisplayed = False
        self.parser = SafeConfigParser()
        self.parser.read(self.properties)
        
        try:
            
            
            self.fromAddress = self.parser.get('email', 'from')
            self.port = self.parser.get('email', 'port')
            self.server = self.parser.get('email', 'server')
            self.recipients = self.parser.get('email', 'to')
            self.password = self.parser.get('email','pwd')
 
        except Exception as inst:
            output = "ERROR GENERATED:\n"
            output += "Exception Type: " + str(type(inst)) + "\n"
            output += "Exception: " + str(inst) + "\n"
            print output
            
            
        if display:
            self.display()
            
        
    def apply(self):
        self.fromAddress = self.eFrom.get().strip()
        self.recipients = self.eRecipients.get().strip()
        self.port = self.ePort.get().strip()
        self.server = self.eServer.get().strip()
        self.password = self.ePassword.get().strip()
        
        
        self.updateProperties(self.parser, 'from', self.fromAddress )
        self.updateProperties(self.parser, 'to',self.recipients)
        self.updateProperties(self.parser, 'port',self.port)
        self.updateProperties(self.parser, 'server',self.server)
        
        if self.savePassword.get() == True:
            msg = "The password though obfuscated will be saved in an insecure manner."
            msg += "This is not recommended.  Are you sure you wish to do this?"
            if tkMessageBox.askyesno('Dangerous Action', msg ):
                
                self.updateProperties(self.parser, 'pwd', self.ePassword.get().strip())

        tkMessageBox.showinfo('Changes Applied', 'Your changes have been applied.')
        self.cancel()
        
    
    def cancel(self): 
        if self.isMain == True:
            tkMessageBox.showinfo("Cheers", "Have a good one :) " )
            os.sys.exit(0)
        else:
            self.running = False
            if self.parentWindow != None:
                self.parentWindow.display()
            self.mainFrame.destroy()
            
    def updateProperties(self,parser, key, val, section='email', propFile='.properties'):
        
        try:
            parser.set(section, key, val)
            
            with open(propFile, 'w') as fOut:
                parser.write(fOut)
                
        except Exception as inst:
            output = "ERROR GENERATED in UpdateProperties:\n"
            output += "Exception Type: " + str(type(inst)) + "\n"
            output += "Exception: " + str(inst) + "\n"
            print output
        
    def checkMissingConfig(self):
        self.hasMissingConfig = False
            
        if self.fromAddress == "":
            self.hasMissingConfig = True
            
        if self.port == "":
            self.hasMissingConfig = True
            
        if self.server == "":
            self.hasMissingConfig = True
        
        if self.recipients == "":
            self.hasMissingConfig = True
            
        return self.hasMissingConfig
            
    def display(self, parentWindow=None):
        self.parentWindow = parentWindow
        
        self.mainFrame = Toplevel(self.master)
        self.mainFrame.title(self.title)
        self.mainFrame.resizable(width=FALSE, height=FALSE)
        self.mainFrame.protocol("WM_DELETE_WINDOW",self.cancel)
        self.isDisplayed  = True
        self.savePassword = BooleanVar()

        eWidth = 30
        lWidth = 20
 
        Label(self.mainFrame, text="Email Configuration",
                           bd=2,relief=SOLID,width=45, bg='gray').grid(columnspan=2,row=0, pady=8)
                           
        Label(self.mainFrame, text="Sender Email Address",
                           bd=2,relief=SOLID,width=lWidth).grid(row=1)
        self.eFrom = Entry(self.mainFrame,width=eWidth, textvariable=self.fromAddress)
        self.eFrom.grid(row=1,column=1, pady=3, padx=5)
        self.eFrom.delete(0, END)
        self.eFrom.insert(0,self.fromAddress)
        
        Label(self.mainFrame, text="Server",
                           bd=2,relief=SOLID,width=lWidth).grid(row=2)
        self.eServer = Entry(self.mainFrame,width=eWidth, textvariable=self.server)
        self.eServer.grid(row=2,column=1, pady=3, padx=5)
        self.eServer.delete(0, END)
        self.eServer.insert(0,self.server)
        
        Label(self.mainFrame, text="Port",
                           bd=2,relief=SOLID,width=lWidth).grid(row=3)
        self.ePort = Entry(self.mainFrame,width=eWidth, textvariable=self.port)
        self.ePort.grid(row=3,column=1, pady=3, padx=5)
        self.ePort.delete(0, END)
        self.ePort.insert(0,self.port)
        
        Label(self.mainFrame, text="Recipients",
                           bd=2,relief=SOLID,width=lWidth).grid(row=4)
        self.eRecipients = Entry(self.mainFrame,width=eWidth, textvariable=self.recipients)
        self.eRecipients.grid(row=4,column=1, pady=3, padx=5)
        self.eRecipients.delete(0, END)
        self.eRecipients.insert(0,self.recipients)
        
        Label(self.mainFrame, text="Password",
                           bd=2,relief=SOLID,width=lWidth).grid(row=5)        
        self.ePassword = Entry(self.mainFrame,width=eWidth, textvariable=self.password, show='*')
        self.ePassword.grid(row=5,column=1, pady=3, padx=5)
        self.ePassword.delete(0, END)
        self.ePassword.insert(0,self.password)
        
        cbPassword = Checkbutton(self.mainFrame, text='Save Password\n(Not Recommended)',var=self.savePassword)
        cbPassword.grid(row=6,column=0, columnspan=2, pady=5)
        Button(self.mainFrame, text='Cancel',bg='blue', fg='white', command=self.cancel).grid(row=7,column=0, pady=5)
        Button(self.mainFrame, text='Apply',bg='blue', fg='white', command=self.apply).grid(row=7,column=1, pady=5)
        
if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    emailConf = EmailConfigGui(root, True, True)
    root.mainloop()