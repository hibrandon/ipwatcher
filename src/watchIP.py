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
        #make this a global import
        self.properties = '.ip_properties'
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


        self.parser = SafeConfigParser()
        self.parser.read(self.properties)
        
        self.getPreviousIP()
        self.getCurrentIP()
        
        self.updateProperties(self.parser, 'user', self.user)
        
        
    
    def getPreviousIP(self):
        try:
            self.prevHostName = self.parser.get('node', 'hostName')
            self.prevInternalIp = self.parser.get('node', 'internalIp')
            self.prevExternalIp = self.parser.get('node', 'externalIp')

            self.user = self.parser.get('node', 'user')
 
        except Exception as inst:
            print 'Here'
            output = "ERROR GENERATED:\n"
            output += "Exception Type: " + str(type(inst)) + "\n"
            output += "Exception: " + str(inst) + "\n"
            print output
            
            
    def getCurrentIP(self):
        ips = GetIP()
        self.curInternalIp = ips.internalIP
        self.curExternalIp = ips.externalIP.strip()
        self.curHostName = ips.host
        self.user = ips.user
        
    def updateProperties(self,parser, key, val, section='node', propFile='.ip_properties'):
        try:
            parser.set(section, key, val)
            
            with open(propFile, 'w') as fOut:
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
            self.updateProperties(self.parser, 'externalIp',self.curExternalIp)
            self.prevExternalIp = self.curExternalIp
            
        if self.curInternalIp != self.prevInternalIp:
            self.internalIpHasChanged = True
            self.hasChanged = True
            self.updateProperties(self.parser,'internalIp',self.curInternalIp)
            self.prevInternalIp = self.curInternalIp
            
        if self.curHostName  != self.prevHostName:
            self.hostHasChanged = True
            self.hasChanged = True
            self.updateProperties(self.parser, 'hostName',self.curHostName)
            self.prevHostName = self.curHostName
          
            
        return self.hasChanged      
        
if __name__ == "__main__":
    watch = WatchIP()
    
    if watch.updateOnChangeInIpOrHost():
        print "Either the IP has changed or this is the first time we've run"
    else:
        print "Nothing changed"
        
        
        