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


import os
import time
import tkMessageBox
from Tkinter import *
import threading

from watchIP import WatchIP
from emailConfigGui import EmailConfigGui
from emailWrapper import EmailWrapper


class ExecuteWatchThread(threading.Thread):
    def __init__(self, interval, fromAddress, password,recipients,
                 watchInternalIP=True, watchExternalIP=True,
                 watchHostname=True, server='smtp.gmail.com', port=587):
        
        self._stopEvent = threading.Event()
        self.newCommandPoll = 5
        self.interval = interval
        self.fromAddress = fromAddress
        self.password = password
        self.recipients = recipients
        self.server = server
        self.port = port
        self.watchInternalIP = watchInternalIP
        self.watchExternalIP = watchExternalIP
        self.watchHostname = watchHostname
        self.execWatchThread = None
        
        self.watch = WatchIP()
        
        
        threading.Thread.__init__(self, name="WatchIP")
        
    def run(self):
        print "Running the thread"
        print "Interval == ", self.interval
        
        while not self._stopEvent.isSet():
            remainingTime = 30 #self.interval
            count = 0
            while (remainingTime > 0) & (not self._stopEvent.isSet()) :
                self._stopEvent.wait(self.newCommandPoll)
                remainingTime -= self.newCommandPoll
                print str(count) + "Listening for stop"
                count += 1
            print "End of an interval checking for change now"   
            
            if self.watchedValueHasChanged():
                print "Values have changed"
                subject = "Watch Value Changed for NODE: " + self.watch.curHostName
                text = self.watch.getCurrentIpString()

                email = EmailWrapper(self.recipients,subject,text, self.fromAddress, self.password, self.server, self.port)   
                email.mail()
                
                if not email.hasErrors:
                    print "Email sent"
                    
                else:
                    print email.errString

    def watchedValueHasChanged(self):
        notify = False
        self.watch.updateOnChangeInIpOrHost()
    
        if self.watchExternalIP == True:
            if self.watch.externalIpHasChanged == True:
                notify = True
                
        if self.watchInternalIP  == True:
            if self.watch.internalIpHasChanged == True:
                notify = True
                
        if self.watchHostname == True:
            if self.watch.hostHasChanged == True:
                notify = True
                
        return notify       
                
    def join(self, timeout=None):
        print "And the thread goes away............."
        self._stopEvent.set()
        threading.Thread.join(self, timeout)
        
    
        
                
