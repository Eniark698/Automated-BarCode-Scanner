.\temp\nssm.exe install ScannerDashboard "python.exe" 
.\temp\nssm.exe set ScannerDashboard AppDirectory "F:\code_for_scan\Automated-BarCode-Scanner"
.\temp\nssm.exe set ScannerDashboard AppParameters "-m streamlit run F:\code_for_scan\Automated-BarCode-Scanner\dashboard.py  --server.port 8501 --server.baseUrlPath /scanner/dashboard/ --server.enableCORS true --server.enableXsrfProtection true"
.\temp\nssm.exe set ScannerDashboard DisplayName "Dashboard for Python Scan Script"
.\temp\nssm.exe set ScannerDashboard Description "Dashboard provide an info about each scanned document, heat map with scans and line chart of scanning per day."
.\temp\nssm.exe set ScannerDashboard Start SERVICE_DELAYED_AUTO_START
.\temp\nssm.exe start ScannerDashboard