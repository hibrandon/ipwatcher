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
import base64

import datetime
from datetime import date
from time import strftime
from tkFileDialog import askopenfilename, asksaveasfilename,askdirectory
import os
import time
from ConfigParser import SafeConfigParser

from emailWrapper import EmailWrapper
from emailConfigGui import EmailConfigGui

class EmailAfterExecGui():
    def __init__(self,master,title='Email After Execution'):
        
        self.pathToExe =""
        self.args = ""
        self.master = master
        self.title = title
        self.newWindow = True 
        
        self.emailConfig = EmailConfigGui(master, False)
        
        if self.emailConfig.checkMissingConfig() == True:
            message = "This is either the first time you have run this program "
            message += "or you are missing some required configuration"
            
            tkMessageBox.showinfo('Required Configuration Options', message)
            self.emailConfig.display(self)
            
        else:
            self.display()
        
       
    def cancel(self): 
        tkMessageBox.showinfo("Cheers", "Have a good one :) " )
        os.sys.exit(0)
        
    def helpButton(self):
        pass
    
    def showVersion(self):
        pass
        
    def submit(self):
        text = 'COMMAND RESULTS:\n'
        
        
        if self.emailConfig.checkMissingConfig() == True: 
            msg = "Please configure the outgoing email."
            tkMessageBox.showinfo('Configure Email', msg)
            self.showPrefs()
            
                   
        elif self.emailConfig.password.get() == "":
            msg = "Enter your password, hit apply and then resubmit"
            tkMessageBox.showinfo('Authenticate', msg)
            self.showPrefs()
            
        else:
        
            try:
                self.pathToExe = self.ePath.get().strip()
                self.args = self.eArgs.get()
                text += self.captureOutput(self.pathToExe)
                
                
                subject = self.pathToExe + " <-- Command completed"
                
                emObj = self.emailConfig
                 
                email = EmailWrapper(emObj.recipients.get(),subject,text, emObj.fromAddress.get(), emObj.password.get())
                
                email.mail()
                
                if email.hasErrors == True:
                    msg = email.errString
                    msg += "\nValues: \n"
                    msg +=  email.toString()
                    tkMessageBox.showerror('Mail Error Generated', msg)
                    
                else:
                    tkMessageBox.showinfo("Execution Complete", subject)
                
            except Exception as inst:
                output = "ERROR GENERATED in EmailAfterExec.submit:\n"
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
    
    def showPrefs(self): 
        self.emailConfig.display(self)
        self.mainFrame.withdraw()
        print "Withdrew the main frame"
    
    def display(self): 
        if self.newWindow == False:
            self.mainFrame.update()
            self.mainFrame.deiconify()
            print "I called update"
        
        else:
            ## Menu Bar
            menubar = Menu(self.master)
            filemenu = Menu(menubar, tearoff=0)
            filemenu.add_command(label="Execute", command=self.submit)
    
            filemenu.add_separator()
    
            filemenu.add_command(label="Exit", command=self.cancel)
            menubar.add_cascade(label="File", menu=filemenu)
            editmenu = Menu(menubar, tearoff=0)
    
            editmenu.add_separator()
    
            editmenu.add_command(label="Preferences", command=self.showPrefs)
    
            menubar.add_cascade(label="Edit", menu=editmenu)
            helpmenu = Menu(menubar, tearoff=0)
            helpmenu.add_command(label="Email After Execution Help", command=self.helpButton)
            helpmenu.add_command(label="About...", command=self.showVersion)
            menubar.add_cascade(label="Help", menu=helpmenu)
            self.master.config(menu=menubar)
            ## End Menu Bar
            
            
            self.mainFrame = Toplevel(self.master)
            self.mainFrame.title(self.title)
            self.mainFrame.resizable(width=FALSE, height=FALSE)
            self.mainFrame.protocol("WM_DELETE_WINDOW",self.cancel)
            
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
            self.newWindow = False
    
if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    emailExec = EmailAfterExecGui(root)
    root.mainloop()
        