class WatchIpGui:
    def __init__(self, master, title='IP Watchdog'):
        self.master = master
        self.master.title(title)
        self.menubar = Menu(self.master)
        self.cbInternalIp = BooleanVar()
        self.cbExternalIp = BooleanVar()
        self.cbHostname   = BooleanVar()
        self.unitSelection = StringVar()
        self.watch = WatchIP()
        self.watch.getCurrentIP()
        self.vInternalIp = StringVar()
        self.vExternalIp = StringVar()
        self.vHostname   = StringVar()
        self.isStarted = False
        self.newWindow = True
        self.preExec = False
        self.scale = None
        self.stop = True
        
        self.execWatchThread = None
        
        self.display()
        
        self.emailConfig = EmailConfigGui(master, False, properties='.ipwatcher.email.properties')
        
        
    def display(self, startExecution=False):
        
        self.startExecution = startExecution
        
         
        if self.newWindow == False:
            self.top.update()
            self.top.deiconify()
            
            if self.startExecution == True:
                self.action()
        
        else:
            curRow = 0
    
    
            ## Menu Bar
            
            filemenu = Menu(self.menubar, tearoff=0)
            filemenu.add_command(label="Execute", command=self.action)
    
            filemenu.add_separator()
    
            filemenu.add_command(label="Exit", command=self.quit)
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
    
            self.top = Toplevel(menu=self.menubar, width=500, relief=RAISED,
                                borderwidth=2)
            
            self.top.protocol("WM_DELETE_WINDOW",self.quit)
    
            gridWidth = 30
            px = 5
            lWidth = 15
            py = 18
    
            #Grid Start
    
            #Notify on Change
            Label(self.top, text='Notify on Change in:',
                  relief=RIDGE, bg='gray',  width=gridWidth).grid(row=curRow, column=0, columnspan=2, pady=py)
    
            curRow += 1
            
            Label(self.top, text='Internal IP', relief=RIDGE,  width=15).grid(row=curRow, column=0)
            Checkbutton(self.top,variable=self.cbInternalIp).grid(row=curRow, column=1, sticky=W, padx=px)
    
            curRow += 1
            
            Label(self.top, text='External IP', relief=RIDGE,  width=15).grid(row=curRow, column=0)
            Checkbutton(self.top,variable=self.cbExternalIp).grid(row=curRow, column=1, sticky=W,padx=px)
    
            curRow += 1
            
            Label(self.top, text='Hostname', relief=RIDGE,  width=15).grid(row=curRow, column=0)
            Checkbutton(self.top,variable=self.cbHostname).grid(row=curRow, column=1, sticky=W,padx=px)
    
    
            #Change Frequency
            curRow += 1
            Label(self.top, text='Poll Frequency:',
                  relief=RIDGE, bg='gray',  width=gridWidth).grid(row=curRow,
                                                                  column=0, columnspan=2, pady=py)
            curRow += 1     
            Label(self.top, text='Units', relief=RIDGE,  width=15).grid(row=curRow, column=0)
            self.optionList = ['minute(s)','hour(s)','day(s)']
            self.unitSelection.set(self.optionList[0])
            OptionMenu(self.top, self.unitSelection, *self.optionList, command=self.updateInterval).grid(row=curRow, column=1, stick=EW)
            
            self.min = 5.0
            self.max = 60.0
    
            curRow += 1
            Label(self.top, text='Interval', relief=SUNKEN,  width=lWidth).grid(row=curRow, column=0,padx=px)
            self.scl = Scale(self.top, from_=self.min, to=self.max, orient=HORIZONTAL)
            self.scl.grid(row=curRow, column=1,padx=px)
    
    
            #Current Values
            curRow += 1
            Label(self.top, text='Current Values:',
                  relief=RIDGE, bg='gray',  width=gridWidth).grid(row=curRow,
                                                                  column=0, columnspan=2, pady=py)
    
            
            curRow += 1
            Label(self.top, text='Internal IP', relief=SUNKEN,  width=lWidth).grid(row=curRow, column=0,padx=px)
            self.eInternalIp = Entry(self.top,state='readonly', textvariable=self.vInternalIp)
            self.eInternalIp.grid(row=curRow, column=1, sticky=W,padx=px)
            
            
    
            curRow += 1
            
            Label(self.top, text='External IP', relief=SUNKEN,  width=lWidth).grid(row=curRow, column=0,padx=px)
            self.eExternalIp = Entry(self.top,state='readonly', textvariable=self.vExternalIp)
            self.eExternalIp.grid(row=curRow, column=1, sticky=W,padx=px)
            #self.vExternalIp.set()
    
            curRow += 1
            
            Label(self.top, text='Hostname', relief=SUNKEN,  width=lWidth).grid(row=curRow, column=0, padx=px)
            self.eHostname = Entry(self.top,state='readonly', textvariable=self.vHostname)
            self.eHostname.grid(row=curRow, column=1, sticky=W,padx=px)
    
    
            #Actions
            
            curRow += 1
            Label(self.top, text='Actions:',
                  relief=RIDGE, bg='gray',  width=gridWidth).grid(row=curRow,
                                                                  column=0, columnspan=2, pady=py)
            
            curRow += 1      
            Button(self.top, text='Quit',bg='blue', fg='white', command=self.quit).grid(row=curRow,column=0, pady=5)
            self.actionButton =Button(self.top, text='Start',bg='blue', fg='white', command=self.action)
            self.actionButton.grid(row=curRow,column=1, pady=5)
            
            self.updateEntries()
            self.newWindow = False
    
            #Grid End
        
    def updateEntries(self):
        self.vInternalIp.set(self.watch.curInternalIp)
        self.vExternalIp.set(self.watch.curExternalIp)
        self.vHostname.set(self.watch.curHostName)
      
    def showPrefs(self): 
        self.emailConfig.display(self, self.preExec)
        self.top.withdraw()
        
    
    def helpButton(self):
        pass
    
    def showVersion(self):
        pass

    def quit(self): 
        if self.execWatchThread != None:
            if self.execWatchThread.isAlive():
                self.execWatchThread.join()
                
        os.sys.exit(0)
        
    def action(self):
        
        if not self.isStarted:
            
            if self.emailConfig.checkMissingConfig() == True: 
                self.preExec = True
                msg = "Please configure the outgoing email."
                tkMessageBox.showinfo('Configure Email', msg)
                self.showPrefs()
                   
            elif self.emailConfig.getPassword() == "":
                self.preExec = True
                msg = "Enter your password to start watching."
                tkMessageBox.showinfo('Authenticate', msg)
                self.showPrefs()
                
            else:
                self.getNotificationList()
 
                if len(self.notifyList) == 0:
                    tkMessageBox.showerror("Insufficient Input", "Please check an item to watch.")
                    
                else:
                    msg = "I will minimize the window and then I will poll the system in " + str(self.scl.get()) + " " + self.unitSelection.get().replace('(s)','')
                    msg += " intervals. Finally I will email/text on change in:\n\n" + '\n'.join(self.notifyList)
                     
                    if tkMessageBox.askokcancel('Execute Confirmation', msg):
                        self.isStarted = not self.isStarted
                        self.actionButton.config(text='Stop')
                        self.top.iconify() 
                        
                        self.normalizeInterval()
                        em = self.emailConfig
                        self.execWatchThread = ExecuteWatchThread(self.scale, em.fromAddress.get(),em.getPassword(),em.recipients.get(),
                                                                   self.cbInternalIp.get(), self.cbExternalIp.get(),
                                                                   self.cbHostname.get(), em.server.get(), em.port.get())
                        self.execWatchThread.start() 
                        
