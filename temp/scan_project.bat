.\temp\nssm.exe install PythonScanner "python.exe" "F:\code_for_scan\Automated-BarCode-Scanner\main.py"
.\temp\nssm.exe set PythonScanner AppDirectory "F:\code_for_scan\Automated-BarCode-Scanner"
.\temp\nssm.exe set PythonScanner DisplayName "Python Scan Script"
.\temp\nssm.exe set PythonScanner Description "Automated BarCode Scanner is a service that scans files for barcodes, detects them, and filters the files based on barcode information."
.\temp\nssm.exe set PythonScanner Start SERVICE_DELAYED_AUTO_START
.\temp\nssm.exe start PythonScanner