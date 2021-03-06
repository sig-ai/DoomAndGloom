import ctypes
from sys import exc_info
import traceback
import code

def updateVar(var_name, new_val, frame, local=True):
  if(local):
    frame.f_locals.update({var_name:new_val})
  else:
    frame.f_globals.update({var_name:new_val})
  ctypes.pythonapi.PyFrame_LocalsToFast(ctypes.py_object(frame), ctypes.c_int(0))

def signal_handler(signal, frame):
    rerun = True
    exitFlag = False
    print ""
    print "Entered interrupt handler!"
    compFrame = frame

    #enable getting frame for:
    #  agent
    #  components
    #  baseline
    #return 

    while "general.py" not in compFrame.f_code.co_filename:
        print compFrame.f_code.co_filename
        compFrame = compFrame.f_back
    d={'_frame':compFrame}         
    d.update(compFrame.f_globals)  
    d.update(compFrame.f_locals)

    i = code.InteractiveConsole(d)
    message  = "Signal received : entering python shell.\nTraceback:\n"
    message += ''.join(traceback.format_stack(frame))
    message += '\n use the command listenEnable[0] = False to reenable the listener! (ctrl+d) to exit'
    i.interact(message)
    return
