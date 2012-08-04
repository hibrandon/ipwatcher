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
from utilities import *

class EmailAfterExecGui():
    def __init__(self,master,title='Email After Execution'):
        
        self.pathToExe =""
        self.args = ""
        self.master = master
        self.menubar = Menu(self.master)
        self.title = title
        self.newWindow = True 
        self.preExec = False
        self.logDir = ""#'..' + os.sep + 'logs'
        self.spacer = '*' * 80 + '\n'
        self.spacer += self.spacer + '\n'
        dateStamp = str(datetime.date.today()) + strftime("_%H%M%S")
        self.errorLog = self.logDir + os.sep + 'emailAfterExec.' + str(dateStamp) + ".log"
        writeLog(self.errorLog, "Starting EmailAfterExec on .... " + str(dateStamp) + "\n")
        writeLog(self.errorLog, self.spacer)
        
        
        self.emailConfig = EmailConfigGui(master, False, self.errorLog)
        
        if self.emailConfig.checkMissingConfig() == True:
            message = "This is either the first time you have run this program "
            message += "or you are missing some required configuration"
            
            tkMessageBox.showinfo('Required Configuration Options', message)
            self.emailConfig.display(self)
            
        else:
            self.display()
            
        
       
    def cancel(self): 
        #tkMessageBox.showinfo("Cheers", "Have a good one :) " )
        os.sys.exit(0)
        
    def helpButton(self):
        pass
    
    def showVersion(self):
        pass
        
    def submit(self):
        text = 'COMMAND RESULTS:\n'
        self.preExec = True
        
        
        if self.emailConfig.checkMissingConfig() == True: 
            msg = "Please configure the outgoing email."
            tkMessageBox.showinfo('Configure Email', msg)
            self.showPrefs()
            
                   
        elif self.emailConfig.password.get() == "":
            msg = "Enter your password, hit apply and then resubmit"
            tkMessageBox.showinfo('Authenticate', msg)
            self.showPrefs()
            
        else:
            msg = 'Shall I minimize the window and execute ' + self.pathToExe + ' now?'
            if tkMessageBox.askokcancel('Execute Confirmation', msg):
                self.top.iconify()
                try:
                    self.pathToExe = self.ePath.get().strip()
                    self.args = self.eArgs.get()
                    text += self.captureOutput(self.pathToExe)
                    
                    
                    subject = self.pathToExe + " <-- Command completed"
                    
                    emObj = self.emailConfig
                     
                    email = EmailWrapper(emObj.recipients.get(),subject,text, 
                                         emObj.fromAddress.get(), emObj.password.get(), emObj.server.get(), emObj.port.get())
                    
                    email.mail()
                    
                    if email.hasErrors == True:
                        msg = email.errString
                        msg += "\nValues: \n"
                        msg +=  email.toString()
                        tkMessageBox.showerror('Mail Error Generated', msg)
                        self.top.deiconify()
                        
                    else:
                        tkMessageBox.showinfo("Execution Complete", subject)
                        self.top.deiconify()
                    
                except Exception as inst:
                    output = "ERROR GENERATED in EmailAfterExec.submit:\n"
                    output += "Exception Type: " + str(type(inst)) + "\n"
                    output += "Exception: " + str(inst) + "\n" 
                    tkMessageBox.showerror('Submit Error Generated', output)
                    self.top.deiconify()
            
        
        
        
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
        self.emailConfig.display(self,self.preExec)
        self.top.withdraw()

    
    def display(self, startExecution=False):
        self.startExecution = startExecution
         
        if self.newWindow == False:
            self.top.update()
            self.top.deiconify()
            
            if self.startExecution == True:
                self.submit()

        
        else:
            ## Menu Bar
           
            filemenu = Menu(self.menubar, tearoff=0)
            filemenu.add_command(label="Execute", command=self.submit)
    
            filemenu.add_separator()
    
            filemenu.add_command(label="Exit", command=self.cancel)
            self.menubar.add_cascade(label="File", menu=filemenu)
            editmenu = Menu(self.menubar, tearoff=0)
    
            editmenu.add_separator()
    
            editmenu.add_command(label="Preferences", command=self.showPrefs)
    
            self.menubar.add_cascade(label="Edit", menu=editmenu)
            helpmenu = Menu(self.menubar, tearoff=0)
            helpmenu.add_command(label="Email After Execution Help", command=self.helpButton)
            helpmenu.add_command(label="About...", command=self.showVersion)
            self.menubar.add_cascade(label="Help", menu=helpmenu)
            self.master.config(menu=self.menubar)
            ## End Menu Bar
            
            
            #self.top = Toplevel(self.master)
            
            
            
            self.top = Toplevel(menu=self.menubar, width=500, relief=RAISED,
                                borderwidth=2)
            
            self.top.protocol("WM_DELETE_WINDOW",self.cancel)
            self.top.title(self.title)
            self.top.resizable(width=FALSE, height=FALSE)
            
            
            Label(self.top, text="Programs To Execute",
                               bd=2,relief=SOLID,width=60, bg='gray').grid(columnspan=2,row=6, pady=8)
                               
            
            Label(self.top, text="Path",
                               bd=2,relief=SOLID,width=30).grid(row=7,sticky=W)
            self.ePath = Entry(self.top,width=35, textvariable=self.pathToExe)
            self.ePath.grid(row=7,column=1, pady=3, padx=5,sticky=W)
            
            Button(self.top, text='+',bg='blue', fg='white', command=self.cancel).grid(row=7,column=2)
                               
            Label(self.top, text="Args",
                               bd=2,relief=SOLID,width=30).grid(row=8,sticky=W)
                               
            self.eArgs = Entry(self.top,width=35, textvariable=self.args)
            self.eArgs.grid(row=8,column=1, pady=3, padx=5,sticky=W)
            
            Button(self.top, text='Help',bg='gray', fg='white', command=self.cancel).grid(row=9,column=0,pady=10)
            Button(self.top, text='Submit',bg='blue', fg='white', command=self.submit).grid(row=9,column=1,pady=10)
            Button(self.top, text='Quit',bg='red', fg='white', command=self.cancel).grid(row=9,column=2,pady=10)
            self.newWindow = False
    
if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    emailExec = EmailAfterExecGui(root)
    root.mainloop()
        