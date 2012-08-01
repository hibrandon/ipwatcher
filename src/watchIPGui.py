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
import tkMessageBox
from Tkinter import *

from watchIP import WatchIP
from emailConfigGui import EmailConfigGui



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
        
        
        self.display()
        
        self.emailConfig = EmailConfigGui(master, False)
        
        
    def display(self):
        curRow = 0


        ## Menu Bar
        
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Execute", command=self.start)

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
        Button(self.top, text='Start',bg='blue', fg='white', command=self.start).grid(row=curRow,column=1, pady=5)
        
        self.updateEntries()
        

        #Grid End
        
    def updateEntries(self):
        self.vInternalIp.set(self.watch.curInternalIp)
        self.vExternalIp.set(self.watch.curExternalIp)
        self.vHostname.set(self.watch.curHostName)
      
    def showPrefs(self): 
        self.emailConfig.display(self)
        self.mainFrame.withdraw()
        print "Withdrew the main frame"
          
    def showPrefs(self):
        pass
    
    def helpButton(self):
        pass
    
    def showVersion(self):
        pass

    def quit(self): 
        tkMessageBox.showinfo("Cheers", "Have a good one :) " )
        os.sys.exit(0)
        
    def start(self):
        pass
        
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

def main():
    root = Tk()
    root.withdraw()
    app = WatchIpGui(root)
    root.mainloop()

if __name__ == '__main__':
    main()

