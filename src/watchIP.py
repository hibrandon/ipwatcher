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
        self.exteralIpHasChanged = False
        self.internalIpHasChanged = False
        self.initialRun = True


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
            self.parser.add_section('node')
            with file(self.properties, "w+") as fOut:
                self.parser.write(fOut)
        
        self.getPreviousIP()
        self.getCurrentIP()
        
        self.updateProperties(self.parser, self.properties, 'user', self.user)
        
        if self.prevInternalIp == "":
            self.updateProperties(self.parser, self.properties, 'internalIp', self.curInternalIp)
        
        if self.prevExternalIp == "":
            self.updateProperties(self.parser, self.properties, 'externalIp', self.curExternalIp)

        if self.prevHostName == "":
            self.updateProperties(self.parser, self.properties, 'hostName', self.curHostName)
        
    
    def getPreviousIP(self):
        if os.path.isfile(self.properties):
            try:
                self.prevHostName = self.parser.get('node', 'hostName')
                self.prevInternalIp = self.parser.get('node', 'internalIp')
                self.prevExternalIp = self.parser.get('node', 'externalIp')
    
                self.user = self.parser.get('node', 'user')
     
            except Exception as inst:
                output = "ERROR GENERATED IN getPreviousIP:\n"
                output += "Exception Type: " + str(type(inst)) + "\n"
                output += "Exception: " + str(inst) + "\n"
                print output
                
        else:
            if self.initialRun == True:
                self.getCurrentIP()
                self.prevHostName = self.curHostName
                self.prevInternalIp = self.prevInternalIp
                self.prevExternalIp = self.prevExternalIp
                self.initialRun == False
                
            
            
            
    def getCurrentIP(self):
        ips = GetIP()
        self.curInternalIp = ips.internalIP
        self.curExternalIp = ips.externalIP.strip()
        self.curHostName = ips.host
        self.user = ips.user
        
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
            
        
    def updateOnChangeInIpOrHost(self):
        #add error handling on properties update
        self.hasChanged = False
        self.internalIpHasChanged = False
        self.exteralIpHasChanged = False
        self.hostHasChanged = False
        
        if self.curExternalIp != self.prevExternalIp:
            self.exteralIpHasChanged = True
            self.hasChanged = True
            self.updateProperties(self.parser, self.properties, 'externalIp',self.curExternalIp)
            self.prevExternalIp = self.curExternalIp
            
        if self.curInternalIp != self.prevInternalIp:
            self.internalIpHasChanged = True
            self.hasChanged = True
            self.updateProperties(self.parser,self.properties, 'internalIp',self.curInternalIp)
            self.prevInternalIp = self.curInternalIp
            
        if self.curHostName  != self.prevHostName:
            self.hostHasChanged = True
            self.hasChanged = True
            self.updateProperties(self.parser, self.properties, 'hostName',self.curHostName)
            self.prevHostName = self.curHostName
          
            
        return self.hasChanged      
        
if __name__ == "__main__":
    watch = WatchIP()
    
    if watch.updateOnChangeInIpOrHost():
        print "Either the IP has changed or this is the first time we've run"
    else:
        print "Nothing changed"
        
        
        