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

from ConfigParser import SafeConfigParser

from emailWrapper import EmailWrapper
from getIP import GetIP
import tkMessageBox
from utilities import *

class WatchIP:
    def __init__(self):
        self.properties = os.getenv("HOME") + os.sep + '.ipwatcher.properties'
        self.prevHostName = ""
        self.prevInternalIp = ""
        self.prevExternalIp = ""
        self.curHostName = ""
        self.curInternalIp = ""
        self.curExternalIp = ""
        self.user = ""
        self.hasChanged = False
        self.hostHasChanged = False
        self.externalIpHasChanged = False
        self.internalIpHasChanged = False
        self.initialRun = True
        self.sectionDict = {'node':['user','internalIp','externalIp','hostname' ]}


        self.parser = SafeConfigParser()
        try:
            self.parser.read(self.properties)
            
        except Exception as inst:
            output = "ERROR GENERATED PARSING: --> " + self.properties + " \n"
            output += "Exception Type: " + str(type(inst)) + "\n"
            output += "Exception: " + str(inst) + "\n"
            print output
            
        
        # Create the properties file if it doesn't exist
        if os.path.exists(self.properties) == False:
            createPropertiesFile(self.properties, self.parser, self.sectionDict)
            
#            self.parser.add_section('node')
#            with file(self.properties, "w+") as fOut:
#                self.parser.write(fOut)
        
        self.getPreviousIP()
        self.getCurrentIP()
        
        self.updateProperties(self.parser, self.properties, 'user', self.user)
        
        if self.prevInternalIp == "":
            self.updateProperties(self.parser, self.properties, 'internalIp', self.curInternalIp)
        
        if self.prevExternalIp == "":
            self.updateProperties(self.parser, self.properties, 'externalIp', self.curExternalIp)

        if self.prevHostName == "":
            self.updateProperties(self.parser, self.properties, 'hostname', self.curHostName)
        
    
    def getPreviousIP(self):
        if os.path.isfile(self.properties):
            try:
                self.prevHostName = self.parser.get('node', 'hostname')
                self.prevInternalIp = self.parser.get('node', 'internalIp')
                self.prevExternalIp = self.parser.get('node', 'externalIp')
    
                self.user = self.parser.get('node', 'user')
     
            except Exception as inst:
                output = "ERROR GENERATED IN getPreviousIP:\n"
                output += "Exception Type: " + str(type(inst)) + "\n"
                output += "Exception: " + str(inst) + "\n"
                print output
                
        else:
            self.getCurrentIP()
            self.prevHostName = self.curHostName
            self.prevInternalIp = self.prevInternalIp
            self.prevExternalIp = self.prevExternalIp      
            
    def getCurrentIP(self):
        ips = GetIP()
        self.curInternalIp = ips.internalIP
        self.curExternalIp = ips.externalIP.strip()
        self.curHostName = ips.host
        self.user = ips.user
        
    def getCurrentIpString(self):
        curVals = "Current Values:\n" 
        curVals += "Internal IP: " + self.curInternalIp + " \n"
        curVals += "External IP: " + self.curExternalIp + " \n"
        curVals += "Hostname: " + self.curHostName + " \n"
        
        return curVals
    
    def getPreviousValuesStrings(self):
        preVals = "Previous Values:\n"
        preVals += "Internal IP: " + self.prevInternalIp + " \n"
        preVals += "External IP: " + self.prevExternalIp + " \n"
        preVals += "Hostname: " + self.prevHostName + " \n"
        
        return preVals    
        
    def updateProperties(self,parser, properties, key, val, section='node'):
        try:
            parser.set(section, key, val)
            
            with open(properties, 'w') as fOut:
                parser.write(fOut)
                
        except Exception as inst:
            output = "ERROR GENERATED in UpdateProperties:\n"
            output += "Exception Type: " + str(type(inst)) + "\n"
            output += "Exception: " + str(inst) + "\n"
            print output
            
        
    def checkForChangeInIpOrHost(self):
       
        self.hasChanged = False
        self.internalIpHasChanged = False
        self.externalIpHasChanged = False
        self.hostHasChanged = False
        
        if self.curExternalIp != self.prevExternalIp:
            self.externalIpHasChanged = True
            self.hasChanged = True          
            
        if self.curInternalIp != self.prevInternalIp:
            self.internalIpHasChanged = True
            self.hasChanged = True
            
        if self.curHostName  != self.prevHostName:
            self.hostHasChanged = True
            self.hasChanged = True
            
        if self.hasChanged:
            self.getPreviousIP()
            
        return self.hasChanged
    
    def updatePropertiesFile(self):
        self.updateProperties(self.parser, self.properties, 'externalIp',self.curExternalIp)
        self.updateProperties(self.parser,self.properties, 'internalIp',self.curInternalIp)  
        self.updateProperties(self.parser, self.properties, 'hostname',self.curHostName)   
        
if __name__ == "__main__":
    watch = WatchIP()
    
    if watch.checkForChangeInIpOrHost():
        print "Either the IP has changed or this is the first time we've run"
    else:
        print "Nothing changed"
        
        
        