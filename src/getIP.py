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
import socket
import getpass

## ----------------------------------------------------------------------------
## captureOutput -  Wrapper function that captures the standard output of an
##                  external command and returns that output in string format
##                  
## ---------------------------------------------------------------------------- 
class GetIP:

    def __init__(self):
        self.internalIP = self.getInternalIP()
        self.externalIP = self.getExternalIP()
        self.host = self.getHost()
        self.user = self.getCurrentUser()
        
    def captureOutput(self,cmd):
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
       
    def getExternalIP(self):
        #Demo purposes switch this to whatsmyip.org or a php version on my site
        cmd = r'curl -s icanhazip.com'
        ip = self.captureOutput(cmd)
        
        return ip
    
    def getInternalIP(self):
        return socket.gethostbyname(socket.gethostname()) 
    
    def getHost(self):
        return socket.gethostname()
    
    def getCurrentUser(self):
        return getpass.getuser()
        
        
        
    
if __name__ == "__main__":
    ips = GetIP()
    print "External:\t",ips.externalIP.strip()
    print "Internal:\t",ips.internalIP
    print "Host Name:\t",ips.host
    print "Current User: \t",ips.user
    print "Done"  