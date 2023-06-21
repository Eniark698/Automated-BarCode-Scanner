import os
import sys
import win32serviceutil
import win32service
import win32event
import servicemanager
import subprocess



#class for win service
class PythonScriptService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'PythonScanner'
    _svc_display_name_ = 'Python Scan Script'
    _svc_description_ = """Automated BarCode Scanner is a service that scans files for barcodes
    , detects them, and filters the files based on barcode information.
    It reads input files, scans for barcodes, writes data to a database, and manages file movement.
    The service supports various photo types, enables rescanning of problem files
    , and offers easy installation and configuration.
    Achieve efficient barcode scanning with this automation solution."""




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
        import main  # Import the main module
        while self.is_alive:
            main.run_main_loop()

#all instructions to service together
if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(PythonScriptService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(PythonScriptService)
