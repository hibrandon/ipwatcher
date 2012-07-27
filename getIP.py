import os

## ----------------------------------------------------------------------------
## captureOutput -  Wrapper function that captures the standard output of an
##                  external command and returns that ouput in string format
##                  
## ---------------------------------------------------------------------------- 
def captureOutput(cmd):
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

#Demo Purposes:
cmd = r'curl -s icanhazip.com'

ip = captureOutput(cmd)
print "IP: ", ip