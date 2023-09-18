import win32serviceutil
import win32service
import win32event
import subprocess

class ScannerDashboard(win32serviceutil.ServiceFramework):
    _svc_name_ = "ScannerDashboard"
    _svc_display_name_ = "Dashboard for Python Scan Script"
    _svc_description_ = "Dashboard provide an info about each scanned document, heat map with scans and line chart of scanning per day."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        subprocess.run(['F:/code_for_scan/Automated-BarCode-Scanner/temp/dash.bat'])
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

if __name__ == '__main__':
   win32serviceutil.HandleCommandLine(ScannerDashboard)
