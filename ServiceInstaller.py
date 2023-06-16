import os
import sys
import win32serviceutil
import win32service
import win32event
import servicemanager
import subprocess
import time


#class for win service
class PythonScriptService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'PythonScanner'
    _svc_display_name_ = 'Python Scan Script'

    #constructor    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_alive = True

    #destructor
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_alive = False

    #event running
    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                             servicemanager.PYS_SERVICE_STARTED,
                             (self._svc_name_, ''))
        self.main()

    #main function
    def main(self):
        while self.is_alive:
            from input_values import importv
            from scanner import scan
            from remover import remove
            from rescanner import rescan
            from writing import write
            #import all important path variables
            pattern=r'[0-9]{5}\-[0-9]{7}_[0-9]{4}_[0-9]{1}_[a-zA-z]'
            days, scanfolder, donefolder, oldfolder, problemfolder, logsfolder, delay,repeat_time,check_word=importv()
            
            scan(scanfolder, donefolder,oldfolder,problemfolder,logsfolder, delay,pattern)
            rescan(donefolder,problemfolder,logsfolder,check_word,pattern)
            remove(days,donefolder,logsfolder)
            write(logsfolder)

    
           

            # repeat every 5 min 
            time.sleep(5*repeat_time)  # Sleep for 5 minutes

#all instructions to service together 
if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(PythonScriptService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(PythonScriptService)
