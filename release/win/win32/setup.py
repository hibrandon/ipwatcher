#windows setup script using cx_freeze
#execute from the command line with python setup.py build

##import sys
##from cx_Freeze import setup, Executable
##
### Dependencies are automatically detected, but it might need fine tuning.
##build_exe_options = {"packages": ["email"]}
##
### GUI applications require a different base on Windows (the default is for a
### console application).
##base = None
##if sys.platform == "win32":
##    base = "Win32GUI"
##
##setup(  name = "IP WatchDog",
##        version = "0.1",
##        description = "My GUI application!",
##        options = {"build_exe": build_exe_options, "icon":"..\images\ojo.ico"},
##        executables = [Executable("emailAfterExec.pyw", base=base)])

build_exe_options = {"packages": ["os","email"]}

from cx_Freeze import setup, Executable
 
setup(
    name = "SimpleNotificationSystem",
    version = "0.1",
    description = "An example wxPython script",
    options = {"build_exe": build_exe_options},
    executables = [Executable("simpleNotificationSystem.pyw")]
    )
