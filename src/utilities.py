#utility functions
import os
from Tkinter import *
from datetime import date
from time import strftime




## -------------------------------------------------------------------------------------------
## writeLog -   Function to open a log file, write to it and close it.  If no
##              log file exist the function will write to stdout
##
## param        log    - path to the log file, Default is Empty String
##              string - String to write to file, Default is Empty String  
## -------------------------------------------------------------------------------------------
    
def writeLog(log="",string="",writeType='a'):
    """
    Writes the value of STRING to LOG.  The default mode is append.
    If LOG is not provided then the function prints to stdout"
    """
    if log == "" or log == None:
        print string
        
    else:
        try:               
            with open(log, writeType) as f:
                f.write(string)
                f.close()           
        except:
            print "Error writing output to log: \n"
            print "OUTPUT: ",string
            print "LOG: ",log
            
            

## -------------------------------------------------------------------------------------------
## END writeLog
## -------------------------------------------------------------------------------------------   


def changeList2String(listToChange, delimiter=', '):
    """
        Function to change a list to a comma separated string with an and as for the
        the last conjunction
    """
    stringVersion = ""
    finalString = ""
    
    if type(listToChange).__name__ != 'list':
        print "PARAMETER ERROR:"
        print """Expected:\t<type 'list'>"""
        print "Received:\t", type(listToChange)
        
    else:
        listToChange = map(lambda value: str(value),listToChange)
        stringVersion = delimiter.join(listToChange)
        lastCommaIndex = stringVersion.rfind(delimiter)
        finalString = stringVersion[:lastCommaIndex]
        finalString += stringVersion[lastCommaIndex:len(stringVersion)].replace(",", ', and')

    return finalString

                        
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

def createPropertiesFile(filePath, parser, sectionDict):
    success = True
    output = ""
    
    try:        
        for section in sectionDict.iterkeys():
            parser.add_section(section)
            
            for option in sectionDict[section]:
                parser.set(section,option,'')
            
            
        with open (filePath, "w") as fOut:
            parser.write(fOut)
            
    except Exception as e:
        success = False
        output = "ERROR GENERATED: utlitities.createPropertiesFile:\n"
        output += "Exception Type: " + str(type(e)) + "\n"
        output += "Exception: " + str(e) + "\n"
    
    return success,output    
            
def updateProperties(parser, propertiesFile, key, val, section='email'):
    success = True
    output = ""
    try:
        parser.set(section, key, val)
        with open(propertiesFile, 'w') as fOut:
            parser.write(fOut)
            
    except Exception as inst:
        success = False
        output = "ERROR GENERATED in Utilities.UpdateProperties:\n"
        output += "Exception Type: " + str(type(inst)) + "\n"
        output += "Exception: " + str(inst) + "\n"
    
    return success, output

def isPropertiesFileIntact(propertiesFile, parser, sectionDict):
    intact = True
    output = ""
    
    if os.path.exists(propertiesFile) == False:
        intact = False
        
    else:
        try:
            for section in sectionDict.iterkeys():
                if parser.has_section(section) == False:
                    intact = False
                    break;
                else:
                    for option in sectionDict[section]:
                        if parser.has_option(section, option) == False:
                            intact = False
                            break;
                        
        except Exception as inst:
            intact = False
            output = "ERROR GENERATED in Utilities.UpdateProperties:\n"
            output += "Exception Type: " + str(type(inst)) + "\n"
            output += "Exception: " + str(inst) + "\n"
        
    return intact, output
                    
def deleteFile(filePath):
    deleted = True
    output =""
    try:
        if os.path.exists(filePath):
            os.remove(filePath)
            
    except Exception as inst:
        deleted = False
        output = "ERROR GENERATED in Utilities.UpdateProperties:\n"
        output += "Exception Type: " + str(type(inst)) + "\n"
        output += "Exception: " + str(inst) + "\n"
        
    return deleted, output
            
    
    