#                        self.emailOnChange() 
#                        self.top.deiconify()
                        print "Done"       

        else:
            self.actionButton.config(text='Start')
            self.isStarted = not self.isStarted
            if self.execWatchThread.isAlive():
                self.execWatchThread.join()
                
            print "She is gone"
            print "Living? ", self.execWatchThread.isAlive()
            
            
    def getNotificationList(self):
        self.notifyList = []

        if self.cbExternalIp.get():
            self.notifyList.append('External IP')
            
        if self.cbInternalIp.get():
            self.notifyList.append('Internal IP')
            
        if self.cbHostname.get():
            self.notifyList.append('Hostname')  
             
            
    
    
    def emailOnChange(self):
        self.normalizeInterval()
        print "Is Started: ", self.isStarted
        
        if self.scale != None:
            
            while self.isStarted == True:
                
                time.sleep(30)
                if self.watchedValueHasChange() == True:
                    tkMessageBox.showinfo("Change Detected", self.watch.getCurrentIpString())
                    
                else:
                    tkMessageBox.showinfo("No Change Detected", self.watch.getCurrentIpString())
                    print "Is Started: ", self.isStarted
                
        
    
    def normalizeInterval(self):
        self.scale = self.scl.get()
        if self.unitSelection.get() == 'minutes(s)':
            self.scale = self.scale * 60
            
        elif self.unitSelection.get() == 'hour(s)':
            self.scale = self.scale * 60  * 60
        
        elif self.unitSelection.get() == 'days(s)':
            self.scale = self.scale * 24 * 60 * 60
        else:
            self.ErrStr = "Error:  Unknown unit --> " + str(self.unitSelection.get())
            
        print self.scale
        self.scale = 120
        
        
        
    def updateInterval(self, event=None):
        if self.unitSelection.get() == self.optionList[0]:
            self.min = 5
            self.max = 60

        elif self.unitSelection.get() == self.optionList[1]:
            self.min = 1
            self.max = 24
        else:
            self.min = 1
            self.max = 7
            
        self.scl.config(from_=self.min)
        self.scl.config(to=self.max)
    

if __name__ == '__main__':
    root = Tk()
    root.withdraw()
    app = WatchIpGui(root)
    root.mainloop()

