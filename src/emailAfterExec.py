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
import datetime
from datetime import date
from time import strftime
from tkFileDialog import askopenfilename, asksaveasfilename,askdirectory
import os
from ConfigParser import SafeConfigParser

from emailWrapper import EmailWrapper

class EmailAfterExecGui:
    def __init__(self,master,title='Email After Execution'):
        
        self.password = ""
        self.pathToExe =""
        self.args = ""
        self.fromAddress =""
        self.port = ""
        self.server = ""
        self.toAddresses = ""
        #make this a global import
        self.propertiesDir = r'../conf'
        self.fileProperties = self.propertiesDir + r"/" + 'properties.conf'
        
        try:
            parser = SafeConfigParser()
            parser.read(self.fileProperties)
            
            self.fromAddress = parser.get('email', 'from')
            self.port = parser.get('email', 'port')
            self.server = parser.get('email', 'server')
            self.toAddresses = parser.get('email', 'to')
            self.password = parser.get('email','pwd')
 
        except Exception as inst:
            output = "ERROR GENERATED:\n"
            output += "Exception Type: " + str(type(inst)) + "\n"
            output += "Exception: " + str(inst) + "\n"
            print output
        
        
        self.mainFrame = Toplevel(master)
        self.mainFrame.title(title)
        self.mainFrame.resizable(width=FALSE, height=FALSE)
        self.mainFrame.protocol("WM_DELETE_WINDOW",self.cancel)

 
#        Label(self.mainFrame, text="Email Configuration",
#                           bd=2,relief=SOLID,width=60, bg='gray').grid(columnspan=2,row=0, pady=8)
#                           
#        Label(self.mainFrame, text="Email Address",
#                           bd=2,relief=SOLID,width=30).grid(row=1)
#        self.eFrom = Entry(self.mainFrame,width=35, textvariable=self.fromAddress)
#        self.eFrom.grid(row=1,column=1, pady=3, padx=5)
#        
#        Label(self.mainFrame, text="Server",
#                           bd=2,relief=SOLID,width=30).grid(row=2)
#        Entry(self.mainFrame,width=35, textvariable=self.server).grid(row=2,column=1, pady=3, padx=5)
#        
#        Label(self.mainFrame, text="Port",
#                           bd=2,relief=SOLID,width=30).grid(row=3)
#        Entry(self.mainFrame,width=35, textvariable=self.port).grid(row=3,column=1, pady=3, padx=5)
#        
#        Label(self.mainFrame, text="Receiver Address",
#                           bd=2,relief=SOLID,width=30).grid(row=4)
#        Entry(self.mainFrame,width=35, textvariable=self.toAddresses).grid(row=4,column=1, pady=3, padx=5)
        
#        Label(self.mainFrame, text="Password",
#                           bd=2,relief=SOLID,width=30).grid(row=5)
#        Entry(self.mainFrame,width=35, textvariable=self.password).grid(row=5,column=1, pady=3, padx=5)
    
        
        Label(self.mainFrame, text="Programs To Execute",
                           bd=2,relief=SOLID,width=60, bg='gray').grid(columnspan=2,row=6, pady=8)
                           
        
        Label(self.mainFrame, text="Path",
                           bd=2,relief=SOLID,width=30).grid(row=7,sticky=W)
        self.ePath = Entry(self.mainFrame,width=35, textvariable=self.pathToExe)
        self.ePath.grid(row=7,column=1, pady=3, padx=5,sticky=W)
        
        Button(self.mainFrame, text='+',bg='blue', fg='white', command=self.cancel).grid(row=7,column=2)
                           
        Label(self.mainFrame, text="Args",
                           bd=2,relief=SOLID,width=30).grid(row=8,sticky=W)
                           
        self.eArgs = Entry(self.mainFrame,width=35, textvariable=self.args)
        self.eArgs.grid(row=8,column=1, pady=3, padx=5,sticky=W)
        
        Button(self.mainFrame, text='Help',bg='gray', fg='white', command=self.cancel).grid(row=9,column=0,pady=10)
        Button(self.mainFrame, text='Submit',bg='blue', fg='white', command=self.submit).grid(row=9,column=1,pady=10)
        Button(self.mainFrame, text='Quit',bg='red', fg='white', command=self.cancel).grid(row=9,column=2,pady=10)
        
    def cancel(self): 
        tkMessageBox.showinfo("Cheers", "Have a good one :) " )
        os.sys.exit(0)
        
    def submit(self):
        text = 'COMMAND RESULTS:\n'
        
        try:
            self.pathToExe = self.ePath.get().strip()
            self.args = self.eArgs.get()
            print self.pathToExe
            text += self.captureOutput(self.pathToExe)
            
            
            subject = self.pathToExe + " <-- Command completed"
             
            email = EmailWrapper(self.toAddresses,subject,text, self.fromAddress, self.password)
            email.mail()
            tkMessageBox.showinfo("Execution Complete", subject)
            
        except Exception as inst:
            output = "ERROR GENERATED:\n"
            output += "Exception Type: " + str(type(inst)) + "\n"
            output += "Exception: " + str(inst) + "\n" 
            print output
        
        os.sys.exit(0)
        
        
        
    ## ----------------------------------------------------------------------------
    ## captureOutput -  Wrapper function that captures the standard output of an
    ##                  external command and returns that ouput in string format
    ##                  
    ## ---------------------------------------------------------------------------- 
    def captureOutput(self, cmd):
        try:
            stream = os.popen(cmd)
            output = stream.read()
            stream.close()
            
        except Exception as inst:
            output = "ERROR GENERATED:\n"
            output += "CMD: " + cmd + "\n"
            output += "Exception Type: " + str(type(inst)) + "\n"
            output += "Exception: " + str(inst) + "\n"
    
            
        return str(output)   
    
if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    emailExec = EmailAfterExecGui(root)
    root.mainloop()
        