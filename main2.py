import os
import sys
import win32serviceutil
import win32service
import win32event
import servicemanager
import subprocess
import time



class PythonScriptService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'PythonScriptService'
    _svc_display_name_ = 'Python Script Service'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_alive = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_alive = False

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                             servicemanager.PYS_SERVICE_STARTED,
                             (self._svc_name_, ''))
        self.main()

    def main(self):
        while self.is_alive:
            # Call your other Python scripts here
            from input_values import importv
            from scanner import scan
            from remover import remove
            days, scanfolder, donefolder, oldfolder, problemfolder, logsfolder=importv()
            scan(scanfolder, donefolder,oldfolder,problemfolder,logsfolder)
            remove(days, donefolder,logsfolder)
            

           

            # Sleep for a while before running the scripts again
            time.sleep(5*60)  # Sleep for 5 minutes

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(PythonScriptService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(PythonScriptService)
